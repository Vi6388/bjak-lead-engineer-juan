
# BJAK Evaluation and Reliability Analysis

## 1. Evaluation Overview

The Personal Professional Interview Assistant uses
a structured CV knowledge base, lexical retrieval,
and deterministic extractive question answering.

Every returned professional fact must have a
reference to a documented source.

The application does not currently use a
generative LLM for answer generation.

## 2. Evaluation Dataset

Total questions: 26

Categories:
- CV-direct questions
- Multi-source questions
- Ambiguous questions
- Unanswerable questions
- Adversarial questions

Evaluation command:

    python evaluate.py

Regression test command:

    python -m pytest tests/ -v

## 3. Baseline Results

Original observed results:

Total questions: 26
Passed: 19
Failed: 7
Pass rate: 73.08%

Original failed cases:

- E03
- E08
- E09
- E10
- E11
- E12
- E21

These failures were identified through the
automated evaluation dataset.

## 4. Verified Improvements

After successive local fixes, the observed
evaluation improved to:

Total questions: 26
Passed: 23
Failed: 3
Pass rate: 88.46%

Remaining failures at that point:

- E09
- E11
- E12

This is the most recent verified result before
the new E09 changes.

## 5. Failure E21 — Unsupported Domain Question

Question:
Have you built quantum astrophysics software?

Expected:
unsupported

Original observed:
answered

Root cause:
The lexical retrieval system matched generic
software-development terminology and returned
an unrelated price-management fact.

Implemented fix:
Removed generic terms such as "built" and
"software" from retrieval matching.

Verification:
E21 passed in the subsequent local evaluation.

Remaining limitation:
Stop-word filtering is not a semantic
entailment mechanism.

## 6. Failure E10 — Employer Detection

Question:
How did you work with stakeholders at Chewy
and Drawboard?

Expected:
answered

Original observed:
unsupported

Root cause:
The employer-verification regex treated
"worked with" as employment verification.

Implemented fix:
Removed "with" from the employer-verification
preposition alternatives.

Verification:
E10 passed in the subsequent local evaluation.

Remaining limitation:
Employer detection is rule-based and does not
cover every possible phrasing.

## 7. Failure E08 — Testing Tools

Question:
What testing tools have you used?

Expected:
answered

Original observed:
unsupported

Root cause:
Generic testing terminology did not sufficiently
overlap with the documented names of testing
technologies.

Implemented fix:
Added a focused retrieval strategy for
documented testing tools, including pytest,
Jest, and Playwright.

Verification:
E08 passed in the subsequent local evaluation.

Remaining limitation:
The approach uses domain-specific rules rather
than general semantic search.

## 8. Failure E09 — Multi-Employer Security

Question:
How did you use security controls at Chewy
and Nature's Path Foods?

Expected:
An answer covering security-related evidence
from both employers.

Original observed:
answered, but incomplete

Observed answer:
The assistant returned Nature's Path Foods
integration and authentication facts but
omitted Chewy.

Root cause:
The retrieval engine ranked facts globally.
The answer engine selected the top-ranked
results without guaranteeing relevant
coverage of both requested employers.

Proposed implementation:
- Detect explicitly mentioned employers.
- Search security evidence for each employer.
- Require relevant facts from both employers.
- Preserve source citations.
- Refuse rather than fabricate missing evidence.

Regression tests:
- Both employer names must appear.
- Relevant security evidence must appear.
- Straight and curly apostrophes must work.
- Citations must be returned.

Retest result:
PENDING — Run pytest and evaluate.py.

Remaining limitation:
Security relevance is determined using a
keyword-based heuristic, not semantic entailment.

## 9. Remaining Failures

E11:
Multi-source integration comparison.
Previously returned an incomplete answer.

E12:
Multi-source backend comparison.
Previously returned an incomplete answer.

Both require investigation using the actual
evaluation questions and returned evidence.

Do not mark these failures resolved until
their regression tests pass.

## 10. Reliability Safeguards

Current safeguards include:

- Structured knowledge-base validation
- Source-linked professional facts
- Extractive answer generation
- Unsupported-question refusal
- Input validation
- Basic prompt-injection detection
- Employer-verification rules
- Automated regression tests

## 11. Known Limitations

- Lexical retrieval can miss paraphrases.
- Keyword overlap does not prove factual support.
- Employer detection is incomplete.
- Domain-specific query rules do not generalize.
- The system does not independently verify
  claims against employer records.
- Source citations require a committed,
  accessible copy of the supporting CV.
- No production authentication or rate limiting.
- No generative LLM is currently used.

## 12. Performance and Cost

Benchmark command:

    python benchmark.py

The application performs local deterministic
retrieval without hosted LLM API calls.

Hosted LLM API cost: $0.

Actual latency and benchmark metrics should
be copied from evaluation/benchmark_results.json.

Total operating cost is not zero because local
compute, development, hosting, and maintenance
still require resources.

## 13. AI-Assisted Development Disclosure

AI assistance was used to draft code,
tests, evaluation approaches, and documentation.

Generated changes must be reviewed and validated
through local execution before submission.

## 14. Final Verification

Before submission:

- Run all regression tests.
- Run the complete 26-question evaluation.
- Inspect every failed case.
- Confirm no unsupported claims.
- Confirm all answered cases have citations.
- Verify the redacted CV source is available.
- Record final evaluation and benchmark results.
- Review the GitHub repository for secrets.
- Complete the README and engineering decisions.

## E11 — Integration comparison across employers

Question:
Compare the integrations at Chewy and Nature's Path Foods.

Expected:
An evidence-grounded comparison covering both employers.

Observed:
unsupported

Root cause:
The multi-employer selector required at least 50% lexical
coverage for each employer, excluding relevant integration
facts that used different terminology.

Implemented change:
Added integration-specific evidence retrieval for each
requested employer, using documented integration terms.

Retest:
[Insert measured result]

Limitation:
Keyword matching remains a heuristic and does not
guarantee semantic relevance.

## E12 — Backend services across employers

Question:
How did you use backend services at Chewy and
Nature's Path Foods?

Expected:
An evidence-grounded answer covering both employers.

Observed baseline:
unsupported

Root cause:
The multi-employer selector required at least 50%
lexical coverage for each employer. Relevant backend
and service-integration facts were excluded.

Implemented change:
Added employer-specific backend evidence retrieval
using technologies documented in the CV.

Retest:
[Insert actual measured result]

Remaining limitation:
The solution uses keyword-based relevance checks,
not semantic entailment.