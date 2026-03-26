# Session 4: Agent Skills - Design Specification

**Version:** 1.0
**Date:** March 26, 2026
**Author:** AI Builder Meetup Series

---

## Executive Summary

Session 4 demonstrates the power of **Agent Skills** by enhancing the multi-agent research system from Session 3 with three targeted skills. The demo compares baseline agents (no skills) vs skilled agents on a challenging, fast-moving research topic: the March 2026 US-Iran-Israel escalation.

**Key Skills:**
1. **SearchStrategySkill** - Guides effective query formulation and recency filtering
2. **SourceValidationSkill** - Validates source authority and cross-references claims
3. **RecencyAwarenessSkill** - Sets temporal requirements for current events research

**Target Audience:** Developers building production AI agents
**Key Takeaway:** Targeted skills dramatically improve agent reliability, accuracy, and trustworthiness

---

## Background and Motivation

### The Problem
The Session 3 multi-agent research system works well for general research, but struggles with:
- **Fast-moving topics:** Generic search returns outdated information
- **Source quality:** Agents can't distinguish authoritative sources from unreliable ones
- **Temporal awareness:** No understanding that "March 2026 events" requires very recent sources
- **Claim verification:** Accepts information without cross-referencing

### The Solution
Rather than re-architecting the multi-agent system, we add **laser-focused skills** to specific agents:
- **Planning Agent** gets RecencyAwarenessSkill → sets temporal constraints
- **Research Agent** gets SearchStrategySkill + SourceValidationSkill → finds and validates current sources
- **Critic Agent** could also use SourceValidationSkill → validates final report

### Why This Approach
- ✅ **Surgical enhancement:** Add skills only where needed, not everywhere
- ✅ **Composable:** Skills build on each other across the agent pipeline
- ✅ **Reusable:** Each skill is a standalone pattern developers can adapt
- ✅ **Measurable:** Side-by-side comparison shows clear before/after improvement

---

## Research Topic

### Title
**"March 2026 US-Iran-Israel Escalation: What Happened, What's Next, Who's Reporting What"**

### Research Questions
1. **What happened?** Timeline of key events in March 2026 (incidents, statements, actions)
2. **What's next?** Expert predictions for near-term trajectory (escalation risks, diplomatic efforts, scenarios)
3. **Who's reporting what?** Source reliability and perspective analysis (US/Israeli/Iranian/international framing)

### Why This Topic is Ideal for the Demo

| Aspect | Why It Works |
|--------|--------------|
| **Recency Critical** | Events from March 2026 (this month!) - baseline agents will cite outdated sources from 2025 or earlier |
| **Source Quality Varies** | Mix of official statements, think tank analysis, news reports, social media, propaganda - skilled agents must filter |
| **Multiple Perspectives** | US, Iranian, Israeli sources have different framings - demonstrates bias awareness |
| **High Stakes** | Real-world, consequential topic shows why agent reliability matters |
| **Clear Comparison** | Easy to annotate side-by-side: outdated vs current, unreliable vs authoritative |

### Demo Risk Mitigation
- **Topic sensitivity:** Focus on analytical perspective, not political advocacy
- **Misinformation:** The SourceValidationSkill specifically addresses this
- **Rapidly changing:** If the situation changes dramatically during demo prep, we can shift to "late March 2026" to lock in a stable snapshot

---

## Skills Design

**Note:** Complete skill implementations are available in the `skills/` directory:
- `skills/search-strategy/SKILL.md` - SearchStrategySkill
- `skills/source-validation/SKILL.md` - SourceValidationSkill
- `skills/recency-awareness/SKILL.md` - RecencyAwarenessSkill

### Skill 1: SearchStrategySkill (Research Agent)

**Location:** `skills/search-strategy/SKILL.md`

#### Purpose
Guides the Research Agent to formulate effective search queries and use temporal filters for current events.

#### Key Behaviors

```markdown
# SearchStrategySkill

You are researching **fast-moving, current events**. Use these search strategies:

## Temporal Query Construction
1. **Include temporal qualifiers in every query:**
   - "March 2026", "latest", "recent", "current"
   - Example: "US Iran Israel tensions March 2026" NOT "US Iran Israel conflict"

2. **Use date filters when available:**
   - Limit results to last 30 days for breaking news topics
   - If researching events from "March 2026", only sources from March 2026 are relevant

## Query Progression
3. **Start broad, then narrow:**
   - First: "US Iran Israel tensions March 2026" (overview)
   - Then: "US Iran [specific incident name] March 2026" (details)
   - Finally: "[expert name/org] analysis US Iran March 2026" (expert opinion)

## Source Diversification
4. **Target multiple source types:**
   - Think tanks: "CSIS US Iran March 2026", "CFR Israel Iran analysis"
   - Government sources: "State Department Iran March 2026", "IDF statement"
   - News: "Reuters US Iran March", "AP Israel Iran latest"
   - Academic: "Foreign Affairs US Iran 2026"

## Adaptive Search
5. **Follow-up based on findings:**
   - If you find mention of a specific incident → search for that incident name directly
   - If you find an expert quoted → search for their full analysis
   - If you find conflicting info → search for fact-checks or cross-references

## What NOT to Do
- ❌ Generic queries like "US Iran conflict" (too broad, gets old results)
- ❌ Accepting first page results without checking dates
- ❌ Single-source reliance - always diversify
```

