# Python Code Evaluator & Automated Testing Tool

## Overview
A command-line project that tests a Python solution against multiple test cases. It compares actual output with expected output and creates a JSON report showing passes, failures, runtime errors, and timeouts.

## Why it is relevant
AI-generated code should be tested, not accepted blindly. This project demonstrates test-case-based evaluation, output comparison, basic runtime-error detection, timeouts, and machine-readable reports.

## Requirements
- Python 3.10+
- Standard library only; no packages required

## Run the example
```bash
python main.py --solution sample_solution.py --tests tests.json --output report.json
```

## Add test cases
Edit `tests.json`:
```json
[
  {"input": "2 3\n", "expected": "5"}
]
```
Each test has an `input` string and an `expected` output string.

## Limitations and safety
This is a learning/portfolio project, not a secure code execution service. A subprocess and timeout do not prevent all malicious behavior. Do not run untrusted code on a computer containing sensitive files or credentials. A production system needs a properly isolated sandbox/container with CPU, memory, filesystem, and network restrictions.

## Portfolio advice
Run the example, inspect the report, and understand every function before describing it to a client.
