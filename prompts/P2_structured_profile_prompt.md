# P2 — Structured Developer/Reviewer Profile Generation

**Paper reference:** Section 3 (Method) → "Profile Generation" — corresponds to **Listing 2** (`lst:prompt-structured-profile`) in the manuscript.

**Context (from the paper):** A Python-based output parser turns the unstructured skills analysis (from [P1](P1_skill_extraction_prompt.md)) into a structured developer/reviewer profile. The structured profile has six parts: developer name, experience level, primary skills, programming languages, summary, and a JavaScript skill matrix. The identical prompt is used for both developer and reviewer profiles.

**Model configuration:** `mistralai/ministral-8b-2512`, temperature 0.1, max tokens 4,000, served via OpenRouter.

## Prompt

```
Generate a JavaScript developer profile that includes:
1. Experience level assessment (Junior/Mid/Senior/Lead) based on JavaScript contributions
2. Primary JavaScript technical skills and frameworks they show expertise
3. Overall JavaScript developer summary
4. Detailed skill matrix mapping to the provided JavaScript categories WITH EMBEDDED FREQUENCY
```

**Note:** This prompt is used together with a predefined list of 17 JavaScript skill-matrix categories and their valid skill/subdomain names (supplied as additional context to the LLM call, not shown here), which constrains the model to consistent terminology across profiles.
