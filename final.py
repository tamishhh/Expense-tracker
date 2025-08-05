import streamlit as st
import sqlite3
import pandas as pd


conn = sqlite3.connect('expenses.db', check_same_thread=False)
c = conn.cursor()


c.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        category TEXT,
        amount REAL,
        description TEXT
    )
''')
conn.commit()


def add_expense(date, category, amount, description):
    c.execute('INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)',
              (date, category, amount, description))
    conn.commit()

def get_expenses():
    c.execute('SELECT * FROM expenses ORDER BY date DESC')
    rows = c.fetchall()
    columns = ['id', 'date', 'category', 'amount', 'description']
    return pd.DataFrame(rows, columns=columns)

def delete_expense(expense_id):
    c.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    conn.commit()


st.set_page_config(page_title="Expense Tracker", layout="centered")
st.title("💰 Expense Tracker")

st.subheader("➕ Add New Expense")
with st.form(key='expense_form'):
    date = st.date_input("Date")
    category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Other"])
    amount = st.number_input("Amount (₹)", min_value=0.0, format="%.2f")
    description = st.text_input("Description (optional)")
    submit_button = st.form_submit_button(label="Add Expense")

    if submit_button:
        add_expense(date.isoformat(), category, amount, description)
        st.success("Expense added successfully ✅")
        st.rerun()


st.subheader("📋 Your Expenses")
df = get_expenses()

if df.empty:
    st.info("No expenses recorded yet.")
else:
    for index, row in df.iterrows():
        col1, col2 = st.columns([5, 1])
        with col1:
            st.write(f"📅 {row['date']} | 🏷️ {row['category']} | ₹{row['amount']} | 📝 {row['description']}")
        with col2:
            if st.button("❌ Delete", key=f"delete_{row['id']}"):
                delete_expense(row['id'])
                st.success("Expense deleted")
                st.rerun()





