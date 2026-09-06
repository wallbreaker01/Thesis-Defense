# P7 — Failed-Prediction Root Cause Analysis

**Paper reference:** Section 3 (Method) → "Evaluation Setup" / Validation Techniques — corresponds to **Listing 8** (`lst:prompt-failure-analysis`) in the manuscript.

**Context (from the paper):** For each failed prediction where no top-3 recommendation matches the actual assignment, this prompt drives an LLM-backed root-cause analysis to provide a contextual explanation for the mismatch, helping identify opportunities for improvement and revealing system limitations.

**Model configuration:** `mistralai/ministral-8b-2512`, temperature 0.1, max tokens 4,000, served via OpenRouter.

## Prompt

```
Based on the PR details above, provide a concise reason why the actual reviewer was better suited than the predicted ones. Focus on the most important factor only. Check the PR properly and avoid generic answers. Also distinguish between the actual and predicted reviewers.
```
