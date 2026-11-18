
import json
from pathlib import Path

KNOWLEDGE_PATH = (
    Path(__file__).resolve().parent
    / "data"
    / "knowledge.json"
)


class KnowledgeBaseError(Exception):
    pass


def load_knowledge():
    if not KNOWLEDGE_PATH.exists():
        raise KnowledgeBaseError(
            "Knowledge base file not found."
        )

    try:
        with KNOWLEDGE_PATH.open(
            "r", encoding="utf-8"
        ) as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError) as exc:
        raise KnowledgeBaseError(
            "Cannot read the knowledge base."
        ) from exc

    if not isinstance(data, dict):
        raise KnowledgeBaseError(
            "Knowledge base must be an object."
        )

    for field in ("sources", "facts", "conflicts"):
        if not isinstance(data.get(field), list):
            raise KnowledgeBaseError(
                f"Invalid knowledge field: {field}"
            )

    source_ids = set()

    for source in data["sources"]:
        if not isinstance(source, dict):
            raise KnowledgeBaseError(
                "Invalid source record."
            )

        source_id = source.get("id")

        if not isinstance(source_id, str) or not source_id:
            raise KnowledgeBaseError(
                "Every source needs an ID."
            )

        if source_id in source_ids:
            raise KnowledgeBaseError(
                f"Duplicate source ID: {source_id}"
            )

        source_ids.add(source_id)

    fact_ids = set()

    for fact in data["facts"]:
        if not isinstance(fact, dict):
            raise KnowledgeBaseError(
                "Invalid fact record."
            )

        fact_id = fact.get("id")
        text = fact.get("text")
        refs = fact.get("source_ids")

        if not isinstance(fact_id, str) or not fact_id:
            raise KnowledgeBaseError(
                "Every fact needs an ID."
            )

        if fact_id in fact_ids:
            raise KnowledgeBaseError(
                f"Duplicate fact ID: {fact_id}"
            )

        fact_ids.add(fact_id)

        if not isinstance(text, str) or not text.strip():
            raise KnowledgeBaseError(
                f"Fact {fact_id} has no text."
            )

        if (
            not isinstance(refs, list)
            or not refs
            or any(
                not isinstance(ref, str)
                or ref not in source_ids
                for ref in refs
            )
        ):
            raise KnowledgeBaseError(
                f"Fact {fact_id} has invalid sources."
            )

    return data


def get_facts():
    return load_knowledge()["facts"]


def get_sources():
    return load_knowledge()["sources"]


if __name__ == "__main__":
    knowledge = load_knowledge()

    print("Knowledge base loaded successfully.")
    print("Sources:", len(knowledge["sources"]))
    print("Facts:", len(knowledge["facts"]))
    print("Conflicts:", len(knowledge["conflicts"]))
