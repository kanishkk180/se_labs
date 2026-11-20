# Lab 5: Static Code Analysis — Issues and Fixes

**Program:** `tower_maintenance.py`  
**Analysis tools:** Pylint, Bandit, and Flake8

The line numbers in this table refer to the original `tower_maintenance.py` file before the fixes. Line numbers may differ in the cleaned version.

| Issue | Type | Original line(s) | Description | Fix applied |
|---|---|---:|---|---|
| SQL query constructed using string formatting | Security — Medium | 11 | The original `addTower` function inserted values directly into an SQL statement using `%` formatting, creating a potential SQL injection risk. | Replaced string formatting with a parameterized SQL query using `?` placeholders and a tuple of values. |
| Unnecessary pickle serialization/deserialization | Security — Medium | 1, 43 | The original program imported `pickle` and serialized then deserialized the result of a database query. This round-trip was unnecessary, and deserializing untrusted pickle data can be unsafe. | Removed the `pickle` import and returned fetched database rows directly from `snapshot()`. |
| Hardcoded password-like value | Security — Low | 6 | `NOC_PASSWORD` contained a password-like string directly in source code. | Removed the unused hardcoded value. If authentication is added later, credentials should be supplied securely through configuration or a secret manager. |
| Overly broad exception handling | Code quality | 20 | Catching `Exception` could hide unexpected errors and make failures harder to diagnose. | Changed the handler to catch `sqlite3.Error` and include the error in the message. |
| Use of `global` for service counter | Code quality | 16 | `serviceTower` modified module-level state through `global service_count`, making it harder to reason about and test. | Removed the global counter. The service count is passed into `service_tower()` and the updated count is returned. |
| Missing function/module docstrings | Maintainability | 1, 10, 15, 25, 34, 42, 46 | The original module and functions did not consistently explain their purpose. | Added a module docstring and concise docstrings to the functions in the cleaned version. |
| Function naming conventions | Style | 10, 15, 34 | Names such as `addTower`, `serviceTower`, and `riskLevel` used camelCase instead of Python's usual `snake_case` convention. | Renamed them to `add_tower`, `service_tower`, and `risk_level`. |
| Long lines and whitespace issues | Style | 5, 11, 18, 25, 35, 43, 50 | Several lines exceeded the configured length limit; Flake8 also reported excessive blank lines and missing whitespace around an operator. | Split long SQL statements and expressions across multiple lines, removed excess blank lines, and corrected whitespace. |
| Unnecessary `else` after `return` | Code quality | 36 | The original `riskLevel()` function used an unnecessary `else` after an `if` branch that already returned. | Removed the `else` and returned `"normal"` after the high-risk check. |
| Missing handling for an unknown tower ID | Potential bug | 35–36 | If the query returned no row, accessing `row[0]` could raise an error. | Added a check for `row is None` and return `"unknown"` when the ID does not exist. |

## Final Verification

The cleaned version was checked with the three static analysis tools. The saved reports show:

- **Pylint:** 10.00/10.
- **Bandit:** No issues identified. Zero findings were reported.
- **Flake8:** The report is empty, indicating no Flake8 violations were reported.
- **Program execution:** The demonstration output was checked against the expected output below.

Expected demonstration output:

```text
['Ridge-A'] high 2 1
```

## Commands Used

```cmd
python -m pylint tower_maintenance.py > pylint_report.txt
python -m bandit -r tower_maintenance.py > bandit_report.txt
python -m flake8 tower_maintenance.py > flake8_report.txt
python tower_maintenance.py
```

The issue descriptions and original line numbers document the initial findings. The final results above reflect the uploaded reports for the cleaned version.
