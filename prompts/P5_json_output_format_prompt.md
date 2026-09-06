# P5 — PR Requirement JSON Output Format

**Paper reference:** Section 3 (Method) → "PR Analysis" / "FAISS-Based Similarity Retrieval" — corresponds to **Listing 6** (`lst:prompt-json-format`) in the manuscript.

**Context (from the paper):** Paired with [P4](P4_pr_requirement_extraction_prompt.md) to force the LLM's PR analysis into a structured JSON-formatted output. The system then parses this JSON response; if parsing fails, a fallback method analyzes the PR's programming language statistics and file naming patterns to infer technical requirements instead.

**Model configuration:** `mistralai/ministral-8b-2512`, temperature 0.1, max tokens 4,000, served via OpenRouter.

## Prompt

```
Provide your analysis in this exact JSON format:
{{"technical_skills_needed": ["skill1", "skill2", "skill3"],
"review_expertise_areas_needed": ["area1", "area2"],
"complexity_level": "Low/Medium/High",
"review_focus_areas": ["focus1", "focus2", "focus3"],
"primary_language": "JavaScript/Python/etc",
"frameworks_involved": ["framework1", "framework2"],
"review_type_needed": "Code Quality/Security/Performance/Documentation/Architecture"}}
```

**Note:** The doubled curly braces (`{{`, `}}`) are preserved verbatim from the source code's Python string template (they are the standard escape for a literal brace inside a `.format()`-style template) and resolve to single braces in the actual text sent to the model.
