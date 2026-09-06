# P1 — JavaScript Expertise Extraction from Pull Requests

**Paper reference:** Section 3 (Method) → "Skills analysis" — corresponds to **Listing 1** (`lst:prompt-skill-extraction`) in the manuscript.

**Context (from the paper):** A prompt-guided LLM processes simplified PR JSON data (title, repository context, labels, review-related signals, code change statistics, short description) and is specifically told to look for JavaScript-specific skills. The output of this stage is unstructured but semantically rich, providing an evidence-based narrative of each developer's capabilities.

**Model configuration:** `mistralai/ministral-8b-2512`, temperature 0.1, max tokens 4,000, served via OpenRouter (see "Model Configuration for LLM-Based Skill Extraction" table in the paper).

## Prompt

```
Focus specifically on JavaScript-related skills. Based on this PR data, identify:
1. JavaScript frameworks and libraries used (React, Vue, Angular, Node.js, etc.)
2. JavaScript programming patterns and paradigms
3. Frontend vs. backend JavaScript contributions
4. Testing frameworks and methodologies in JavaScript
5. Build tools and development workflow
6. JavaScript ES6+ features usage
7. TypeScript usage and proficiency
8. API development and consumption patterns
9. Asynchronous programming patterns
10. Code quality and modern JavaScript practices
Provide a detailed analysis focusing exclusively on JavaScript ecosystem skills and expertise.
Look for evidence in PR titles, descriptions, file changes, and technology stacks.
```
