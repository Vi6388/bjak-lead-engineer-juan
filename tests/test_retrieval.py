
from retrieval import retrieve


def test_react_retrieval():
    results = retrieve("React")

    assert results
    assert any(
        "react" in item["text"].lower()
        for item in results
    )


def test_rag_retrieval():
    results = retrieve("RAG", top_k=10)

    assert results
    assert any(
        "rag" in item["text"].lower()
        for item in results
    )


def test_empty_question():
    assert retrieve("") == []


def test_unrelated_question():
    results = retrieve("quantum astrophysics")

    assert results == []


def test_source_references():
    results = retrieve("PostgreSQL")

    assert results

    for result in results:
        assert result["sources"]
        assert all(
            source["id"]
            for source in result["sources"]
        )
