
# BJAK Evaluation and Reliability Analysis

## Evaluation Method

The assistant uses structured professional facts
extracted from a CV.

Retrieval uses token overlap and question coverage.

The answer engine returns extractive responses
with source references.

## Baseline Results

Evaluation date: [Enter date]
Total questions: 26
Status accuracy: [Measured value]
Refusal correctness: [Measured value]
Citation presence: [Measured value]
Latency p95: [Measured value]

## Failure 1

Question: [Actual failed question]

Expected behavior: [Expected result]

Observed behavior: [Actual result]

Root cause: [Explain the code-level cause]

Proposed or implemented fix: [Explain change]

Retest result: [Measured result]

## Failure 2

Question: [Actual failed question]

Expected behavior: [Expected result]

Observed behavior: [Actual result]

Root cause: [Explain the code-level cause]

Proposed or implemented fix: [Explain change]

Retest result: [Measured result]

## Known Limitations

- Lexical retrieval does not understand all paraphrases.
- Token coverage is not factual entailment.
- Employer recognition is rule-based and incomplete.
- CV claims have not been independently verified
  against employer records.
- Extractive answers may be less conversational
  than generative answers.

## Future Improvements

- Add semantic retrieval with local embeddings.
- Introduce claim-level verification.
- Expand adversarial regression testing.
- Add confidence calibration and clarification handling.
- Monitor retrieval and refusal errors over time.


## Failure E21 — Unsupported Domain Question

Question:
Have you built quantum astrophysics software?

Expected:
unsupported

Baseline observed:
answered

Baseline answer:
The assistant returned an unrelated price-management
software fact from Nature's Path Foods.

Root cause:
The lexical retrieval algorithm treated generic terms
such as "built" and "software" as relevant evidence.
The answer engine then accepted the result based on
token coverage, without checking whether the
distinctive technical domain was supported.

Implemented mitigation:
Excluded generic software-development action and
artifact terms from retrieval matching.

Regression tests:
- Unsupported quantum astrophysics question
- No irrelevant retrieval results
- Supported React experience remains answerable

Retest result:
[Enter actual result after running evaluation]

Remaining limitation:
Stop-word filtering is a heuristic. It does not
provide semantic entailment or comprehensive
protection against unrelated answers.

## E10 — Stakeholder collaboration misclassified

Expected: answered
Baseline observed: unsupported

Root cause:
The employer-detection regex included "with",
causing collaboration questions to be treated
as employment-verification questions.

Fix:
Restricted the employer-verification regex to
"at" and "for".

Retest:
[Insert measured result]

Remaining limitation:
Multi-employer retrieval may still omit one
of the employers requested.