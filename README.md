
# Personal Professional Interview Assistant

### BJAK Engineering Manager / Lead Engineer Practical Assessment

**Candidate:** Juan Paolo Ramos  
**Repository:** https://github.com/Vi6388/bjak-lead-engineer-juan  
**Language:** Python  
**Interface:** Streamlit  
**Architecture:** Source-grounded, deterministic question answering

---

## 1. Project Overview

This project is a personal professional interview assistant developed for the BJAK Engineering Manager / Lead Engineer practical assessment.

The application answers questions about my documented professional experience, technical skills, employment history, and engineering projects.

Its primary objective is to provide accurate, traceable answers without fabricating professional qualifications, employment history, achievements, or project experience.

The system uses a structured knowledge base derived from my professional CV, lexical information retrieval, and deterministic extractive answer generation.

**Important architectural distinction:** The current implementation does not use a generative Large Language Model at runtime. It is a source-grounded question-answering prototype developed with AI-assisted coding.

### Key Features

- Source-grounded professional question answering
- Structured CV knowledge base
- Source references and citation display
- Lexical retrieval and relevance ranking
- Evidence-based refusal for unsupported questions
- Handling of ambiguous questions
- Basic prompt-injection detection
- Multi-employer evidence retrieval
- Automated reliability evaluation
- Regression testing
- Local performance benchmarking
- No paid AI API dependency

---

## 2. Technology Stack

| Component | Technology |
|-----------|------------|
| Programming language | Python |
| User interface | Streamlit |
| Knowledge storage | JSON |
| Retrieval | Custom lexical retrieval |
| Answer generation | Deterministic extractive QA |
| Testing | pytest |
| Evaluation | Custom Python evaluation runner |
| Benchmarking | Python time.perf_counter |
| Version control | Git and GitHub |

The application runs locally without requiring OpenAI API keys, hosted LLM services, or a vector database.

---

## 3. System Architecture

The application follows a modular architecture.

```text
                  User / Interviewer
                          |
                          v
                  Streamlit Interface
                       app.py
                          |
                          v
                     Answer Engine
                   answer_engine.py
                          |
                +---------+---------+
                |                   |
                v                   v
         Input Validation     Answer Policies
                |             - Refusal
                |             - Ambiguity
                |             - Injection checks
                |             - Employer checks
                |                   |
                +---------+---------+
                          |
                          v
                    Retrieval Engine
                      retrieval.py
                          |
                          v
                   Knowledge Loader
                     knowledge.py
                          |
                          v
                  Structured Knowledge
                  data/knowledge.json
                          |
                          v
                  Source References
                     data/sources/
                          |
                          v
                  Extractive Response
                    With Citations
```

### Component Responsibilities

**app.py**

Provides the Streamlit user interface, accepts interview questions, and displays answers and supporting citations.

**answer_engine.py**

Controls input validation, ambiguity handling, employer verification, evidence selection, unsupported-question refusal, and answer assembly.

**retrieval.py**

Tokenizes questions, performs lexical matching, and ranks documented professional facts.

**knowledge.py**

Loads the knowledge base and validates its structure and source references.

**data/knowledge.json**

Stores structured professional facts, source metadata, and documented conflicts or gaps.

**evaluate.py**

Executes the labelled evaluation dataset and records accuracy, refusal behavior, citations, and latency.

**benchmark.py**

Measures local answer-engine response latency.

