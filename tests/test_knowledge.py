
from knowledge import load_knowledge


def test_knowledge_base_structure():
    data = load_knowledge()

    assert data["schema_version"] == "1.0"
    assert isinstance(data["sources"], list)
    assert isinstance(data["facts"], list)
    assert isinstance(data["conflicts"], list)


def test_every_fact_has_a_source():
    data = load_knowledge()

    source_ids = {
        source["id"]
        for source in data["sources"]
    }

    for fact in data["facts"]:
        assert fact["source_ids"]
        assert all(
            ref in source_ids
            for ref in fact["source_ids"]
        )
