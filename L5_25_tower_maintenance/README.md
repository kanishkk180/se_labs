# Lab 5: Static Code Analysis — Telecom Tower Maintenance Tracker

## About the Program

This lab uses a Python telecom tower maintenance tracker to demonstrate static code analysis. The program stores tower records in an in-memory SQLite database, records servicing, lists overdue towers, and classifies tower risk based on fault counts.

## Tools Used

- **Pylint:** Reviews code quality and programming practices.
- **Bandit:** Scans Python code for common security issues.
- **Flake8:** Checks Python style and formatting.

## Setup

Install the required tools:

```bash
python -m pip install pylint bandit flake8
```

## Run the Program

```bash
python tower_maintenance.py
```

Expected demonstration output:

```text
['Ridge-A'] high 2 1
```

## Run Static Analysis

Run the following commands from the directory containing `tower_maintenance.py`:

```bash
python -m pylint tower_maintenance.py > pylint_report.txt
python -m bandit -r tower_maintenance.py > bandit_report.txt
python -m flake8 tower_maintenance.py > flake8_report.txt
```

The output is saved in the corresponding report files.

## Results

The uploaded final reports show:

- **Pylint:** 10.00/10.
- **Bandit:** No issues identified.
- **Flake8:** Empty report; no violations were reported.

## Files

- `tower_maintenance.py` — cleaned Python source code.
- `issues.md` — issues found in the original code and fixes applied.
- `reflection.md` — reflection answers.
- `pylint_report.txt` — Pylint output.
- `bandit_report.txt` — Bandit output.
- `flake8_report.txt` — Flake8 output.

## Notes

Do not include the local `venv/` or `.venv/` environment directories in the submission. They contain locally installed packages and are not source-code deliverables.