**tests/**

Contains automated unit and regression tests.

Additional architecture documentation is available in `docs/architecture.md`.

---

## 4. Knowledge Base and Source Provenance

The knowledge base is derived from my professional CV.

Its purpose is to ensure that answers are grounded in documented information rather than generated assumptions.

### Knowledge Structure

The knowledge base contains three primary collections:

```json
{
  "schema_version": "1.0",
  "sources": [],
  "facts": [],
  "conflicts": []
}
```

### Sources

Each source record identifies a supporting document or document section.

Source metadata may include:

- Unique source ID
- Document title
- Source type
- File path
- Page number
- Source status

### Facts

Each professional fact includes its supporting source references.

This enables the answer engine to associate returned statements with the documents from which they were extracted.

### Conflicts and Missing Information

The knowledge structure supports recording incomplete, conflicting, or insufficiently verified information.

The assistant should not infer missing employment dates, credentials, management responsibilities, or achievements.

The current implementation does not fully enforce every conflict policy during answer generation. This remains a known limitation.

### Privacy

The structured knowledge base is intended to exclude unnecessary personal contact information.

Before publishing or distributing the repository, the supporting CV must be checked for sensitive information.

The source file referenced by the knowledge base must also be available to reviewers if source verification is expected.

---

## 5. Question Answering Workflow

The assistant processes questions through the following stages.

### Stage 1: Input Validation

The application verifies that the user has submitted a nonempty question.

Invalid inputs receive a safe response.

### Stage 2: Safety and Ambiguity Checks

The answer engine checks for known prompt-injection patterns and selected ambiguous questions.

These checks are rule-based and do not provide comprehensive protection against every adversarial input.

### Stage 3: Employer Verification

Explicit employment questions are checked against the documented employer list.

Questions about collaboration with stakeholders are not treated as employment-verification requests.

### Stage 4: Knowledge Retrieval

The retrieval engine searches documented professional facts using lexical matching.

Some question categories use additional evidence-selection rules.

These include:

- Testing tools
- Security controls
- System integrations
- Backend services
- Multi-employer comparisons

### Stage 5: Evidence Selection

The answer engine selects retrieved facts according to relevance and evidence requirements.

For supported multi-employer questions, the system attempts to retrieve relevant evidence for each employer independently.

### Stage 6: Response Generation

The system returns documented statements rather than generating new professional claims.

A supported response includes source citations.

When sufficient evidence is unavailable, the assistant returns an unsupported response.

### Stage 7: Failure Handling

Knowledge-loading or retrieval errors return a generic service error instead of exposing internal implementation details.

---

## 6. Installation and Local Setup

### Prerequisites

- Python
- Git
- Windows CMD, PowerShell, or a compatible terminal

The project was developed locally using Python 3.15. Dependency compatibility should be confirmed on the target installation environment.

### Step 1: Clone the Repository

```bash
git clone https://github.com/Vi6388/bjak-lead-engineer-juan.git
cd bjak-lead-engineer-juan
```

### Step 2: Create a Virtual Environment

Windows CMD:

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

### Step 3: Install Dependencies

```cmd
python -m pip install -r requirements.txt
```

### Step 4: Validate the Knowledge Base

```cmd
python knowledge.py
```

### Step 5: Start the Application

```cmd
python -m streamlit run app.py
```

Open the local application at:

http://localhost:8501

No hosted LLM API key is required.

---

## 7. Example Questions

The assistant supports questions about documented professional experience.

Examples include:

```text
What is your experience with React?

What testing tools have you used?

How did you use security controls at Chewy
and Nature's Path Foods?

How did you work with stakeholders at
Chewy and Drawboard?

Compare the integrations at Chewy
and Nature's Path Foods.

How did you use backend services at
Chewy and Nature's Path Foods?
```

### Unsupported Question Example

```text
Have you built quantum astrophysics software?
```

Expected behavior:

```text
I cannot verify that information from the
available professional sources.
```

The assistant must not use unrelated software-development experience as evidence for an unsupported technical claim.

---

## 8. Evaluation and Reliability Testing

Reliability is a major focus of this assessment.

The project includes a labelled evaluation dataset containing 26 questions.

### Evaluation Categories

| Category | Number of Cases |
|----------|----------------:|
| Direct CV questions | 8 |
| Multi-source questions | 4 |
| Ambiguous questions | 4 |
| Unanswerable questions | 5 |
| Adversarial questions | 5 |
| **Total** | **26** |

The multi-source category includes questions requiring information from multiple employer-related facts. The current primary evidence source is one CV, so these tests do not establish independent cross-document corroboration.

### Run the Evaluation

```cmd
python evaluate.py
```

Evaluation results are saved to:

```text
evaluation/results.json
```

### Final Local Evaluation Results

The latest completed local evaluation produced:

| Metric | Result |
|--------|-------:|
| Total evaluation cases | 26 |
| Passed cases | 26 |
| Failed cases | 0 |
| Full-case pass rate | 100% |
| Status accuracy | 100% |
| Citation presence | 100% |
| Extractive-format proxy | 100% |
| Refusal correctness | 100% |
| Prohibited-claim check rate | 100% |
| p95 evaluation latency | 3.60 ms |

These results were measured during local execution on November 18, 2026.

The project-defined status accuracy threshold is 85%.

The latest evaluation exceeded this threshold.

**Evaluation scope:** These measurements describe performance against the current 26-question dataset. They do not establish perfect factual accuracy, robustness against all adversarial questions, or generalization to unseen questions.

The citation-presence metric measures whether citations are returned where expected. It does not independently prove that each citation supports every claim.

---

## 9. Evaluation Improvements

The initial evaluation identified seven failing cases.

### Baseline

| Metric | Result |
|--------|-------:|
| Total cases | 26 |
| Passed | 19 |
| Failed | 7 |
| Full-case pass rate | 73.08% |

### Final Local Evaluation

| Metric | Result |
|--------|-------:|
| Total cases | 26 |
| Passed | 26 |
| Failed | 0 |
| Full-case pass rate | 100% |

### Improvement

The evaluation pass rate increased by 26.92 percentage points.

The improvements focused on retrieval relevance, refusal behavior, employer detection, and multi-source evidence selection.

### Failure E21: Unsupported Technical Experience

**Question:**

Have you built quantum astrophysics software?

**Original problem:**

The assistant returned unrelated software-development experience as if it supported the question.

**Root cause:**

Generic terms such as "built" and "software" contributed to lexical relevance scoring.

**Fix:**

Reduced the influence of generic software-development terminology in retrieval.

**Final result:**

Passed. The assistant returned an unsupported response.

### Failure E10: Incorrect Employer Detection

**Question:**

How did you work with stakeholders at Chewy and Drawboard?

**Original problem:**

The employer-verification logic incorrectly interpreted collaboration terminology as an employment claim.

**Root cause:**

The employment-detection pattern included the preposition "with".

**Fix:**

Restricted the employer-verification rule to more explicit employment phrasing.

**Final result:**

Passed.

### Failure E08: Testing Tools Retrieval

**Question:**

What testing tools have you used?

**Original problem:**

The assistant refused despite documented testing experience.

**Root cause:**

Broad testing terminology did not sufficiently overlap with the names of specific testing tools.

**Fix:**

Added evidence retrieval for documented testing technologies, including pytest, Jest, and Playwright.

**Final result:**

Passed.

### Failure E09: Security Across Employers

**Original problem:**

The answer included security information from Nature's Path Foods but omitted Chewy.

**Fix:**

Added employer-specific security evidence retrieval.

**Final result:**

Passed.

### Failure E11: Integration Comparison

**Original problem:**

Relevant integration facts were excluded by the generic lexical coverage requirement.

**Fix:**

Added integration-specific evidence retrieval for each requested employer.

**Final result:**

Passed.

### Failure E12: Backend Services Comparison

**Original problem:**

The assistant could not retrieve sufficient backend-service evidence for both requested employers.

**Fix:**

Added employer-specific backend evidence retrieval.

**Final result:**

Passed.

Further details are documented in:

```text
docs/evaluation_analysis.md
```

---

## 10. Automated Testing

The project uses pytest for unit and regression testing.

### Run All Tests

```cmd
python -m pytest tests/ -v
```

### Run Reliability Tests

```cmd
python -m pytest tests/test_reliability.py -v
```

Regression tests cover scenarios such as:

- Invalid input
- Supported professional experience
- Unknown employers
- Unsupported technical claims
- Prompt-injection attempts
- Testing-tool questions
- Multi-employer evidence retrieval
- Citation presence

The complete test suite should be executed after each significant change.

A passing evaluation dataset is not a substitute for broader unit, integration, and adversarial testing.

---

## 11. Performance and Cost

### Local Evaluation Latency

The final 26-question local evaluation reported:

```text
p95 latency: 3.60 ms
```

This measures local answer-engine execution during the evaluation.

It does not include browser rendering, deployment network latency, or concurrent production traffic.

### Performance Benchmark

Run:

```cmd
python benchmark.py
```

Benchmark results are written to:

```text
evaluation/benchmark_results.json
```

The standalone benchmark measures repeated local question-answer calls.

### Computational Complexity

The retrieval engine scans the structured fact collection.

For a small knowledge base, this approach is simple and inexpensive.

However, retrieval work grows with the number and size of stored facts.

### Cost Model

| Component | Cost Consideration |
|-----------|-------------------|
| Hosted LLM API | $0 per request |
| Vector database | Not required |
| Local execution | Local CPU and memory |
| Storage | Small JSON knowledge base |
| Hosting | Depends on deployment |
| Maintenance | Developer effort required |

The prototype does not incur hosted LLM inference charges.

This does not imply zero total operational cost.

### Scaling Considerations

At significantly higher traffic, potential improvements include:

- Caching validated knowledge
- Avoiding repeated JSON parsing
- Building an indexed retrieval layer
- Introducing a dedicated backend API
- Adding request concurrency controls
- Measuring throughput and memory usage
- Adding monitoring and observability

No production-scale throughput claims are made for the current prototype.

---

## 12. Engineering Decisions and Trade-offs

### Decision 1: Structured JSON Instead of a Database

**Reason:**

The dataset is small, structured, and relatively static.

**Advantages:**

- Easy to audit
- Simple deployment
- Low infrastructure overhead
- Direct source references

**Trade-offs:**

- Manual updates
- Limited scalability
- No built-in concurrent editing

### Decision 2: Deterministic Retrieval Instead of Runtime LLM Generation

**Reason:**

The assessment emphasizes trustworthy answers about real professional experience.

**Advantages:**

- No hosted inference dependency
- Predictable local execution
- Extractive response generation
- Easier reproducibility

**Trade-offs:**

- Limited paraphrase understanding
- Less conversational responses
- Keyword-based relevance errors

### Decision 3: Explicit Evidence-Based Refusal

**Reason:**

Unsupported professional claims can misrepresent a candidate's qualifications.

**Advantages:**

- Reduces unsupported answers
- Encourages source traceability
- Provides predictable refusal behavior

**Trade-offs:**

- May reject legitimate paraphrased questions
- Requires careful threshold tuning

### Decision 4: Streamlit Interface

**Reason:**

Streamlit provides a practical interface for a time-boxed engineering prototype.

**Advantages:**

- Rapid development
- Minimal frontend infrastructure
- Easy local demonstration

**Trade-offs:**

- Limited UI customization
- No dedicated production API
- Additional deployment controls required

### Decision 5: Evaluation-Driven Iteration

**Reason:**

Reliability improvements should be supported by repeatable tests.

**Advantages:**

- Detects regressions
- Measures changes objectively
- Documents observed failures
- Supports technical review

**Trade-offs:**

- Evaluation coverage is limited
- Passing known cases does not guarantee generalization
- Human factual review remains necessary

See `docs/decisions.md` for further architectural discussion.

---

## 13. Security and Privacy

The application follows a conservative approach to professional information.

### Implemented Controls

- Structured knowledge validation
- Read-only fact retrieval
- Source references
- Input validation
- Unsupported-question refusal
- Basic prompt-injection pattern detection
- Generic internal error messages
- No runtime transmission of CV data to a hosted LLM

### Known Security Limitations

- No user authentication
- No rate limiting
- No production authorization layer
- No comprehensive prompt-injection defense
- No automatic sensitive-data classification
- No independent source-truth verification
- No security penetration testing

The current application is a local assessment prototype, not a production-hardened service.

### Secret Management

The repository should not contain:

- API keys
- Access tokens
- Passwords
- Private credentials
- Unnecessary personal contact information

No environment variables are required for hosted AI inference in the current implementation.

---

## 14. Reliability Limitations

Although the current evaluation passes all 26 cases, several limitations remain.

### Lexical Retrieval

The system does not fully understand semantic relationships or paraphrases.

### Evidence Validation

A matching keyword does not prove that a retrieved statement answers a question.

### Domain-Specific Rules

Specialized retrieval logic for security, integration, backend, and testing questions may not generalize to new domains.

### Multi-Source Reasoning

The system selects multiple facts but does not perform full semantic reasoning across independent documents.

### Source Verification

Professional facts originate from the supplied CV.

The system does not independently verify employment or qualifications against external records.

### Adversarial Robustness

Pattern-based protections cover only a limited set of attacks.

### Evaluation Coverage

The evaluation contains 26 questions.

Additional unseen questions, paraphrases, contradictions, and adversarial cases are needed to assess generalization.

---

## 15. Future Improvements

The next development priorities are:

1. Add claim-level evidence validation.
2. Improve paraphrase handling with semantic retrieval.
3. Expand evaluation with unseen questions.
4. Add stronger contradiction and ambiguity handling.
5. Support automatic document ingestion.
6. Add authentication and rate limiting.
7. Introduce production observability.
8. Evaluate a constrained LLM answer-generation layer with explicit citation verification.

Any generative answer layer should be prevented from presenting unsupported professional claims as facts.

---

## 16. AI-Assisted Development Disclosure

AI assistance was used during development to help draft:

- Python implementation code
- Retrieval and answer-selection logic
- Unit and regression tests
- Evaluation approaches
- Architecture documentation
- Reliability analysis
- README documentation

The development process included local execution, debugging, iterative changes, and evaluation against the labelled question dataset.

The developer remains responsible for reviewing the implementation, validating professional facts, and verifying the final submitted repository.

The runtime system itself does not currently use a generative LLM.

---

## 17. Scope and Time Management

The implementation prioritizes:

- Source-grounded answers
- Safe refusal behavior
- Explainable architecture
- Repeatable evaluation
- Minimal runtime dependencies
- A functional demonstration interface

The following capabilities were deferred:

- Hosted LLM integration
- Vector database infrastructure
- Automated document ingestion
- Multi-user authentication
- Production deployment
- Advanced observability

**Development time:** Record the actual time spent in the final submission notes. Do not represent the project as completed within the suggested 120-minute time box unless that is accurate.

**Reuse disclosure:** Record any starter code, previous project components, templates, or third-party assets used beyond the dependencies and AI-assisted development already described.

---

## 18. Engineering Self-Review

If this project were submitted for production code review, two changes would receive the highest priority.

### Review Change 1: Stronger Evidence Validation

The current system uses lexical relevance and domain-specific evidence rules.

I would introduce a claim-level validation layer that checks whether each returned statement is actually supported by the cited source and relevant to the user's question.

This would address the risk of irrelevant facts being returned as valid answers.

### Review Change 2: Broader Reliability Testing

I would expand the evaluation suite with:

- Unseen paraphrases
- Contradictory sources
- Missing evidence
- Partial employer coverage
- Prompt-injection variations
- Malformed source records
- Performance and concurrency tests

This would improve confidence beyond the current fixed evaluation dataset.

---

## 19. Repository Structure

```text
bjak-lead-engineer-juan/
|
|-- app.py
|-- answer_engine.py
|-- retrieval.py
|-- knowledge.py
|-- evaluate.py
|-- benchmark.py
|-- requirements.txt
|-- README.md
|-- .gitignore
|
|-- data/
|   |-- knowledge.json
|   |-- sources/
|       |-- README.md
|
|-- evaluation/
|   |-- questions.json
|   |-- results.json
|   |-- benchmark_results.json
|
|-- tests/
|   |-- test_knowledge.py
|   |-- test_reliability.py
|
|-- docs/
|   |-- architecture.md
|   |-- decisions.md
|   |-- evaluation_analysis.md
```

Additional files may be present depending on the final committed implementation.

---

## 20. Reproducing the Results

From the repository root:

```cmd
python knowledge.py
python -m pytest tests/ -v
python evaluate.py
python benchmark.py
python -m streamlit run app.py
```

The expected local evaluation result for the final tested implementation is:

```text
SUMMARY
total: 26
passed: 26
full_case_pass_rate: 1.0
status_accuracy: 1.0
citation_presence: 1.0
extractive_format_proxy: 1.0
refusal_correctness: 1.0
prohibited_claim_check_rate: 1.0
p95_latency_ms: 3.6
pass_bar_status_accuracy: 0.85
meets_status_accuracy_bar: True
```

Exact latency values may vary by environment.

The full regression suite and evaluation should be rerun after cloning the repository.

---

## 21. Submission

**Repository:**

https://github.com/Vi6388/bjak-lead-engineer-juan

The repository contains the implementation, evaluation framework, documentation, and source-grounded knowledge representation.

Before submission, the final commit should be checked for:

- Complete and accurate source references
- Reproducible installation
- Passing regression tests
- Updated evaluation outputs
- Accurate engineering disclosures
- No exposed secrets or unnecessary personal data

If the repository is private, access must be granted to the designated BJAK reviewer.

---

## 22. Conclusion

This assessment demonstrates an engineering approach centered on reliability, traceability, and controlled answer generation.

The prototype combines structured professional knowledge, deterministic retrieval, source citations, and repeatable evaluation.

The local evaluation improved from 19/26 passing cases to 26/26 through iterative debugging and regression testing.

The main engineering lesson is that a successful question-answering system requires more than producing plausible responses. It must also identify insufficient evidence, handle unsupported questions safely, and make its limitations explicit.

The current implementation provides a foundation for further development, while remaining transparent about its non-generative architecture and limited evaluation coverage.
