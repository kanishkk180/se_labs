# Lab 5: Static Code Analysis — Reflection

## 1. What is static code analysis, and how is it different from testing?

Static code analysis examines source code without executing the program. It can identify potential bugs, security weaknesses, naming problems, and style violations early in development. Testing executes the program with selected inputs to check its behavior. The two approaches complement each other: static analysis finds suspicious code patterns, while tests help confirm that the program behaves as expected.

## 2. What are the differences between Pylint, Flake8, and Bandit?

Pylint checks code quality and programming practices, including naming conventions, missing docstrings, broad exception handling, and unnecessary control flow. Flake8 focuses mainly on Python style and formatting, such as line length, blank lines, and whitespace. Bandit scans Python code for common security risks, such as unsafe pickle use, hardcoded password-like strings, and potentially unsafe SQL construction. Using all three gives a broader review than relying on only one tool.

## 3. What issues did you find, and how did you fix them?

The initial analysis identified a possible SQL injection issue caused by building an SQL query with string formatting, unsafe and unnecessary pickle use, a hardcoded password-like value, and overly broad exception handling. The code was updated to use parameterized SQL, remove the pickle round-trip and unused hardcoded value, and catch `sqlite3.Error` rather than the general `Exception` type. The global service counter was also removed, docstrings were added, function names were changed to `snake_case`, and formatting issues were corrected. A check was added to handle an unknown tower ID without raising an indexing error.

## 4. How does static analysis improve software quality and maintainability?

Static analysis helps developers detect problems early, before code reaches production. It encourages consistent style, clearer function names and documentation, more focused exception handling, and safer coding practices. The reports also make issues easier to prioritize and verify after fixes. Static analysis does not prove that a program is completely correct or secure, so it should be combined with running the program, testing important cases, and reviewing the changes.
