
"""Financial Stock MCP Server — FastMCP with streamable-http transport."""
import json, argparse
from datetime import datetime
import yfinance as yf
from fastmcp import FastMCP

mcp = FastMCP(
    name="financial-stock-server",
    instructions="Real-time stock market data via yfinance, served over HTTP.",
)

def _fmt(v, prefix="", suffix="", d=2):
    try:
        return f"{prefix}{v:,.{d}f}{suffix}" if v is not None else "N/A"
    except (TypeError, ValueError):
        return "N/A"

def _fmt_large(v):
    try:
        v = float(v)
        if v >= 1e12: return f"{v/1e12:.2f}T"
        if v >= 1e9:  return f"{v/1e9:.2f}B"
        if v >= 1e6:  return f"{v/1e6:.2f}M"
        return f"{v:,.0f}"
    except (TypeError, ValueError):
        return "N/A"

@mcp.tool
def get_stock_profile(symbol: str) -> str:
    """Get company profile: name, sector, industry, location, employees, description."""
    info = yf.Ticker(symbol.upper()).info
    return json.dumps({
        "symbol":      symbol.upper(),
        "company":     info.get("longName", "N/A"),
        "sector":      info.get("sector", "N/A"),
        "industry":    info.get("industry", "N/A"),
        "location":    f"{info.get('city','')}, {info.get('country','')}".strip(", "),
        "employees":   info.get("fullTimeEmployees", "N/A"),
        "website":     info.get("website", "N/A"),
        "description": (info.get("longBusinessSummary") or "")[:400],
    }, indent=2)

@mcp.tool
def get_stock_price(symbol: str) -> str:
    """Get current price, market cap, P/E ratio, 52-week range, and analyst recommendation."""
    info = yf.Ticker(symbol.upper()).info
    cur  = info.get("currentPrice") or info.get("regularMarketPrice")
    prev = info.get("previousClose") or info.get("regularMarketPreviousClose")
    chg  = (cur - prev) if (cur and prev) else None
    pct  = (chg / prev * 100) if (chg and prev) else None
    return json.dumps({
        "symbol":          symbol.upper(),
        "Current Price":   _fmt(cur, prefix="$"),
        "Change":          _fmt(chg, prefix="$", suffix=f" ({_fmt(pct, suffix='%')})"),
        "Day Range":       f"{_fmt(info.get('dayLow'), prefix='$')} - {_fmt(info.get('dayHigh'), prefix='$')}",
        "52-Week Range":   f"{_fmt(info.get('fiftyTwoWeekLow'), prefix='$')} - {_fmt(info.get('fiftyTwoWeekHigh'), prefix='$')}",
        "Market Cap":      _fmt_large(info.get("marketCap")),
        "P/E Ratio":       _fmt(info.get("trailingPE")),
        "EPS":             _fmt(info.get("trailingEps"), prefix="$"),
        "Dividend Yield":  _fmt(info.get("dividendYield",0)*100 if info.get("dividendYield") else None, suffix="%"),
        "Recommendation":  info.get("recommendationKey", "N/A"),
        "Target Price":    _fmt(info.get("targetMeanPrice"), prefix="$"),
    }, indent=2)

@mcp.tool
def get_stock_history(symbol: str, period: str = "3mo") -> str:
    """Get historical OHLCV data. period: 1d,5d,1mo,3mo,6mo,1y,2y,5y,ytd,max."""
    hist = yf.Ticker(symbol.upper()).history(period=period)
    if hist.empty:
        return json.dumps({"error": f"No data for {symbol}"})
    records = [{"date": d.strftime("%Y-%m-%d"), "open": round(float(r["Open"]),4),
                "high": round(float(r["High"]),4), "low": round(float(r["Low"]),4),
                "close": round(float(r["Close"]),4), "volume": int(r["Volume"])}
               for d, r in hist.iterrows()]
    s, e = records[0]["close"], records[-1]["close"]
    return json.dumps({
        "symbol": symbol.upper(), "period": period,
        "start_date": records[0]["date"], "end_date": records[-1]["date"],
        "period_return_pct": round((e-s)/s*100, 2),
        "period_high": round(max(r["high"] for r in records), 4),
        "period_low":  round(min(r["low"]  for r in records), 4),
        "history": records,
    }, indent=2)

