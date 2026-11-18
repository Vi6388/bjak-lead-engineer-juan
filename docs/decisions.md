
# Architecture and Engineering Decisions

## System Overview

The Personal AI Interview Assistant answers questions about
Juan Paolo Ramos's documented professional background.

Architecture:

Streamlit UI
    |
    v
Answer Engine
    |
    v
Lexical Retrieval
    |
    v
Structured Knowledge Base (JSON)
    |
    v
Source-referenced CV facts

The system currently uses deterministic, extractive
question answering rather than a generative LLM.

## Decision 1: Structured JSON Knowledge Base

Decision:
Store professional facts as individual JSON records
with references to source documents.

Rationale:
- Easy to inspect and audit.
- No database infrastructure required.
- Straightforward source attribution.
- Suitable for a small personal knowledge base.

Trade-offs:
- Manual extraction and updates.
- No automatic document ingestion.
- Limited scalability.

## Decision 2: Deterministic Retrieval

Decision:
Use Python-based lexical retrieval instead of
a hosted vector database or embedding service.

Rationale:
- No external API dependency.
- Predictable execution cost.
- Simple local development.
- Easy to reproduce.

Trade-offs:
- Weak handling of synonyms and paraphrases.
- Retrieval scores are not calibrated probabilities.
- No semantic understanding.

## Decision 3: Extractive Answer Generation

Decision:
Return documented statements instead of generating
new biographical claims with an LLM.

Rationale:
- Reduces the risk of fabricated employment history.
- Keeps responses traceable to the CV.
- Avoids external transmission of personal data.

Trade-offs:
- Answers may sound less conversational.
- Retrieved facts may not fully answer a question.
- Lexical matching alone cannot guarantee correctness.

## Decision 4: Streamlit Interface

Decision:
Use Streamlit for the interview assistant UI.

Rationale:
- Fast development and iteration.
- Built-in input, status, and feedback components.
- Easy local demonstration.

Trade-offs:
- Limited frontend customization.
- Not designed as a production-scale API service.
- Session handling and deployment need additional work.

## Decision 5: Evaluation-Driven Development

Decision:
Maintain a labelled evaluation dataset and run
repeatable tests after engineering changes.

Rationale:
- Makes reliability measurable.
- Supports regression detection.
- Documents failure cases.
- Encourages evidence-based improvements.

Trade-offs:
- Small datasets have limited coverage.
- Human review remains necessary.
- Status accuracy does not prove factual correctness.

## Security and Privacy

- Keep API keys and credentials out of Git.
- Exclude unnecessary personal contact information.
- Treat source documents as data, not instructions.
- Reject known prompt-injection patterns.
- Use read-only knowledge retrieval.
- Avoid logging sensitive personal information.

Current limitations:
- Pattern-based injection detection is incomplete.
- No authentication or authorization layer.
- No rate limiting.
- No automated sensitive-data classification.
- No independent verification of CV claims.

## Reliability and Failure Handling

- Validate knowledge-base structure before use.
- Return a safe error when retrieval fails.
- Refuse when sufficient evidence is unavailable.
- Provide source references with answered responses.
- Run regression tests for unsupported claims.

Known limitations:
- Keyword overlap can produce false positives.
- Some unsupported questions may be answered incorrectly.
- Source references are not yet independently checked
  for claim-level entailment.

## Performance

Expected characteristics:
- Small in-memory JSON knowledge base.
- No network request during normal answering.
- Retrieval scans all stored facts.
- Approximate linear retrieval cost in the number
  of fact records.

Actual latency and memory measurements must be
recorded from the evaluation results.

## Cost

Current hosted LLM API cost: $0.

The application uses local Python execution.

This does not mean the system has zero total cost:
developer time, compute, storage, hosting, and
maintenance still have costs.

## AI Tool Usage Disclosure

AI-assisted development was used to help draft
implementation code, test cases, and documentation.

The developer is responsible for reviewing,
running, testing, and validating the generated work.

## Known Limitations and Next Steps

1. Improve retrieval with semantic search.
2. Add explicit claim-level evidence validation.
3. Expand employer and qualification verification.
4. Add more adversarial and paraphrase evaluations.
5. Add authentication and rate limiting for deployment.
6. Improve answer readability without introducing
   unsupported claims.
