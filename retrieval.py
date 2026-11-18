
import re
from collections import Counter
from knowledge import load_knowledge

STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by",
    "can", "did", "do", "does", "for", "from", "have",
    "has", "how", "i", "in", "is", "me", "my", "of",
    "on", "or", "the", "their", "to", "was", "were",
    "what", "which", "who", "with", "you", "your",
    "about", "tell", "please", "experience",

    # Generic question/action terms are not evidence
    # of a specific professional capability.
    "build", "built", "building",
    "software", "application", "applications",
}


def tokenize(text):
    words = re.findall(r"[a-z0-9+#.]+", text.lower())
    return [
        word for word in words
        if word not in STOP_WORDS and len(word) > 1
    ]


def retrieve(question, top_k=5):
    """
    Retrieve ranked CV facts with source metadata.

    A search match is only a candidate, not proof
    that the fact answers the question.
    """
    if not isinstance(question, str):
        return []

    query_tokens = tokenize(question)

    if not query_tokens:
        return []

    data = load_knowledge()
    facts = data["facts"]
    sources = {
        source["id"]: source
        for source in data["sources"]
    }

    if not facts:
        return []

    query_terms = set(query_tokens)
    documents = []

    for fact in facts:
        tokens = tokenize(
            fact["text"] + " " +
            " ".join(fact.get("tags", []))
        )
        documents.append(tokens)

    document_frequency = Counter()

    for tokens in documents:
        document_frequency.update(set(tokens))

    results = []

    for fact, tokens in zip(facts, documents):
        matched = query_terms.intersection(tokens)

        if not matched:
            continue

        # Rare terms are more informative.
        score = sum(
            1.0 / document_frequency[term]
            for term in matched
        )

        # Prefer coverage of the user's question.
        coverage = len(matched) / len(query_terms)
        score += 2.0 * coverage

        # Retrieve source metadata for citations.
        citations = [
            sources[source_id]
            for source_id in fact["source_ids"]
        ]

        results.append({
            "id": fact["id"],
            "text": fact["text"],
            "category": fact.get("category", ""),
            "score": round(score, 4),
            "coverage": round(coverage, 4),
            "sources": citations
        })

    results.sort(
        key=lambda item: (
            -item["score"],
            item["id"]
        )
    )

    return results[:max(0, top_k)]


if __name__ == "__main__":
    questions = [
        "What is your experience with React?",
        "Have you built RAG applications?",
        "What did you do at Chewy?",
        "What is your experience with PostgreSQL?",
        "Did you work at Google?"
    ]

    for question in questions:
        print(f"\nQuestion: {question}")

        results = retrieve(question, top_k=3)

        if not results:
            print("No relevant evidence found.")
            continue

        for result in results:
            print(f"  Fact: {result['text']}")
            print(f"  Score: {result['score']}")

            for source in result["sources"]:
                print(
                    f"  Source: {source['id']}, "
                    f"page {source.get('page', 'N/A')}"
                )
