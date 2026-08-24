# Codomax Python Development Internship

A comprehensive repository containing all core Python projects, object-oriented systems, REST API integrations, and data analysis pipelines developed during the **Codomax Digital Solutions Python Development Internship**.

---

## 📚 Repository Modules Overview

- **Module 2:** Student Record Management System (Functions, File I/O, Exception Handling)
- **Module 3:** Object-Oriented Banking System (Four Pillars of OOP, Clean Architecture)
- **Module 4:** Python Data & APIs (REST API Consumer, Pandas/NumPy Analysis, Data Visualizations)

---

## 📊 Module 4: Python Data & APIs

A complete data analytics application that consumes live REST APIs, performs data cleaning and manipulation with Pandas and NumPy, generates statistical summary reports, and renders visualizations using Matplotlib and Seaborn.

### 🌟 Key Highlights:
- **REST API Integration:** Consumes live HTTP REST endpoints via `requests` and handles structured JSON payloads.
- **Data Cleaning & Wrangling:** Processes missing values, performs feature engineering (word counts, title lengths), and computes normalized statistical metrics via **Pandas** and **NumPy**.
- **Data Visualizations:** Exports analytical charts (distribution histograms and user frequency plots) using **Matplotlib** and **Seaborn**.
- **Automated Reporting:** Generates automated textual statistical summary reports alongside cleaned CSV exports.

---

## 🏦 Module 3: Object-Oriented Banking System

An enterprise-style banking CLI application architected around the core principles of Object-Oriented Programming.

### 📐 Architecture Class Diagram:

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