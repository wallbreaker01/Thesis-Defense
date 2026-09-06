# LLM Prompts

This folder contains the exact LLM prompts used in Section 3 (Method) of the paper:

> **A Hybrid LLM and Frequency-Weighted Knowledge Unit-Based Approach for Pull Request Reviewer Recommendation: An Empirical Study on JavaScript Projects**

Due to page-length constraints, the manuscript prints an abbreviated form of these prompts in-text (with the full text noted as available here). This folder is the canonical, verbatim source referenced by the paper.

## Model configuration

All prompts below were run with the same base configuration (see "Model Configuration for LLM-Based Skill Extraction" table in the paper):

| Parameter | Value |
|---|---|
| Model | `mistralai/ministral-8b-2512` |
| Temperature | 0.1 |
| Max tokens | 4,000 |
| API provider | OpenRouter |

## Index

| ID | Prompt | Pipeline stage | Paper listing | File |
|----|--------|-----------------|----------------|------|
| P1 | JavaScript expertise extraction from PRs | Skills analysis | Listing 1 | [P1_skill_extraction_prompt.md](P1_skill_extraction_prompt.md) |
| P2 | Structured developer/reviewer profile generation | Profile generation | Listing 2 | [P2_structured_profile_prompt.md](P2_structured_profile_prompt.md) |
| P3 | Category & frequency-embedding consistency rules | Profile generation | Listing 3 | [P3_consistency_rules_prompt.md](P3_consistency_rules_prompt.md) |
| P4 | PR requirement field extraction | PR analysis | Listing 5 | [P4_pr_requirement_extraction_prompt.md](P4_pr_requirement_extraction_prompt.md) |
| P5 | PR requirement JSON output format | PR analysis | Listing 6 | [P5_json_output_format_prompt.md](P5_json_output_format_prompt.md) |
| P6 | Reviewer matching and ranking | Reviewer recommendation | Listing 7 | [P6_reviewer_matching_prompt.md](P6_reviewer_matching_prompt.md) |
| P7 | Failed-prediction root cause analysis | Evaluation | Listing 8 | [P7_failure_analysis_prompt.md](P7_failure_analysis_prompt.md) |

## Pipeline order

The prompts are applied in this order during a full run:

1. **P1** extracts an unstructured, evidence-based skills narrative from a developer's/reviewer's raw PR history.
2. **P2 + P3** turn that narrative into a structured, frequency-weighted JSON skill profile (used for both developers and reviewers).
3. When a new PR arrives, **P4 + P5** extract its structured technical requirements as JSON.
4. **P6** combines the PR requirements, all candidate reviewer profiles, and FAISS-retrieved similar past reviews to produce a ranked top-3 reviewer recommendation.
5. **P7** is run offline during evaluation, only on cases where the top-3 recommendation missed the actual assigned reviewer, to explain the mismatch.
