import matplotlib.pyplot as plt
import sqlite3
import pandas as pd

def show_expense_chart(user_id):

    conn = sqlite3.connect(
        "finance.db"
    )

    query = """
    SELECT category,
           SUM(amount)
    FROM transactions
    WHERE user_id=?
    AND type='Expense'
    GROUP BY category
    """

    df = pd.read_sql_query(
        query,
        conn,
        params=(user_id,)
    )

    plt.figure(figsize=(6,6))

    plt.pie(
        df["SUM(amount)"],
        labels=df["category"],
        autopct="%1.1f%%"
    )

    plt.title(
        "Expense Distribution"
    )

    plt.show()