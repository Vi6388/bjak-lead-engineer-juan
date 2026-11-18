"""Run from repository root: python evaluate.py"""
import json
import math
import statistics
import time
from pathlib import Path

from answer_engine import answer_question

ROOT = Path(__file__).resolve().parent
DATASET = ROOT / "evaluation" / "questions.json"
OUTPUT = ROOT / "evaluation" / "results.json"
PASS_BAR = 0.85  # Provisional target for exact response-status accuracy.
REFUSAL_STATUSES = {"unsupported", "ambiguous"}


def ratio(numerator, denominator):
    return round(numerator / denominator, 4) if denominator else None


def percentile_nearest_rank(values, p):
    if not values:
        return None
    ordered = sorted(values)
    return round(ordered[max(0, math.ceil(len(ordered) * p) - 1)], 2)


def run():
    questions = json.loads(DATASET.read_text(encoding="utf-8"))
    rows = []
    for item in questions:
        start = time.perf_counter()
        try:
            response = answer_question(item["question"])
        except Exception as exc:
            response = {"status": "error", "answer": "", "citations": []}
            error_type = type(exc).__name__
        else:
            error_type = None
        elapsed_ms = (time.perf_counter() - start) * 1000
        status = response.get("status", "error")
        answer = str(response.get("answer", ""))
        citations = response.get("citations", [])
        expected = item["expected_status"]
        contains_ok = all(term.casefold() in answer.casefold() for term in item.get("must_contain", []))
        prohibited_ok = all(term.casefold() not in answer.casefold() for term in item.get("must_not_claim", []))
        status_ok = status == expected
        evidence_ok = bool(citations) if status == "answered" else not bool(citations)
        passed = status_ok and contains_ok and prohibited_ok and evidence_ok
        rows.append({
            "id": item["id"], "category": item["category"], "question": item["question"],
            "expected_status": expected, "actual_status": status, "status_ok": status_ok,
            "required_terms_ok": contains_ok, "prohibited_claims_ok": prohibited_ok,
            "citation_policy_ok": evidence_ok, "passed": passed,
            "latency_ms": round(elapsed_ms, 2), "answer": answer,
            "citations": citations, "exception_type": error_type,
        })
    answered = [r for r in rows if r["actual_status"] == "answered"]
    refusals = [r for r in rows if r["expected_status"] in REFUSAL_STATUSES]
    # Extractive-format proxy, not an independent factual entailment check.
    extractive = [r for r in answered if r["answer"].startswith("Based on my documented experience:")]
    summary = {
        "total": len(rows), "passed": sum(r["passed"] for r in rows),
        "full_case_pass_rate": ratio(sum(r["passed"] for r in rows), len(rows)),
        "status_accuracy": ratio(sum(r["status_ok"] for r in rows), len(rows)),
        "citation_presence": ratio(sum(bool(r["citations"]) for r in answered), len(answered)),
        "extractive_format_proxy": ratio(len(extractive), len(answered)),
        "refusal_correctness": ratio(sum(r["actual_status"] == r["expected_status"] for r in refusals), len(refusals)),
        "prohibited_claim_check_rate": ratio(sum(r["prohibited_claims_ok"] for r in rows), len(rows)),
        "p95_latency_ms": percentile_nearest_rank([r["latency_ms"] for r in rows], 0.95),
        "pass_bar_status_accuracy": PASS_BAR,
        "meets_status_accuracy_bar": ratio(sum(r["status_ok"] for r in rows), len(rows)) >= PASS_BAR,
    }
    OUTPUT.write_text(json.dumps({"summary": summary, "cases": rows}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("ID  Category       Expected     Actual       Pass  Latency(ms)")
    print("-" * 70)
    for r in rows:
        print(f"{r['id']:<3} {r['category']:<14} {r['expected_status']:<12} {r['actual_status']:<12} {str(r['passed']):<5} {r['latency_ms']:>9.2f}")
    print("\nSUMMARY")
    for key, value in summary.items():
        print(f"{key}: {value}")
    print(f"\nSaved: {OUTPUT}")


if __name__ == "__main__":
    run()