#### Impact
- **Without:** "US Iran conflict" → results from 2023-2024, misses March 2026 events
- **With:** "US Iran Israel tensions March 2026" → current analysis, recent developments

---

### Skill 2: SourceValidationSkill (Research Agent or Critic Agent)

**Location:** `skills/source-validation/SKILL.md`

#### Purpose
Validates source authority, publication dates, and cross-references factual claims.

#### Key Behaviors

```markdown
# SourceValidationSkill

You are gathering information for a research report. **Every source must be validated** before inclusion.

## Date Validation
1. **Check publication date for EVERY source:**
   - For events in "March 2026", sources must be from Feb-March 2026 minimum
   - Sources older than 1 month are likely outdated for this topic
   - ALWAYS include publication date in your citations

#### Authority Assessment
2. **Prioritize authoritative sources:**
   - ✅ **Tier 1:** Government officials, established think tanks (CSIS, CFR, IISS, Carnegie), major news agencies (AP, Reuters, BBC)
   - ⚠️ **Tier 2:** Reputable regional outlets, credentialed experts, mainstream news
   - ❌ **Tier 3:** Unknown blogs, social media posts, unverified sources

3. **Note source credentials:**
   - Is this a known organization with track record?
   - Is the author an expert in the field?
   - Does the source have potential bias? (Note it, don't exclude)

## Claim Cross-Reference
4. **Verify factual claims:**
   - If a source makes a factual claim (date, event, statement), find at least ONE other independent source confirming it
   - If you can't verify, label it as "unverified" or "according to [source]"
   - Be especially careful with casualty numbers, attribution of responsibility, timing

## Bias Awareness
5. **Flag potential bias:**
   - US government sources have US perspective
   - Iranian state media has Iranian perspective
   - Israeli sources have Israeli perspective
   - This doesn't disqualify them - just note the framing

## Citation Format
6. **All citations must include:**
   - Source name/organization
   - Publication date (critical!)
   - Brief authority note if relevant
   - Example: "According to CSIS analysis (March 15, 2026)..." or "Reuters reports (March 20, 2026)..."

## Red Flags
❌ **Reject sources that:**
- Have no identifiable author or organization
- Make extraordinary claims without evidence
- Are clearly dated before the events they claim to describe
- Appear to be disinformation or propaganda without labeling
```

#### Impact
- **Without:** Cites unreliable sources, accepts claims without verification, no date checking
- **With:** Every source is dated and assessed, claims are cross-referenced, bias is noted

---

### Skill 3: RecencyAwarenessSkill (Planning Agent)

**Location:** `skills/recency-awareness/SKILL.md`

#### Purpose
Identifies when research topics require current information and sets explicit temporal constraints.

#### Key Behaviors

```markdown
# RecencyAwarenessSkill

You are creating a research plan. **Detect temporal requirements** and set appropriate constraints.

## Temporal Signal Detection
1. **Recognize signals that recency is critical:**
   - Dates: "March 2026", "2026", "current", "latest", "recent"
   - Events: "escalation", "crisis", "breaking", "developing"
   - Verbs: "What is happening", "current status", "latest developments"

2. **When detected, set explicit requirements:**
   - "All sources must be from [specific month/year]"
   - "Prioritize sources from the last [X days/weeks]"
   - "Historical context is secondary to current analysis"

## Plan Components
3. **For current events research, your plan must include:**
   - **Recency requirement:** Explicit date window for acceptable sources
   - **Source freshness check:** Instruct researchers to verify publication dates
   - **Update awareness:** Note that situation may evolve beyond research date
   - **Timeline focus:** Emphasize recent developments over historical background

## Example Plan Element
```
RECENCY REQUIREMENT: This research is about events in March 2026.
- All primary sources must be dated February-March 2026 or later
- Background sources may be older but must be noted as historical context
- Researchers should prioritize the question "What is happening NOW" over "What has happened historically"
```

## Temporal Decay Warning
4. **Flag when older analysis may be outdated:**
   - "Analysis from before March 2026 may not reflect recent escalations"
   - "Predictions made in 2025 should be compared with actual 2026 developments"
   - "Historical context is useful but distinct from current state"

## What to Avoid
❌ **Don't:**
- Create generic research plans for time-sensitive topics
- Assume researchers will figure out recency requirements on their own
- Mix historical analysis and current events without clear delineation
```

