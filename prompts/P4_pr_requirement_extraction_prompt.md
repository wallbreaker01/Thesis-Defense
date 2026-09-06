# P4 — PR Requirement Field Extraction

**Paper reference:** Section 3 (Method) → "PR Analysis" / "FAISS-Based Similarity Retrieval" — corresponds to **Listing 5** (`lst:prompt-pr-analysis`) in the manuscript.

**Context (from the paper):** When a new PR is submitted, the pipeline converts it to a text summary and analyzes it with an LLM to extract technical skill requirements, expertise domains, complexity level, and review focus areas. This is combined with historical FAISS-retrieved similar PRs and structured skill metrics from developer profiles to generate a well-informed reviewer recommendation.

**Model configuration:** `mistralai/ministral-8b-2512`, temperature 0.1, max tokens 4,000, served via OpenRouter.

## Prompt

```
Extract these fields:
- technical_skills_needed: concrete technologies, libraries, languages, or APIs required to review this PR
- review_expertise_areas_needed: review domains such as backend, testing, security, performance, docs, release, architecture
- complexity_level: Low, Medium, or High based on scope, risk, and implementation depth
- review_focus_areas: the exact aspects a reviewer should inspect
- primary_language: the main implementation language, or Unknown if not clear
- frameworks_involved: only frameworks/libraries clearly present in the PR
- review_type_needed: the single best review type from Code Quality, Security, Performance, Documentation, Architecture, or Testing
```

**Note:** This prompt is used together with [P5](P5_json_output_format_prompt.md), which specifies the exact JSON output shape for these fields.
