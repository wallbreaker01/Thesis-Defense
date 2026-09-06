# P6 — Reviewer Matching and Ranking

**Paper reference:** Section 3 (Method) → "FAISS-Based Similarity Retrieval" / Reviewer Recommendation Workflow — corresponds to **Listing 7** (`lst:prompt-reviewer-matching`) in the manuscript.

**Context (from the paper):** Combines the structured PR requirements (from [P4](P4_pr_requirement_extraction_prompt.md)/[P5](P5_json_output_format_prompt.md)), a summary of all reviewer profiles (from [P2](P2_structured_profile_prompt.md)/[P3](P3_consistency_rules_prompt.md)), and similar past PR reviews retrieved from the FAISS index. The model ranks the top-3 reviewers, treating frequency counts as the strongest signal of practical expertise. If the LLM output is unavailable, invalid, or unparseable, a deterministic frequency-weighted fallback scoring mechanism is used instead (see paper, Section 3).

**Model configuration:** `mistralai/ministral-8b-2512`, temperature 0.1, max tokens 4,000, served via OpenRouter.

## Prompt

```
Task: rank the best 3 reviewers for this PR using the provided requirements, reviewer profiles, and similar past reviews.
Hard rules:
- Use only reviewers that appear in AVAILABLE REVIEWERS.
- Base every claim on the provided profile data or similar review evidence.
- Treat frequency counts as the strongest signal of practical expertise.
- Prefer direct matches over general seniority.
- Penalize reviewers with weak or missing evidence for the required skills.
- Return JSON only. No markdown, no explanation, no code fences.
PR REQUIREMENTS: {pr_requirements}
AVAILABLE REVIEWERS: {reviewer_profiles}
SIMILAR PAST REVIEWS: {similar_reviews}
Scoring rubric:
- skill_frequency_match: 0.00 to 1.00, weight 0.45. Measures direct overlap between required skills/frameworks and reviewer frequency evidence.
- domain_alignment: 0.00 to 1.00, weight 0.20. Measures fit to the needed review type and expertise areas.
- similar_review_relevance: 0.00 to 1.00, weight 0.15. Measures match with retrieved similar PRs and review patterns.
- review_activity_consistency: 0.00 to 1.00, weight 0.10. Measures reviewer reliability from total reviews/comments/PRs reviewed.
- complexity_fit: 0.00 to 1.00, weight 0.10. Measures whether reviewer experience matches PR complexity.
Decision guidance:
- Rank by final weighted score, highest first.
- Use conservative scores when evidence is partial.
- If two reviewers are close, prefer the one with stronger frequency evidence and more similar-review matches.
- Make the reasoning short, factual, and specific.
- Provide exactly 3 reviewers.
Return exactly this JSON shape:
{{"recommended_reviewers": [{{
      "reviewer_name": "name",
      "match_score": 0.0,
      "reasoning": "short evidence-based explanation",
      "strengths_alignment": ["specific strength 1", "specific strength 2"],
      "review_experience": "short factual summary",
      "potential_concerns": "specific gap or None identified",
      "score_breakdown": {{
        "skill_frequency_match": 0.0,
        "domain_alignment": 0.0,
        "similar_review_relevance": 0.0,
        "review_activity_consistency": 0.0,
        "complexity_fit": 0.0}},
      "evidence": ["evidence 1", "evidence 2"]}}],
  "assignment_confidence": "High|Medium|Low",
  "assignment_reasoning": "one short sentence explaining the top choice",
  "ranking_notes": ["note 1", "note 2"]}}
```

**Note:** `{pr_requirements}`, `{reviewer_profiles}`, and `{similar_reviews}` are runtime template placeholders substituted with the actual PR analysis, candidate reviewer profiles, and FAISS-retrieved similar reviews before the prompt is sent to the model. Doubled curly braces (`{{`, `}}`) are the source code's escape for literal single braces in the JSON output shape.
