# Lab 6 — Train Fare Coverage

## Files
- `train_fare.py` — application under test.
- `test_train_fare.py` — complete pytest test suite.
- `CodeCoverageTest_213_application.py` — tests for code/statement coverage.
- `BranchCoverageTest_213_application.py` — tests for branch coverage.

## Install dependencies
```bash
python -m pip install pytest coverage
```

## Code coverage
```bash
python -m coverage erase
python -m coverage run -m pytest -v CodeCoverageTest_213_application.py
python -m coverage report -m
```

## Branch coverage
```bash
python -m coverage erase
python -m coverage run --branch -m pytest -v BranchCoverageTest_213_application.py
python -m coverage report -m
```

The two coverage test files intentionally contain the same test cases. The `--branch` option enables branch measurement.
