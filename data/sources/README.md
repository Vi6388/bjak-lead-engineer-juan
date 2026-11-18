# Knowledge Sources

## Purpose

This directory contains the source materials used to build the Personal AI Interview Assistant's knowledge base.

The assistant is designed to answer questions about my professional background using verified information rather than generating unsupported claims.

## 1. Data Sources

The primary knowledge source is my professional CV/resume.

Additional sources may include:

- LinkedIn profile information
- GitHub repositories and project documentation
- Technical writing and engineering notes
- Verified project descriptions

Only sources explicitly included in the knowledge base are available to the assistant.

**Current status:** Source ingestion is not yet complete. The initial `knowledge.json` contains no professional facts.

## 2. Data Collection and Processing

The knowledge preparation process consists of:

1. Collecting professional documents.
2. Reviewing and removing unnecessary personal information.
3. Extracting relevant employment history, technical skills, projects, and engineering experience.
4. Structuring verified information into individual factual records.
5. Assigning unique source identifiers to each record.
6. Storing structured records in `data/knowledge.json`.

Each fact must reference at least one registered source.

## 3. Knowledge Storage

Structured information is stored in:

`data/knowledge.json`

The knowledge base contains three primary collections:

- `sources`: Information about the original documents.
- `facts`: Verified professional statements with source references.
- `conflicts`: Known inconsistencies, gaps, or outdated information.

The application uses `knowledge.py` to load and validate these records.

## 4. Source Traceability

Every factual record must contain a valid source reference.

When answering questions, the assistant should display the evidence supporting its response.

If the available sources do not support an answer, the assistant must not invent information.

## 5. Privacy and Redaction

Personal information not required for the assessment should be removed before source documents are committed.

Examples include:

- Personal phone numbers
- Residential addresses
- Private email addresses
- Confidential employer information
- Credentials and API keys

Any synthetic content must be explicitly labelled and must never be presented as verified professional experience.

## 6. Conflicting or Missing Information

When two sources disagree, the system must not silently select an unsupported version.

Conflicts should be recorded in the knowledge base and surfaced when relevant.

If evidence is insufficient, the assistant should clearly communicate that the information cannot be verified.

A real example of a conflict or stale fact will be documented after the source review.

## 7. Adding New Sources

New documents can be integrated without redesigning the knowledge base by:

1. Registering a new source with a unique ID.
2. Extracting and reviewing relevant factual statements.
3. Adding records to `data/knowledge.json`.
4. Linking each fact to its supporting source.
5. Updating the retrieval index and running evaluation tests.

## 8. Current Limitations

The initial implementation uses manually structured JSON rather than an automated document-ingestion pipeline.

Source references provide traceability, but source-ID validation alone does not guarantee that a statement is factually supported.

Future improvements include automated document ingestion, source-level evidence validation, stale-data detection, and retrieval quality monitoring.