@mcp.tool
def get_stock_financials(symbol: str) -> str:
    """Get revenue, margins, EPS, debt ratios, ROE, and analyst price targets."""
    info = yf.Ticker(symbol.upper()).info
    def pct(k): v = info.get(k); return _fmt(v*100 if v else None, suffix="%")
    return json.dumps({
        "symbol":            symbol.upper(),
        "Revenue (TTM)":     _fmt_large(info.get("totalRevenue")),
        "Gross Margin":      pct("grossMargins"),
        "Operating Margin":  pct("operatingMargins"),
        "Profit Margin":     pct("profitMargins"),
        "EPS (TTM)":         _fmt(info.get("trailingEps"), prefix="$"),
        "Forward EPS":       _fmt(info.get("forwardEps"), prefix="$"),
        "P/E Ratio":         _fmt(info.get("trailingPE")),
        "Debt/Equity":       _fmt(info.get("debtToEquity")),
        "ROE":               pct("returnOnEquity"),
        "Free Cash Flow":    _fmt_large(info.get("freeCashflow")),
        "Recommendation":    info.get("recommendationKey", "N/A"),
        "Target (Mean)":     _fmt(info.get("targetMeanPrice"), prefix="$"),
    }, indent=2)

@mcp.tool
def get_stock_news(symbol: str, max_articles: int = 5) -> str:
    """Get the latest news headlines and summaries for a stock."""
    news = yf.Ticker(symbol.upper()).news or []
    articles = []
    for item in news[:min(max_articles, 10)]:
        c = item.get("content", {})
        pub = c.get("pubDate", "")
        try:
            pub = datetime.fromisoformat(pub.replace("Z","+00:00")).strftime("%Y-%m-%d %H:%M UTC")
        except (ValueError, AttributeError):
            pass
        articles.append({
            "title":     c.get("title", item.get("title", "N/A")),
            "publisher": c.get("provider",{}).get("displayName", item.get("publisher","N/A")),
            "published": pub or "N/A",
            "summary":   (c.get("summary") or "")[:200],
        })
    return json.dumps({"symbol": symbol.upper(), "articles": articles}, indent=2)

@mcp.tool
def compare_stocks(symbols: str) -> str:
    """Compare multiple stocks. symbols: comma-separated tickers e.g. 'AAPL,MSFT,GOOGL'."""
    rows = []
    for sym in [s.strip().upper() for s in symbols.split(",") if s.strip()]:
        try:
            info = yf.Ticker(sym).info
            cur = info.get("currentPrice") or info.get("regularMarketPrice")
            ytd = None
            try:
                h = yf.Ticker(sym).history(period="ytd")
                if not h.empty:
                    ytd = round((h["Close"].iloc[-1]-h["Close"].iloc[0])/h["Close"].iloc[0]*100, 2)
            except Exception:
                pass
            rows.append({
                "symbol":     sym,
                "price":      _fmt(cur, prefix="$"),
                "market_cap": _fmt_large(info.get("marketCap")),
                "pe_ratio":   _fmt(info.get("trailingPE")),
                "ytd_return": f"{ytd:+.1f}%" if ytd is not None else "N/A",
                "rec":        info.get("recommendationKey", "N/A"),
            })
        except Exception as e:
            rows.append({"symbol": sym, "error": str(e)})
    return json.dumps({"comparison": rows}, indent=2)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8765)
    a = p.parse_args()
    print(f"FastMCP HTTP server starting on http://{a.host}:{a.port}/mcp")
    mcp.run(transport="streamable-http", host=a.host, port=a.port)
