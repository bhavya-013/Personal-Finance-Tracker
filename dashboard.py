import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import pandas as pd
from reports import generate_report
from charts import show_expense_chart


class FinanceDashboard:

    def __init__(self, root, user_id):

        self.root = root
        self.user_id = user_id

        self.root.title("Personal Finance Tracker")
        self.root.geometry("1000x650")
        self.dark_mode = False

        self.conn = sqlite3.connect("finance.db")
        self.cursor = self.conn.cursor()

        self.create_widgets()

        self.load_transactions()
        self.update_summary()

    def create_widgets(self):

        title = tk.Label(
            self.root,
            text="Finance Dashboard",
            font=("Arial", 20, "bold")
        )

        title.pack(pady=10)

        self.balance_label = tk.Label(
            self.root,
            text="Balance: ₹0",
            font=("Arial", 14)
        )
        tk.Button(
           self.root,
           text="Toggle Theme",
           command=self.toggle_theme
        ).pack()

        self.balance_label.pack()

        self.income_label = tk.Label(
            self.root,
            text="Income: ₹0",
            font=("Arial", 12)
        )

        self.income_label.pack()

        self.expense_label = tk.Label(
            self.root,
            text="Expense: ₹0",
            font=("Arial", 12)
        )
        self.savings_label = tk.Label(
             self.root,
             text="Savings Rate: 0%"
        )

        self.savings_label.pack()

        self.expense_label.pack()

        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=15)

        self.type_var = tk.StringVar()
        self.type_var.set("Expense")

        ttk.Combobox(
            input_frame,
            textvariable=self.type_var,
            values=["Income", "Expense"],
            width=15
        ).grid(row=0, column=0, padx=5)

        self.category_entry = tk.Entry(
            input_frame,
            width=20
        )

        self.category_entry.grid(row=0, column=1, padx=5)

        self.amount_entry = tk.Entry(
            input_frame,
            width=20
        )

        self.amount_entry.grid(row=0, column=2, padx=5)

        tk.Button(
            input_frame,
            text="Add Transaction",
            command=self.add_transaction
        ).grid(row=0, column=3, padx=5)

        self.tree = ttk.Treeview(
            self.root,
            columns=(
                "ID",
                "Type",
                "Category",
                "Amount",
                "Date"
            ),
            show="headings"
        )

        for col in (
            "ID",
            "Type",
            "Category",
            "Amount",
            "Date"
        ):
            self.tree.heading(col, text=col)

        self.tree.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )
        budget_frame = tk.Frame(self.root)
        budget_frame.pack(pady=10)

        tk.Label(
        budget_frame,
        text="Monthly Budget"
        ).grid(row=0,column=0)

        self.budget_entry = tk.Entry(
            budget_frame
        )

        self.budget_entry.grid(
           row=0,
           column=1
        )

        tk.Button(
           budget_frame,
           text="Set Budget",
           command=self.set_budget
        ).grid(row=0,column=2)

        search_frame = tk.Frame(self.root)
        search_frame.pack()

        self.search_entry = tk.Entry(
           search_frame,
           width=25
        )

        self.search_entry.grid(
           row=0,
           column=0
        )

        tk.Button(
            search_frame,
            text="Search",
            command=self.search_transactions
        ).grid(row=0,column=1)
    
    def toggle_theme(self):

     if self.dark_mode:

        self.root.configure(bg="white")

        self.balance_label.config(
            bg="white",
            fg="black"
        )

        self.income_label.config(
            bg="white",
            fg="black"
        )

        self.expense_label.config(
            bg="white",
            fg="black"
        )

        self.dark_mode = False

     else:

        self.root.configure(bg="#2b2b2b")

        self.balance_label.config(
            bg="#2b2b2b",
            fg="white"
        )

        self.income_label.config(
            bg="#2b2b2b",
            fg="white"
        )

        self.expense_label.config(
            bg="#2b2b2b",
            fg="white"
        )

        self.dark_mode = True
    def set_budget(self):

     budget = self.budget_entry.get()

     if budget == "":
        return

     self.cursor.execute("""
     INSERT OR REPLACE INTO budgets
     
        user_id,
        monthly_budget
     )
     VALUES (?,?)
     """,
     (
        self.user_id,
        float(budget)
     ))

     self.conn.commit()

     messagebox.showinfo(
        "Success",
        "Budget Updated"
     )

     self.check_budget()

    def add_transaction(self):

        category = self.category_entry.get()
        amount = self.amount_entry.get()
        trans_type = self.type_var.get()

        if category == "" or amount == "":
            messagebox.showerror(
                "Error",
                "Fill all fields"
            )
            return

        self.cursor.execute("""
        INSERT INTO transactions
        (
            user_id,
            type,
            category,
            amount,
            date
        )
        VALUES
        (
            ?, ?, ?, ?, ?
        )
        """,
        (
            self.user_id,
            trans_type,
            category,
            float(amount),
            datetime.now().strftime("%Y-%m-%d")
        ))
        action_frame = tk.Frame(self.root)
        action_frame.pack(pady=10)

        tk.Button(
            action_frame,
            text="Edit Transaction",
            command=self.edit_transaction
        ).grid(row=0,column=0,padx=5)

        tk.Button(
           action_frame,
           text="Delete Transaction",
           command=self.delete_transaction
        ).grid(row=0,column=1,padx=5)
        tk.Button(
           action_frame,
           text="Export CSV",
           command=self.export_csv
        ).grid(row=0,column=2,padx=5)
        tk.Button(
           action_frame,
           text="Export PDF",
           command=self.export_pdf
        ).grid(row=0,column=3,padx=5)
        tk.Button(
          action_frame,
          text="Expense Chart",
          command=self.view_chart
        ).grid(row=0,column=4,padx=5)
        
        self.conn.commit()

        self.category_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

        self.load_transactions()
        self.update_summary()
        self.check_budget()

    def load_transactions(self):

        self.tree.delete(
            *self.tree.get_children()
        )

        self.cursor.execute("""
        SELECT
        id,
        type,
        category,
        amount,
        date
        FROM transactions
        WHERE user_id=?
        ORDER BY id DESC
        """,
        (self.user_id,)
        )

        rows = self.cursor.fetchall()

        for row in rows:
            self.tree.insert(
                "",
                tk.END,
                values=row
            )

    def update_summary(self):

        self.cursor.execute("""
        SELECT SUM(amount)
        FROM transactions
        WHERE user_id=?
        AND type='Income'
        """,
        (self.user_id,)
        )

        income = self.cursor.fetchone()[0] or 0

        self.cursor.execute("""
        SELECT SUM(amount)
        FROM transactions
        WHERE user_id=?
        AND type='Expense'
        """,
        (self.user_id,)
        )

        expense = self.cursor.fetchone()[0] or 0

        balance = income - expense

        self.balance_label.config(
            text=f"Balance: ₹{balance:.2f}"
        )

        self.income_label.config(
            text=f"Income: ₹{income:.2f}"
        )

        self.expense_label.config(
            text=f"Expense: ₹{expense:.2f}"
        )
        savings_rate = 0
        if income > 0:

          savings_rate = (
          balance / income
        ) * 100

    def check_budget(self):

      self.cursor.execute("""
      SELECT monthly_budget
      FROM budgets
      WHERE user_id=?
      """,
     (self.user_id,)
     )

      result = self.cursor.fetchone()

      if not result:
        return

      budget = result[0]

      self.cursor.execute("""
      SELECT SUM(amount)
      FROM transactions
      WHERE user_id=?
      AND type='Expense'
      """,
      (self.user_id,)
      )

      expense = self.cursor.fetchone()[0] or 0

      percent = (expense / budget) * 100

      if percent >= 100:

        messagebox.showwarning(
            "Budget Alert",
            "Budget Exceeded!"
        )

      elif percent >= 80:

        messagebox.showwarning(
            "Budget Alert",
            "80% Budget Used"
        )
    def search_transactions(self):

       keyword = self.search_entry.get()

       self.tree.delete(
         *self.tree.get_children()
       )

       self.cursor.execute("""
       SELECT
       id,
       type,
       category,
       amount,
       date
       FROM transactions
       WHERE user_id=?
       AND category LIKE ?
       """,
       (
         self.user_id,
         f"%{keyword}%"
       )
      )

       rows = self.cursor.fetchall()

       for row in rows:

        self.tree.insert(
            "",
            tk.END,
            values=row
        )
    def delete_transaction(self):

       selected = self.tree.selection()

       if not selected:
         return

       values = self.tree.item(
          selected[0]
       )["values"]

       transaction_id = values[0]

       self.cursor.execute("""
         DELETE FROM transactions
          WHERE id=?
         """,
       (transaction_id,)
       )

       self.conn.commit()

       self.load_transactions()
       self.update_summary()
    def edit_transaction(self):

        selected = self.tree.selection()

        if not selected:
           return
 
        values = self.tree.item(
            selected[0]
        )["values"]

        transaction_id = values[0]

        new_category = self.category_entry.get()
        new_amount = self.amount_entry.get()

        self.cursor.execute("""
        UPDATE transactions
        SET
        category=?,
        amount=?
        WHERE id=?
        """,
      (
        new_category,
        float(new_amount),
        transaction_id
      )
      )

    def export_csv(self):

     query = """
     SELECT *
     FROM transactions
     WHERE user_id=?
     """

     df = pd.read_sql_query(
        query,
        self.conn,
        params=(self.user_id,)
     )

     df.to_csv(
        "exports/transactions.csv",
        index=False
     )

     messagebox.showinfo(
        "Success",
        "CSV Exported"
     )
    def export_pdf(self):

       self.cursor.execute("""
       SELECT SUM(amount)
       FROM transactions
       WHERE user_id=?
       AND type='Income'
       """,
       (self.user_id,)
    )

       income = self.cursor.fetchone()[0] or 0

       self.cursor.execute("""
       SELECT SUM(amount)
       FROM transactions
       WHERE user_id=?
       AND type='Expense'
       """,
       (self.user_id,)
       )

       expense = self.cursor.fetchone()[0] or 0

       balance = income - expense

       generate_report(
        income,
        expense,
        balance
       )

       messagebox.showinfo(
        "Success",
        "PDF Generated"
       )  
    def view_chart(self):

     show_expense_chart(
        self.user_id
    )         
    
     self.conn.commit()

     self.load_transactions()
     self.update_summary()
    