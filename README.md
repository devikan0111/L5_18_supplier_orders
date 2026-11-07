# Lab 5: Static Code Analysis - Supplier Purchase Order Tracker

**Name:** Devika N
**SRN:** PES1UG24AM080
**Course:** Software Engineering


## Problem Statement

`supplier_orders.py` is a purchase order tracker for a stores department. It places orders with suppliers, marks deliveries as received, notifies the warehouse and cleans up fulfilled orders. It uses an in-memory SQLite database.

## Repository contents

| File | Description |
|------|-------------|
| `supplier_orders.py` | Cleaned and fixed version of the program |
| `issues.md` | Table of all issues found, with line numbers, descriptions and fixes |
| `pylint_report_before.txt` / `pylint_report_after.txt` | Pylint output before and after the fixes |
| `flake8_report_before.txt` / `flake8_report_after.txt` | Flake8 output before and after the fixes |
| `bandit_report_before.txt` / `bandit_report_after.txt` | Bandit output before and after the fixes |

## How to run

```
pip install pylint bandit flake8
python supplier_orders.py
pylint supplier_orders.py
flake8 supplier_orders.py
bandit -r supplier_orders.py
```

Expected output of the program:

```
notifying warehouse about Acme
1 540
```

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 2.41 / 10 | 10.00 / 10 |
| Bandit | 1 High, 1 Medium, 1 Low | 0 issues |
| Flake8 | 4 findings | 0 findings |

## Issues found and fixed

The full table, with line numbers, is in [`issues.md`](issues.md).

**Security (Bandit)**
- **B605 (High):** `os.system("echo ... " + supplier)` ran through a shell, so a supplier name like `x; rm -rf ~` would execute as a command. The shell call was removed.
- **B608 (Medium):** the INSERT query was built with string formatting, which breaks on names like `O'Brien` and allows SQL injection. It now uses a parameterised query with `?` placeholders.
- **B110 (Low):** `except Exception: pass` silently hid every failure. It now catches only `sqlite3.Error` and logs it with `logging.exception`.

**Design and bugs (Pylint)**
- Removed module-level `global` state. The database connection is now created in `create_connection()` and passed to each function, and the order total is a local variable in `main()`.
- Removed the unused `remarks` argument of `mark_received`.
- Added an `if __name__ == "__main__":` guard so importing the file no longer runs the demo.

**Style (Pylint and Flake8)**
- Renamed camelCase functions to snake_case (`placeOrder` to `place_order`, and so on).
- Added a module docstring and a docstring for every function.
- Split lines longer than 79 characters and fixed spacing around operators.


## Commit history

1. Fix Bandit findings
2. Fix Flake8 findings
3. Fix Pylint findings
