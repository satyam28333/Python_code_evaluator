"""Python Code Evaluator: test a Python program against input/output cases.
For trusted local practice code only; this is not a secure sandbox.
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def run_solution(source_code, test_input, timeout=2.0):
    with tempfile.TemporaryDirectory() as tmp:
        script = Path(tmp) / "solution.py"
        script.write_text(source_code, encoding="utf-8")
        try:
            result = subprocess.run(
                [sys.executable, str(script)],
                input=test_input, text=True, capture_output=True,
                timeout=timeout, cwd=tmp, check=False
            )
            return {
                "status": "process_ok" if result.returncode == 0 else "runtime_error",
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
            }
        except subprocess.TimeoutExpired:
            return {
                "status": "timeout", "stdout": "",
                "stderr": f"Execution exceeded {timeout} seconds."
            }


def evaluate(source_code, cases, timeout=2.0):
    results = []
    for index, case in enumerate(cases, start=1):
        outcome = run_solution(source_code, case.get("input", ""), timeout)
        expected = str(case.get("expected", "")).strip()
        if outcome["status"] == "process_ok":
            status = "PASS" if outcome["stdout"] == expected else "FAIL"
        else:
            status = outcome["status"].upper()
        results.append({
            "case": index, "status": status,
            "expected": expected, "actual": outcome["stdout"],
            "stderr": outcome["stderr"]
        })

    total = len(results)
    passed = sum(item["status"] == "PASS" for item in results)
    return {
        "summary": {
            "total": total, "passed": passed, "failed": total - passed,
            "score_percent": round(passed / total * 100, 2) if total else 0
        },
        "results": results
    }


def main():
    parser = argparse.ArgumentParser(description="Test a Python program against JSON test cases.")
    parser.add_argument("--solution", required=True, help="Path to the solution .py file")
    parser.add_argument("--tests", required=True, help="Path to test cases JSON file")
    parser.add_argument("--timeout", type=float, default=2.0, help="Timeout per test in seconds")
    parser.add_argument("--output", help="Optional path to save the JSON report")
    args = parser.parse_args()

    try:
        source = Path(args.solution).read_text(encoding="utf-8")
        cases = json.loads(Path(args.tests).read_text(encoding="utf-8"))
        if not isinstance(cases, list):
            raise ValueError("Test data must be a JSON list.")
        report = evaluate(source, cases, args.timeout)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        raise SystemExit(2)

    rendered = json.dumps(report, indent=2)
    print(rendered)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
