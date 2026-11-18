
# System Architecture

```mermaid
flowchart TD
    A[Recruiter Question] --> B[Streamlit UI]
    B --> C[Answer Engine]
    C --> D{Input Validation}
    D -->|Invalid or Unsafe| E[Safe Response]
    D -->|Valid| F[Retrieval Engine]
    F --> G[Structured Knowledge Base]
    G --> H[Source-Referenced Facts]
    H --> F
    F --> I{Sufficient Match?}
    I -->|No| J[Refusal]
    I -->|Yes| K[Extractive Answer]
    K --> L[Source Citations]
    J --> B
    E --> B
    L --> B
```

## Component Responsibilities

- `app.py`: User interface and source display.
- `answer_engine.py`: Input checks, refusal, and answer assembly.
- `retrieval.py`: Lexical search and fact ranking.
- `knowledge.py`: JSON loading and schema validation.
- `data/knowledge.json`: Structured professional facts.
- `data/sources/`: Supporting source documents.
- `evaluate.py`: Automated evaluation.
- `tests/`: Unit and regression tests.
