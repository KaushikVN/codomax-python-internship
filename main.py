"""
Codomax Python Internship - Module 6: Python Capstone Project
Project: Smart Expense Tracker & Financial Analytics API
Architecture: FastAPI, SQLite, Pydantic, Logging, Static Web Dashboard, and Render Deployment.
"""

import sqlite3
import logging
from typing import List, Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

# Setup Enterprise Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

DB_NAME = "expenses.db"

app = FastAPI(
    title="Smart Expense Tracker & Financial Analytics API",
    description="Full-stack Capstone Project for Codomax Python Development Internship",
    version="2.0.0"
)


# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            notes TEXT
        )
    """)
    conn.commit()
    conn.close()
    logging.info("Database initialized successfully.")

init_db()


# --- PYDANTIC SCHEMAS ---
class ExpenseCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=100)
    category: str = Field(..., min_length=2, max_length=50)
    amount: float = Field(..., gt=0)
    notes: Optional[str] = None


class ExpenseResponse(BaseModel):
    id: int
    title: str
    category: str
    amount: float
    date: str
    notes: Optional[str]


# --- REST API ENDPOINTS ---

@app.get("/api/expenses", response_model=List[ExpenseResponse], tags=["Expenses"])
def get_all_expenses():
    """Retrieve all expenses sorted by most recent."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


@app.post("/api/expenses", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED, tags=["Expenses"])
def create_expense(expense: ExpenseCreate):
    """Add a new expense with validation and logging."""
    try:
        entry_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO expenses (title, category, amount, date, notes) VALUES (?, ?, ?, ?, ?)",
            (expense.title, expense.category, expense.amount, entry_date, expense.notes)
        )
        conn.commit()
        expense_id = cursor.lastrowid
        conn.close()
        logging.info(f"Created Expense #{expense_id}: {expense.title} - ₹{expense.amount}")
        return {
            "id": expense_id,
            "title": expense.title,
            "category": expense.category,
            "amount": expense.amount,
            "date": entry_date,
            "notes": expense.notes
        }
    except Exception as e:
        logging.error(f"Error creating expense: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/api/expenses/analytics", tags=["Analytics"])
def get_analytics():
    """Get category-wise breakdown and total expenditure."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total_spent = cursor.fetchone()[0] or 0.0

    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    category_summary = {row[0]: round(row[1], 2) for row in cursor.fetchall()}
    conn.close()

    return {
        "total_expenditure": round(total_spent, 2),
        "category_breakdown": category_summary,
        "currency": "INR"
    }


@app.delete("/api/expenses/{expense_id}", tags=["Expenses"])
def delete_expense(expense_id: int):
    """Delete an expense record."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    rows = cursor.rowcount
    conn.close()

    if rows == 0:
        raise HTTPException(status_code=404, detail=f"Expense #{expense_id} not found")
    logging.info(f"Deleted Expense #{expense_id}")
    return {"message": f"Expense #{expense_id} deleted successfully"}


# --- WEB DASHBOARD FRONTEND ---
@app.get("/", response_class=HTMLResponse, tags=["Dashboard"])
def serve_dashboard():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Smart Expense Tracker | Python Capstone</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: system-ui, -apple-system, sans-serif; }
            body { background: linear-gradient(135deg, #f0fdf4, #e0f2fe); min-height: 100vh; padding: 2rem 1rem; color: #1e293b; }
            .container { max-width: 900px; margin: 0 auto; }
            .card { background: rgba(255, 255, 255, 0.9); border-radius: 16px; padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
            h1 { color: #0f172a; margin-bottom: 0.5rem; }
            .stats { display: flex; gap: 1rem; margin-bottom: 1.5rem; }
            .stat-box { flex: 1; background: #2563eb; color: white; padding: 1.25rem; border-radius: 12px; font-weight: bold; }
            .stat-box span { font-size: 1.8rem; display: block; margin-top: 0.25rem; }
            form { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 0.75rem; }
            input, select, button { padding: 0.75rem; border-radius: 8px; border: 1px solid #cbd5e1; font-size: 0.95rem; }
            button { background: #16a34a; color: white; border: none; font-weight: bold; cursor: pointer; transition: 0.2s; }
            button:hover { background: #15803d; }
            table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
            th, td { padding: 0.75rem; text-align: left; border-bottom: 1px solid #e2e8f0; }
            th { background: #f8fafc; color: #64748b; font-size: 0.85rem; text-transform: uppercase; }
            .del-btn { background: #ef4444; color: white; padding: 0.35rem 0.65rem; border-radius: 6px; border: none; cursor: pointer; }
            .docs-link { display: inline-block; margin-top: 1rem; color: #2563eb; text-decoration: none; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="card">
                <h1>💰 Smart Expense Tracker</h1>
                <p>Codomax Python Internship Capstone Project</p>
                <a href="/docs" target="_blank" class="docs-link">📖 View Interactive Swagger API Docs &rarr;</a>
            </div>

            <div class="stats">
                <div class="stat-box">Total Expenditure<span id="total-val">₹0.00</span></div>
            </div>

            <div class="card">
                <h3>+ Add New Expense</h3><br>
                <form id="exp-form">
                    <input type="text" id="title" placeholder="Expense Title" required>
                    <select id="category" required>
                        <option value="Food & Dining">Food & Dining</option>
                        <option value="Transportation">Transportation</option>
                        <option value="Software & Cloud">Software & Cloud</option>
                        <option value="Education">Education</option>
                        <option value="Utilities">Utilities</option>
                    </select>
                    <input type="number" id="amount" placeholder="Amount (₹)" step="0.01" required>
                    <button type="submit">Add Record</button>
                </form>
            </div>

            <div class="card">
                <h3>📊 Expense History</h3>
                <table>
                    <thead>
                        <tr><th>Title</th><th>Category</th><th>Amount</th><th>Date</th><th>Action</th></tr>
                    </thead>
                    <tbody id="expense-table"></tbody>
                </table>
            </div>
        </div>

        <script>
            async function loadData() {
                const [expRes, anaRes] = await Promise.all([
                    fetch('/api/expenses'),
                    fetch('/api/expenses/analytics')
                ]);
                const expenses = await expRes.json();
                const analytics = await anaRes.json();

                document.getElementById('total-val').innerText = `₹${analytics.total_expenditure.toFixed(2)}`;

                const tbody = document.getElementById('expense-table');
                tbody.innerHTML = expenses.map(e => `
                    <tr>
                        <td><strong>${e.title}</strong></td>
                        <td>${e.category}</td>
                        <td>₹${e.amount.toFixed(2)}</td>
                        <td><small>${e.date}</small></td>
                        <td><button class="del-btn" onclick="deleteItem(${e.id})">Delete</button></td>
                    </tr>
                `).join('');
            }

            document.getElementById('exp-form').addEventListener('submit', async (e) => {
                e.preventDefault();
                const title = document.getElementById('title').value;
                const category = document.getElementById('category').value;
                const amount = parseFloat(document.getElementById('amount').value);

                await fetch('/api/expenses', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ title, category, amount })
                });

                e.target.reset();
                loadData();
            });

            async function deleteItem(id) {
                await fetch(`/api/expenses/${id}`, { method: 'DELETE' });
                loadData();
            }

            loadData();
        </script>
    </body>
    </html>
    """


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)