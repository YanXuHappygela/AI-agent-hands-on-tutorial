# Additional Test Design: Source Collection vs. Citation Analysis

**Purpose:** Determine whether skill-constrained agents found fewer sources during research OR found similar sources but cited fewer in reports

**Date:** 2026-03-26
**Test Version:** 1.0

---

## Research Question

**Primary:** Did SourceValidationSkill + SearchStrategySkill cause the research agent to:
- **Hypothesis A:** Collect fewer sources during research phase (search constraint)
- **Hypothesis B:** Collect similar sources but filter more at reporting phase (citation constraint)

**Why This Matters:** Understanding whether skills constrain search or reporting has significant implications for skill design optimization.

---

## Test Methodology

### Phase 1: Intermediate Output Analysis

**Objective:** Extract all sources found during research phase regardless of final citation

**Data Sources:**
1. `agent_outputs/research_specialist_research_phase_20260326_114745.md` (Baseline)
2. `agent_outputs/research_specialist_agent_output_20260326_120636.md` (Skilled)

**Analysis Steps:**

1. **Extract all web_search results** mentioned in intermediate outputs
2. **Extract all content_extractor calls** with URLs
3. **Count total unique URLs accessed** by each research agent
4. **Categorize sources** by type (news, think tank, government, academic)
5. **Compare collection patterns** between baseline and skilled

**Expected Outputs:**
- Baseline research agent URL collection log
- Skilled research agent URL collection log
- Comparative statistics table

### Phase 2: Citation Mapping

**Objective:** Map collected sources to final report citations

**Analysis Steps:**

1. **Identify sources cited** in BASELINE_REPORT.md
2. **Identify sources cited** in SKILLED_REPORT.md
3. **Calculate citation rate:** Citations / Sources_collected
4. **Identify filtered sources:** Collected but not cited
5. **Categorize filtering patterns:** Why were sources excluded?

**Expected Outputs:**
- Citation efficiency metrics (% of collected sources that appear in report)
- Filtering analysis (what types of sources were excluded)

### Phase 3: Search Query Analysis

**Objective:** Analyze search queries used to understand strategy differences

**Data Sources:**
- Intermediate research agent outputs with web_search queries

**Analysis Steps:**

1. **Extract all search queries** executed by both agents
2. **Classify queries** by temporal specificity:
   - Generic (no date qualifiers)
   - Date-qualified ("March 2026", "2026")
   - Specific event searches
3. **Analyze query progression:** Did queries refine over time?
4. **Count follow-up queries:** Evidence of adaptive search?

**Expected Outputs:**
- Query pattern comparison
- Temporal qualifier usage rate
- Query refinement evidence

---

## Test Execution Plan

### Step 1: Parse Intermediate Outputs

```bash
# Extract research phase outputs
grep -E "(web_search|content_extractor|URL|http)" agent_outputs/research_specialist_*.md > research_urls.txt

# Count unique URLs per agent
grep -oE 'https?://[^\s]+' agent_outputs/research_specialist_research_phase_*.md | sort | uniq | wc -l
grep -oE 'https?://[^\s]+' agent_outputs/research_specialist_agent_output_*.md | sort | uniq | wc -l
```

### Step 2: Manual Analysis of Intermediate Files

**For each research agent output:**

1. Read full intermediate output file
2. Log each source mentioned during research
3. Note source type and date (if visible)
4. Track whether source appeared in final report
5. Document explicit filtering decisions (if mentioned)

### Step 3: Create Source Collection Matrix

| Source URL/Type | Baseline Collected | Baseline Cited | Skilled Collected | Skilled Cited |
|-----------------|-------------------|----------------|-------------------|---------------|
| Reuters article | Yes | Yes | Yes | Yes |
| CSIS report | Yes | No | Yes | Yes |
| ...etc | ... | ... | ... | ... |

### Step 4: Statistical Analysis

**Key Metrics:**

1. **Collection Count Ratio:**
   ```
   Skilled_sources_collected / Baseline_sources_collected
   ```
   - If < 1.0: Skilled agent collected fewer (search constraint)
   - If ≈ 1.0: Skilled agent collected similar (citation constraint)

2. **Citation Efficiency:**
   ```
   Citations_in_report / Sources_collected
   ```
   - Higher in skilled = more aggressive filtering
   - Similar = both filtered similarly

3. **Source Type Shift:**
   ```
   % Tier1_sources_collected (Baseline vs Skilled)
   ```
   - Higher in skilled = search strategy targeted better sources

---

## Expected Outcomes Matrix

### Scenario A: Search Constraint Hypothesis

**If SearchStrategySkill constrained collection:**

| Metric | Expected Pattern |
|--------|------------------|
| Sources collected | Skilled < Baseline (fewer collected) |
| Citation rate | Similar (both cite ~50% of what they find) |
| Source quality | Skilled higher (targetted search) |
| Query specificity | Skilled higher (temporal qualifiers) |

**Interpretation:** Skills optimize search to find fewer but better sources upfront

