# P3 — Category & Frequency-Embedding Consistency Rules

**Paper reference:** Section 3 (Method) → "Profile Generation" — corresponds to **Listing 3** (`lst:prompt-consistency-rules`) in the manuscript.

**Context (from the paper):** Appended to the [P2](P2_structured_profile_prompt.md) profile-generation call to enforce consistency. It includes both positive constraints (correct formats) and negative constraints (common mistakes), particularly around category naming, frequency embedding, and skill selection — this significantly reduces parsing failures downstream.

**Model configuration:** `mistralai/ministral-8b-2512`, temperature 0.1, max tokens 4,000, served via OpenRouter.

## Prompt

```
Be specific and evidence-based in your JavaScript skill assessment. Map identified
skills to the appropriate categories, using evidence from PR titles, descriptions,
and file changes.

CATEGORY RULES:
- Only use the 17 exact predefined category names; DO NOT invent new categories or skills
- DO NOT use subcategory or individual skill names (e.g., "Testing Libraries", "Node.js") as category names
- Route testing skills (Jest, Mocha, etc.) under "Framework/Library Expertise"; route
  code-quality/linting skills under the existing category they best fit

FREQUENCY EMBEDDING RULES:
- For each non-empty category, embed the frequency count in BOTH the category name
  and each individual skill name
- Format: "Category Name, frequency: X": ["Skill Name, frequency: Y", ...]
- The category frequency is the SUM of its individual skill frequencies
- For categories with no skills, omit the frequency and use the category name alone
```