#### Impact
- **Without:** Generic research plan, no temporal constraints, researchers find whatever
- **With:** Clear recency requirements, all downstream agents know to prioritize current sources

---

## Demo Structure

### Overall Flow (45 minutes total)

#### Part 1: Setup (5 minutes)
- **Recap Session 3:** Quick reminder of the 5-agent research system (Planning → Research → Analysis → Writing → Critic)
- **Introduce challenge:** "How do we make agents reliable for fast-moving, high-stakes topics?"
- **Preview:** Show the three skills we'll add and explain why each matters

#### Part 2: Baseline Run (10 minutes)
**Objective:** Show the problems that skills solve

1. Run multi-agent system WITHOUT any skills
2. Display research plan (no recency requirements)
3. Show research queries (generic, no temporal filters)
4. Display final report
5. **Highlight problems:**
   - ❌ Timeline missing March 2026 events (cites older incidents)
   - ❌ Sources from 2023-2025 (outdated analysis)
   - ❌ Unverified claims (no cross-reference)
   - ❌ No source dates (can't assess currency)
   - ❌ Missing expert predictions (didn't search for current analysis)

#### Part 3: Skilled Run (10 minutes)
**Objective:** Show how skills improve the process and output

1. Load the three skills (show skill files briefly)
2. Run multi-agent system WITH skills added:
   - RecencyAwarenessSkill → Planning Agent
   - SearchStrategySkill + SourceValidationSkill → Research Agent
3. Display research plan (explicit recency requirements)
4. Show research queries (temporal filters, diverse sources)
5. Display final report
6. **Highlight improvements:**
   - ✅ Timeline includes March 2026 developments
   - ✅ All sources dated February-March 2026
   - ✅ Claims cross-referenced
   - ✅ Source authority noted
   - ✅ Expert predictions included
   - ✅ Bias awareness noted

#### Part 4: Side-by-Side Comparison (10 minutes)
**Objective:** Make the value proposition crystal clear

1. Display both reports in split view
2. **Annotate with color coding:**
   - 🔴 **Baseline problems:** Outdated sources, missing events, unverified claims
   - 🟢 **Skill improvements:** Current sources, comprehensive timeline, validated info
   - 🟡 **Recency wins:** Specific examples where SearchStrategySkill found March 2026 sources
   - 🔵 **Validation wins:** Specific examples where SourceValidationSkill caught unreliable info

3. **Metrics comparison:**
   - Source date distribution (2023-2025 vs Feb-March 2026)
   - Source authority breakdown (Tier 1/2/3 sources)
   - Coverage completeness (events mentioned)

#### Part 5: Implementation Walkthrough (10 minutes)
**Objective:** Show developers how to build this

1. **Skill structure:** Show how skills are defined (simple markdown or Python classes)
2. **Adding skills to agents:** Code snippet showing Strands AgentSkills integration
3. **When to use each skill:**
   - RecencyAwarenessSkill → Planning agents for time-sensitive tasks
   - SearchStrategySkill → Research agents that need to find current info
   - SourceValidationSkill → Any agent that gathers information from web sources

4. **Q&A and discussion**

---

## Implementation Plan

### Artifacts to Create

1. **Jupyter Notebook:**
   - `Agent_Skills_Comparative_Study.ipynb`
   - Cells: Setup → Baseline run → Skills definition → Skilled run → Comparison → Discussion

2. **Skill Definitions:** ✅ **COMPLETED**
   - `skills/search-strategy/SKILL.md` ✅
   - `skills/source-validation/SKILL.md` ✅
   - `skills/recency-awareness/SKILL.md` ✅

3. **Documentation:**
   - Update `README.md` with Session 4 details
   - Add Colab link once notebook is ready
   - (Optional) Blog post or detailed writeup

### Technical Stack
- **Framework:** Strands (from previous sessions)
- **LLM:** Ollama with Qwen model (free, local) or OpenAI API
- **Skills Plugin:** Strands AgentSkills
- **Comparison:** Manual annotation or simple script to highlight differences

### Notebook Structure

```python
# Cell 1-2: Setup
import strands
from strands import Agent, MultiAgentOrchestrator
# ... imports

# Cell 3-4: Load Session 3 multi-agent system
planning_agent = Agent("planner", ...)
research_agent = Agent("researcher", ...)
# ... define 5 agents

# Cell 5: Define research topic
topic = """
March 2026 US-Iran-Israel Escalation:
What Happened, What's Next, Who's Reporting What
"""

# Cell 6-7: BASELINE RUN (no skills)
baseline_result = orchestrator.run(topic)
print("=== BASELINE REPORT ===")
print(baseline_result.report)
# Save for comparison

# Cell 8-10: Define and load skills
search_strategy_skill = load_skill("skills/search-strategy/SKILL.md")
source_validation_skill = load_skill("skills/source-validation/SKILL.md")
recency_awareness_skill = load_skill("skills/recency-awareness/SKILL.md")

# Add skills to agents
planning_agent.add_skill(recency_awareness_skill)
research_agent.add_skill(search_strategy_skill)
research_agent.add_skill(source_validation_skill)

# Cell 11-12: SKILLED RUN (with skills)
skilled_result = orchestrator.run(topic)
print("=== SKILLED REPORT ===")
print(skilled_result.report)

# Cell 13: Generate comparison
compare_reports(baseline_result.report, skilled_result.report)
# Highlight differences, show metrics

# Cell 14: Discussion and takeaways
"""
Key learnings:
1. Surgical skills > wholesale prompting
2. Skills compose across multi-agent pipelines
3. Measurable impact on quality metrics
"""
```

---

## Expected Outcomes

### What Developers Will Learn

1. **Practical Skill Patterns**
   - Three concrete, reusable skills for their own agents
   - Understanding of when each skill type is useful
   - Template for creating custom skills

2. **Targeted Enhancement Strategy**
   - Skills don't need to be everywhere - add them where they matter
   - Planning → set requirements, Research → execute better, Critic → validate
   - Start with 2-3 high-impact skills, not 10 marginal ones

3. **Measurable Value**
   - Side-by-side comparison proves skills aren't just "nice to have"
   - Clear metrics: source currency, authority, claim verification
   - ROI: Small skill investment → large quality improvement

4. **Implementation Simplicity**
   - Skills are often just structured prompts (markdown)
   - Easy to add to existing agents without re-architecting
   - Can start with one skill, add more incrementally

### Demo Success Criteria

✅ **Baseline clearly shows problems:** Outdated sources, missing events, unverified claims
✅ **Skilled version clearly better:** Current sources, comprehensive timeline, validated info
✅ **Differences are obvious:** Even non-technical audience can see the improvement
✅ **Developers get practical value:** Walk away with skills they can use immediately
✅ **Implementation is approachable:** Not intimidating, feels doable

---

## Alternative Variations

### If Time Permits: Add a Fourth Skill

**BiasDetectionSkill (Analysis Agent)**
- Flags when report presents single perspective
- Suggests including alternative viewpoints
- Notes when sources have clear national/political alignment

**Why add it:**
- Demonstrates skill composability (4 skills across 3 agents)
- Addresses important issue in geopolitical research
- Shows how skills can target specific quality dimensions

### If Time is Short: Reduce to Two Skills

**Keep:**
1. SearchStrategySkill (biggest impact on finding current info)
2. SourceValidationSkill (biggest impact on quality)

**Drop:**
- RecencyAwarenessSkill (planning insight is valuable but less visually dramatic)

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| **Topic too sensitive** | Focus on analytical perspective, source diversity; avoid political advocacy |
| **Situation changes during demo** | Lock in "March 15-20, 2026" timeframe; note that events continue to evolve |
| **Baseline doesn't fail enough** | Choose queries that baseline naturally struggles with; if needed, use weaker base model |
| **Skills don't show clear improvement** | Test beforehand; iterate on skill prompts until delta is dramatic |
| **Implementation too complex** | Start with markdown skills (simplest); show code only if asked |
| **Audience doesn't see value** | Lead with side-by-side comparison; make annotations very visual |

---

## Success Metrics

**Qualitative:**
- Developers understand what agent skills are
- Developers see clear value in adding skills to their agents
- Developers feel confident they could implement similar skills

**Quantitative:**
- 80%+ of sources in skilled report from Feb-March 2026 vs <50% in baseline
- 100% of sources dated in skilled report vs minimal dating in baseline
- 3+ expert predictions in skilled report vs 0-1 in baseline
- Audience survey: "Would you add skills to your agents?" >80% yes

---

## Next Steps

1. ✅ Design approved → proceed to implementation
2. ✅ Create skill definition files
3. ⏳ Build Jupyter notebook with baseline and skilled runs
4. ⏳ Test both versions and iterate on skills until delta is clear
5. ⏳ Create side-by-side comparison visualization
6. ⏳ Prepare talking points and demo script
7. ⏳ Update README and prepare Colab link

---

## Appendix: Skill Template

For developers who want to create their own skills, here's the template:

```markdown
# [SkillName]

## Purpose
[One sentence: what does this skill help the agent do better?]

## When to Use
[Conditions under which this skill should be active]

## Key Behaviors
1. **[Behavior 1 Name]**
   - [Specific action the agent should take]
   - Example: [concrete example]

2. **[Behavior 2 Name]**
   - [Specific action]
   - Example: [concrete example]

## What NOT to Do
❌ [Anti-patterns this skill helps avoid]

## Example
[Before/after showing impact of this skill]
```

---

**End of Design Specification**
