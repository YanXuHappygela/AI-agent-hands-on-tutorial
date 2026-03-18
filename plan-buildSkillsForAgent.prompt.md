# Plan: Session 4 Skills Notebook

Create a new, notebook-only Session 4 that is based on the existing multi-agent research assistant and adds a comparative baseline vs skill-enabled study, a lightweight skill contract layer, and a scoreboard, sized for a 45-minute concept-heavy demo with a results-only fallback.

## Steps

1. **Create a new notebook** by copying the structure of the existing multi-agent notebook, then trim to the sections needed for the skills demo (setup, tool definitions, agent creation, orchestration, evaluation). *depends on none*

2. **Add an experiment intro** that states the hypothesis, control vs experiment conditions, and the 45-minute run-of-show (live mini-run plus results fallback). *parallel with step 3*

3. **Implement a notebook-local skill contract layer**: JSON validation, bounded retries/repair for invalid outputs, and explicit error surfacing; wire it into the existing JSON-returning tools. *depends on step 1*

4. **Add budgets and caching** for research tools (max sources, max chars, max tool calls, cached search/extract) to stabilize the demo and enable quick re-runs. *parallel with step 3*

5. **Add a rule-based scoreboard** that evaluates format correctness, budget adherence, citation presence, and recovery behavior; output a compact table for baseline vs skills. *depends on steps 3–4*

6. **Provide two runnable cells**: baseline run (skills off) and skilled run (skills on + budgets + caching), both producing artifacts and scoreboard rows. *depends on steps 3–5*

7. **Add a results-only cell** that loads cached artifacts and prints final scoreboard deltas when the full run is too long. *depends on step 6*

8. **Update the closing section** with skills takeaways and a quick checklist for "what to skill-ify next." *depends on steps 2–7*

## Relevant Files

- `AI-agent-hands-on-tutorial/Multi_Agent_Deep_Research_Assistant.ipynb` — reference structure, tools, and agent setup to clone into the new Session 4 notebook.
- `AI-agent-hands-on-tutorial/README.md` — optional update to list the new Session 4 notebook if you want it linked in the series.

## Verification

1. Run the baseline cell and confirm it completes with a scoreboard row.
2. Run the skilled cell and confirm validation/repair triggers when needed and budgets are enforced.
3. Run the results-only cell and confirm it prints the scoreboard without re-running the full swarm.

## Decisions

- **Notebook-only delivery**; no separate scripts.
- **Comparative study** includes baseline vs skills plus a scoreboard.
- **Live portion is constrained**, with a results-only fallback for long runs.
- **New notebook name**: `Agent_Skills_Baseline_vs_Skilled.ipynb`
- **README update**: yes — link the new Session 4 notebook in the series.
- **Task theme**: general productivity (not meetup-specific).
- **Scoreboard metric focus**: citations (presence and correctness).
- **Cache strategy**: per-demo folder (fresh cache for each run, avoids stale artifacts).

## Estimated Timeline

- Steps 1–2: 15–20 min (setup + intro)
- Steps 3–4: 30–40 min (skill contracts + budgets + caching)
- Step 5: 20–25 min (scoreboard implementation)
- Step 6: 15–20 min (two runnable cells + integration)
- Step 7: 10–15 min (results-only fallback)
- Step 8: 10 min (closing updates)

**Total**: ~120–155 minutes (~2–2.5 hours)

## Implementation Readiness

All decisions locked. Proceed with:
1. Creating `Agent_Skills_Baseline_vs_Skilled.ipynb` in the tutorial folder.
2. Updating `README.md` to add Session 4 description.
3. Implementing steps 1–8 in the notebook.
