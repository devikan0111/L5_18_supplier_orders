# Issues found in `supplier_orders.py`

Baseline: Pylint 2.41/10, Bandit 1 High / 1 Medium / 1 Low, Flake8 4 findings.
After: Pylint 10.00/10, Bandit 0 issues, Flake8 0 issues.
Reports are in `*_report_before.txt` and `*_report_after.txt`.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command built from input (B605, High) | Security | 21 | `os.system("echo ... " + supplier)` runs through a shell, so a supplier name such as `x; rm -rf ~` would execute as a command. | Removed `os.system`; the notification is now a plain `print` (the `echo` was only a placeholder). No process or shell is started. |
| SQL built with string formatting (B608, Medium) | Security / Bug | 11 | Supplier and item were pasted into the INSERT with `%`, so a name like `O'Brien` breaks the query and a crafted one injects SQL. | Parameterised query using `?` placeholders and a values tuple. |
| Silent broad exception (B110 Low, W0718) | Bug / Security | 25-28 | `except Exception: pass` hides every failure, so cleanup could fail and nobody would know. | Catch only `sqlite3.Error` and log it with `logging.exception`. |
| Module-level `global` state (W0603, C0103) | Design | 4-6, 10 | A global connection and global `order_total` made the functions depend on hidden state and shadowed the `conn` parameter (W0621 x4). | Connection is created in `create_connection()` and passed around; the total is a local in `main()`. |
| Unused argument `remarks` (W0613) | Code quality | 16 | `mark_received` accepted `remarks` but never used it, which suggests remarks were being saved when they were not. | Removed the parameter and updated the caller. |
| Code ran on import (no main guard) | Design | 44 | `main()` was called at module level, so importing the file ran the demo. | Added `if __name__ == "__main__":`. |
| camelCase function names (C0103 x3) | Style | 9, 16, 20, 31 | `placeOrder`, `markReceived`, `notifyWarehouse`, `pendingCount` break PEP 8 naming. | Renamed to snake_case and updated all callers. |
| Missing docstrings (C0114, C0116 x6) | Style | 1, 9, 16, 20, 24, 31, 35 | No module or function docstrings. | Added a docstring to the module and every function. |
| Lines too long (E501 x3, C0301 x2) | Style | 5, 11, 32 | Lines up to 131 characters, over the 79 limit. | Split strings and calls across lines. |
| Missing whitespace around operator (E225) | Style | 12 | `order_total+=quantity` | Now `order_total += quantity`. |
| f-string suggestion (C0209) | Style | 11 | `%` formatting where an f-string would be preferred. | Gone with the parameterised query (an f-string would have kept the injection, so it was not used). |

## Commits

1. Fix Bandit findings: parameterised SQL, remove os.system shell call, no silent except
2. Fix Flake8 findings: line length and operator spacing
3. Fix Pylint findings: snake_case names, docstrings, remove global state, main guard
