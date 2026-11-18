# bjak-lead-engineer-juan# Personal Professional Interview Assistant — BJAK Assessment

A source-grounded, local interview assistant that answers questions about Juan Paolo Ramos's documented professional background. It uses a redacted CV, structured facts, lexical retrieval, and extractive answers. **It does not call a generative LLM at runtime.**

> **Submission status:** Draft. Replace all `TODO` entries with verified results before submitting.

## Quick start (Windows CMD)

Prerequisites: Python 3.15 and Git. From the repository root:

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python knowledge.py
python -m pytest tests/ -v
python -m streamlit run app.py
```

Open http://localhost:8501. No API key is required for the current implementation. If Python 3.15 dependency compatibility causes installation problems, document the tested Python version and update this section after validating it.

## System design

`app.py` (Streamlit) → `answer_engine.py` (validation, refusal, answer assembly) → `retrieval.py` (lexical fact ranking) → `knowledge.py` (schema checks) → `data/knowledge.json` (facts and source references).

The answer engine returns source-linked, extractive statements when its heuristic threshold is met, and otherwise returns a refusal or clarification. **A lexical match is not proof of entailment.** This is a known safety limitation, and claims must be checked against their cited source.

### Source collection and provenance

- Primary source: redacted two-page professional CV in `data/sources/Juan_Ramos_Full_Stack_Developer_redacted.pdf`.
- Structured facts: `data/knowledge.json`, with `source_ids` referencing the CV page records.
- Redactions: personal email address, phone number, and location are excluded from the structured knowledge base; inspect the redacted PDF before publishing.
- No synthetic work history is included.
- Source conflicts/gaps are represented in `conflicts`, including the absence of verified formal management scope and month-level employment dates. The current answer engine does **not** fully enforce these conflict policies; this is a documented limitation.
- Additional sources can be added by registering a unique `sources` record and linking new facts through `source_ids`; add tests and update the evaluation labels for the new evidence.

## Why this architecture

A small, auditable JSON knowledge base and deterministic retrieval were selected over a hosted LLM and vector database to keep setup, privacy exposure, and runtime cost low during the time box. The trade-off is limited paraphrase understanding and a risk of irrelevant extractive answers. See `docs/decisions.md` and `docs/architecture.md` for alternatives and design details.

### Failure handling and security

Invalid questions are rejected; missing evidence results in a refusal; a knowledge-loading failure returns a generic service error. Pattern-based injection checks are incomplete and must not be treated as a comprehensive prompt-injection defense. The app is a local demo, without production authentication, rate limiting, or a public-service threat model. No source data is sent to an LLM provider by the current runtime. Keep secrets out of Git and list all configurable environment variables in `.env.example` (or explicitly document that none are consumed).

### Cost and latency

- Hosted model/API charge per question: **$0** in the current implementation (no hosted model calls).
- Local compute and hosting: not zero; not separately priced.
- Measured p95 latency: **TODO — copy from `evaluation/benchmark_results.json` after running `python benchmark.py`**.
- Benchmark scope: local `answer_question()` calls only; excludes browser and network overhead.
- At 100× traffic, the single-process Streamlit deployment, per-request JSON reads and linear retrieval are likely bottlenecks; measure concurrency before making capacity claims.

## Evaluation

Run:

```cmd
python evaluate.py
python benchmark.py
python -m pytest tests/ -v
```

The labelled question set is `evaluation/questions.json` (26 questions, if using the supplied evaluation package). It should cover direct CV facts, multiple-source questions, ambiguity, unanswerable questions, and adversarial prompts. **The current source set is one CV with two pages, not two independent documents; do not claim cross-document validation.**

Results: **TODO — insert measured counts, accuracy, refusal correctness, citation presence, p95, and the date/environment of the run.** Commit `evaluation/results.json` and `evaluation/benchmark_results.json` only after executing the scripts.

Pass bar: **TODO — record the declared threshold and how each metric is computed, before reporting success.** If using the provisional threshold from development, state 85% status accuracy, with zero manually observed fabricated professional claims; these are project-defined thresholds, not BJAK's.

Failure analysis: **TODO — link two actual failed cases from `evaluation/results.json`, with expected/observed outputs, root cause, fix or proposed fix, and retest result.** See `docs/evaluation_analysis.md`. Do not report hypothetical failure modes as observed failures.

For a financial transaction use case, add claim-level provenance, high-severity negative tests, adversarial regression suites, human review of sampled decisions, audit trails, and continuous CI evaluation before deployment.

## Decisions, scope and AI usage

See `docs/decisions.md` for 3–5 decisions, rejected alternatives, security trade-offs, and next steps.

Time-box cuts: hosted LLM integration, embeddings/vector database, automated ingestion, multi-user authentication, and production deployment. Next priorities: (1) enforce claim-level evidence validation, (2) improve paraphrase handling, (3) expand adversarial and regression evaluation.

AI-assisted coding was used to draft code, tests, and documentation. **TODO — record which generated changes you actually reviewed, edited, and verified.** Do not let a model decide whether unsupported employment, credentials, or achievements are true.

Self-review — two requested PR changes: (1) replace heuristic support scoring with question-specific evidence validation; (2) strengthen tests around employer questions, contradictions, and prompt injection.

Actual hands-on time: **TODO — record your true time spent, including any overrun beyond the suggested 120 minutes.**

Reuse disclosure: **TODO — list any starter code, prior project, templates, or third-party assets actually used, or state 'none'.**

## Repository contents

- `app.py` — UI and visible citations/refusals
- `knowledge.py`, `data/knowledge.json`, `data/sources/` — knowledge and provenance
- `retrieval.py`, `answer_engine.py` — retrieval and response policy
- `evaluate.py`, `evaluation/` — labelled evaluation and measured results
- `benchmark.py` — local latency benchmark
- `tests/` — unit and regression tests
- `docs/` — architecture, decision record, and failure analysis

## Submission checklist

- [ ] Fresh clone installs and starts in under ten minutes
- [ ] Dependencies are pinned and `.env.example` is accurate
- [ ] Redacted source PDF and structured facts are committed
- [ ] Evaluation and benchmark have been run; actual outputs are committed
- [ ] Two observed failures are documented, or the lack of failures is transparently explained with additional challenge cases
- [ ] All TODOs are replaced with verified statements
- [ ] No keys, unnecessary personal information, or `.venv` committed
- [ ] Meaningful commits and `submission` tag pushed
- [ ] Repository URL and visibility sent to the BJAK assessment recipients
