
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
