# Codomax Python Development Internship

A modular repository containing all internship assignments, projects, and object-oriented implementations for Codomax Digital Solutions.

---

## 🏦 Module 3: Object-Oriented Python Banking System

An enterprise-patterned banking application built using core Object-Oriented Programming (OOP) principles.

### 📐 Clean Architecture Class Diagram

```text
               +----------------------------------+
               |        <<abstract>> Account      |
               +----------------------------------+
               | - _account_number: str           |
               | - _holder_name: str              |
               | - __balance: float (Private)     |
               | - _transactions: list            |
               +----------------------------------+
               | + deposit(amount: float): bool   |
               | + withdraw(amount: float)*: bool |
               | + display_statement(): void      |
               | + to_dict(): dict                |
               +-----------------+----------------+
                                 |
                 +---------------+---------------+
                 |                               |
                 v                               v
+-------------------------------+ +--------------------------------+
|        SavingsAccount         | |         CurrentAccount         |
+-------------------------------+ +--------------------------------+
| + min_balance: float = 500.0  | | + overdraft_limit: float = 5000|
+-------------------------------+ +--------------------------------+
| + withdraw(amount: float)     | | + withdraw(amount: float)      |
+-------------------------------+ +--------------------------------+

                 +--------------------------------+
                 |              Bank              |
                 +--------------------------------+
                 | + accounts: dict               |
                 +--------------------------------+
                 | + create_account()             |
                 | + get_account()                |
                 | + save_data() / load_data()    |
                 +--------------------------------+