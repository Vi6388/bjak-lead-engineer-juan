
import json
import statistics
import time

from answer_engine import answer_question


QUESTIONS = [
    "What is your experience with React?",
    "What did you build at Chewy?",
    "Have you built RAG applications?",
    "What is your experience with PostgreSQL?",
    "Did you work at Google?",
]


def percentile(values, fraction):
    ordered = sorted(values)
    index = min(
        len(ordered) - 1,
        max(0, int(len(ordered) * fraction + 0.999999) - 1),
    )
    return ordered[index]


def run_benchmark(iterations=20):
    timings = []

    for _ in range(iterations):
        for question in QUESTIONS:
            start = time.perf_counter()
            answer_question(question)
            elapsed = (time.perf_counter() - start) * 1000
            timings.append(elapsed)

    report = {
        "requests": len(timings),
        "mean_latency_ms": round(statistics.mean(timings), 3),
        "median_latency_ms": round(statistics.median(timings), 3),
        "p95_latency_ms": round(percentile(timings, 0.95), 3),
        "max_latency_ms": round(max(timings), 3),
        "measurement_scope": "Local answer_question execution only",
    }

    with open(
        "evaluation/benchmark_results.json",
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(report, file, indent=2)

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    run_benchmark()