### Scenario B: Citation Constraint Hypothesis

**If SourceValidationSkill constrained reporting:**

| Metric | Expected Pattern |
|--------|------------------|
| Sources collected | Skilled ≈ Baseline (similar collected) |
| Citation rate | Skilled < Baseline (more filtering) |
| Source quality | Skilled higher (better curation) |
| Query specificity | Similar (both search broadly) |

**Interpretation:** Skills filter at reporting stage, rejecting lower-quality sources

### Scenario C: Both Constraints (Most Likely)

**If both skills work in tandem:**

| Metric | Expected Pattern |
|--------|------------------|
| Sources collected | Skilled < Baseline (some search constraint) |
| Citation rate | Skilled < Baseline (also reporting constraint) |
| Source quality | Skilled significantly higher |
| Query specificity | Skilled higher |

**Interpretation:** SearchStrategy finds fewer but better; SourceValidation filters even more stringently

---

## Data Collection Instrument

### Research Agent Source Log Template

**Agent:** [Baseline / Skilled]
**Timestamp:** [Date/Time]

For each source encountered:

```
Source ID: [Sequential number]
Discovery Method: [web_search / content_extractor / mentioned]
Source Type: [News / Think Tank / Government / Academic / Other]
URL: [If available]
Date: [Publication date if extracted]
Tier: [1 / 2 / 3 / Unknown]
Cited in Report: [Yes / No]
Filtering Reason: [If not cited, why? Generic, outdated, unreliable, etc.]
```

---

## Pilot Test: Manual Analysis Sample

Let me demonstrate with the first 5 sources from each intermediate output:

### Baseline Research Agent (sample from intermediate output)

Will need to read: `agent_outputs/research_specialist_research_phase_20260326_114745.md`

### Skilled Research Agent (sample from intermediate output)

Will need to read: `agent_outputs/research_specialist_agent_output_20260326_120636.md`

---

## Test Execution Checklist

- [ ] Read baseline research intermediate output
- [ ] Read skilled research intermediate output
- [ ] Extract all URLs and sources mentioned
- [ ] Count unique sources collected per agent
- [ ] Map sources to final report citations
- [ ] Calculate collection and citation metrics
- [ ] Analyze query patterns
- [ ] Classify filtering decisions
- [ ] Generate comparison matrix
- [ ] Write findings report

**Estimated Time:** 2-3 hours manual analysis

---

## Success Criteria

This test will be successful if we can definitively answer:

1. **Collection Count:** Did skilled agent collect fewer sources? (Hypothesis A vs B)
2. **Citation Rate:** What % of collected sources were cited in each report?
3. **Quality Differential:** Were skilled sources measurably higher quality?
4. **Search Strategy:** Do query patterns show temporal constraint application?

If analysis reveals Scenario C (both constraints), we can conclusively state:
> "Skills optimize research at BOTH collection and reporting stages - SearchStrategy targets better sources, SourceValidation curates more stringently."

---

## Potential Findings Impact

### If Hypothesis A (Search Constraint)

**Implication:** SearchStrategySkill is highly effective at query optimization
**Recommendation:** Emphasize query formulation guidance in skill design
**Demo Message:** "Skills enable agents to find better sources faster, not just filter better"

### If Hypothesis B (Citation Constraint)

**Implication:** SourceValidationSkill does heavy lifting at reporting stage
**Recommendation:** Consider adding filtering guidance at collection stage too
**Demo Message:** "Skills ensure only high-quality sources make it to reports, maintaining research breadth"

### If Hypothesis C (Both Constraints)

**Implication:** Skills compose effectively across research pipeline
**Recommendation:** Current design is optimal - keep both skills
**Demo Message:** "Skills work in tandem - better search + stricter validation = quality results"

---

## Next Steps After Test

1. **Implement automated parsing** of intermediate outputs (Python script)
2. **Run test on multiple research topics** for robustness
3. **Develop source quality rubric** for objective tier assignment
4. **Create visualization** of source collection → citation pipeline
5. **Publish findings** in revised comparison analysis

---

## Appendix: Automated Analysis Script (Pseudocode)

```python
def analyze_source_collection(baseline_output, skilled_output):
    """
    Parse intermediate agent outputs to extract source collection patterns
    """
    baseline_sources = extract_sources(baseline_output)
    skilled_sources = extract_sources(skilled_output)

    baseline_citations = extract_citations(BASELINE_REPORT)
    skilled_citations = extract_citations(SKILLED_REPORT)

    metrics = {
        'collection_count': {
            'baseline': len(baseline_sources),
            'skilled': len(skilled_sources),
            'ratio': len(skilled_sources) / len(baseline_sources)
        },
        'citation_rate': {
            'baseline': len(baseline_citations) / len(baseline_sources),
            'skilled': len(skilled_citations) / len(skilled_sources)
        },
        'quality_shift': calculate_tier_distribution(baseline_sources, skilled_sources)
    }

    return metrics
```

---

**Test Design Complete** ✅
**Ready for execution upon approval**
