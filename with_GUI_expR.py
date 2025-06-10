import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import json
import os

# File paths
data_file = "expenses.json"
category_file = "custom_categories.json"
budget_file = "budgets.json"

# Load existing data
def load_data():
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            return json.load(file)
    return []

def save_data(data):
    with open(data_file, 'w') as file:
        json.dump(data, file, indent=4)

# Load and save custom categories
def load_custom_categories():
    if os.path.exists(category_file):
        with open(category_file, 'r') as file:
            return json.load(file)
    return {}

def save_custom_categories(custom_cats):
    with open(category_file, 'w') as file:
        json.dump(custom_cats, file, indent=4)

# GUI Functions
def add_expense():
    try:
        amount = float(entry_amount.get())
        description = entry_description.get()
        category = combo_category.get()

        if not category:
            raise ValueError("Category is required.")

        data = load_data()
        data.append({
            "amount": amount,
            "description": description,
            "category": category,
            "date": datetime.today().date().isoformat()
        })
        save_data(data)
        messagebox.showinfo("Success", "Expense added successfully!")
    except ValueError as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

def show_summary():
    data = load_data()
    if not data:
        messagebox.showinfo("Info", "No data available.")
        return
    df = pd.DataFrame(data)
    summary = df.groupby("category")["amount"].sum()
    summary_window = tk.Toplevel(root)
    summary_window.title("Expense Summary")
    summary_window.configure(bg="#f0f0f0")
    text = tk.Text(summary_window, height=10, width=50, bg="#ffffff", fg="#333333")
    text.pack(padx=10, pady=10)
    text.insert(tk.END, summary.to_string())
    text.insert(tk.END, f"\n\nTotal: ₹{df['amount'].sum():.2f}")

def export_excel():
    data = load_data()
    if not data:
        messagebox.showinfo("Info", "No data to export.")
        return
    df = pd.DataFrame(data)
    df.to_excel("expenses_export.xlsx", index=False)
    messagebox.showinfo("Exported", "Data exported to expenses_export.xlsx")

def search_expense():
    keyword = entry_search.get().lower()
    data = load_data()
    results = [exp for exp in data if keyword in exp['description'].lower() or keyword in exp['category'].lower()]

    result_window = tk.Toplevel(root)
    result_window.title("Search Results")
    result_window.configure(bg="#f0f0f0")
    text = tk.Text(result_window, height=15, width=60, bg="#ffffff", fg="#333333")
    text.pack(padx=10, pady=10)
    if results:
        for r in results:
            text.insert(tk.END, f"{r['date']} | {r['category']}: ₹{r['amount']:.2f} - {r['description']}\n")
    else:
        text.insert(tk.END, "No matching records found.")

def visualize():
    data = load_data()
    if not data:
        messagebox.showinfo("Info", "No data to visualize.")
        return
    df = pd.DataFrame(data)
    summary = df.groupby("category")["amount"].sum()
    summary.plot(kind="bar", color="#FF6F61", figsize=(8, 5))
    plt.title("---Expense Summary Visualization---")
    plt.xlabel("Categories")
    plt.ylabel("Total Expense")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def view_by_period():
    data = load_data()
    if not data:
        messagebox.showinfo("Info", "No data available.")
        return

    def filter():
        choice = combo_choice.get()
        today = datetime.today().date()

        if choice == "Today":
            start_date = today
        elif choice == "Last 7 Days":
            start_date = today - timedelta(days=7)
        elif choice == "This Month":
            start_date = today.replace(day=1)
        else:
            messagebox.showerror("Error", "Invalid period selected.")
            return

        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"]).dt.date
        filtered = df[df["date"] >= start_date]

        if var_filter.get():
            selected_category = entry_cat.get()
            filtered = filtered[filtered['category'] == selected_category]

        result_win = tk.Toplevel(root)
        result_win.title("Filtered Expenses")
        result_win.configure(bg="#f0f0f0")

        text = tk.Text(result_win, height=20, width=70, bg="#ffffff", fg="#333333")
        text.pack(padx=10, pady=10)

        if filtered.empty:
            text.insert(tk.END, "No expenses found for this period.")
        else:
            for _, row in filtered.iterrows():
                text.insert(tk.END, f"{row['date']} | {row['category']}: ₹{row['amount']:.2f} - {row['description']}\n")
                
            text.insert(tk.END, "\n--- Grouped Summary ---\n")
            text.insert(tk.END, filtered.groupby("category")["amount"].sum().to_string())

    win = tk.Toplevel(root)
    win.title("View by Period")
    win.configure(bg="#e6f2ff")

    tk.Label(win, text="Choose period:", bg="#e6f2ff").pack(pady=5)
    combo_choice = ttk.Combobox(win, values=["Today", "Last 7 Days", "This Month"])
    combo_choice.pack(pady=5)

    var_filter = tk.BooleanVar()
    tk.Checkbutton(win, text="Filter by Category", variable=var_filter, bg="#e6f2ff").pack(pady=5)
    entry_cat = tk.Entry(win)
    entry_cat.pack(pady=5)

    tk.Button(win, text="Apply Filter", command=filter, bg="#607D8B", fg="white").pack(pady=10)

def highest_lowest():
    data = load_data()
    if not data:
        messagebox.showinfo("Info", "No data available.")
        return
    df = pd.DataFrame(data)
    highest = df.loc[df['amount'].idxmax()]
    lowest = df.loc[df['amount'].idxmin()]
    messagebox.showinfo("Extremes", f"Highest: ₹{highest['amount']} - {highest['description']}\nLowest: ₹{lowest['amount']} - {lowest['description']}")

def set_and_check_budgets():
    messagebox.showinfo("Budgets", "This feature is under development.")

def manage_categories():
    messagebox.showinfo("Manage Categories", "This feature is under development.")

# GUI Setup
root = tk.Tk()
root.title("Expense Tracker")
root.configure(bg="#e6f2ff")

frame = tk.Frame(root, bg="#e6f2ff")
frame.pack(pady=20)

# Labels and Entries
tk.Label(frame, text="Amount:", bg="#e6f2ff", font=("Arial", 10)).grid(row=0, column=0, sticky='w')
entry_amount = tk.Entry(frame)
entry_amount.grid(row=0, column=1)

tk.Label(frame, text="Description:", bg="#e6f2ff", font=("Arial", 10)).grid(row=1, column=0, sticky='w')
entry_description = tk.Entry(frame)
entry_description.grid(row=1, column=1)

categories = list(load_custom_categories().keys()) or ["Groceries", "Travel", "Bills"]
tk.Label(frame, text="Category:", bg="#e6f2ff", font=("Arial", 10)).grid(row=2, column=0, sticky='w')
combo_category = ttk.Combobox(frame, values=categories)
combo_category.grid(row=2, column=1)

# Buttons
tk.Button(frame, text="Add Expense", command=add_expense, bg="#4CAF50", fg="white", width=20).grid(row=3, column=0, pady=10, columnspan=2)
tk.Button(frame, text="View Summary", command=show_summary, bg="#2196F3", fg="white", width=20).grid(row=4, column=0, pady=5, columnspan=2)
tk.Button(frame, text="Export to Excel", command=export_excel, bg="#FF9800", fg="white", width=20).grid(row=5, column=0, pady=5, columnspan=2)
tk.Button(frame, text="Visualize", command=visualize, bg="#9C27B0", fg="white", width=20).grid(row=6, column=0, pady=5, columnspan=2)
tk.Button(frame, text="View by Period", command=view_by_period, bg="#607D8B", fg="white", width=20).grid(row=7, column=0, pady=5, columnspan=2)
tk.Button(frame, text="Highest & Lowest", command=highest_lowest, bg="#795548", fg="white", width=20).grid(row=8, column=0, pady=5, columnspan=2)
tk.Button(frame, text="Set & Check Budgets", command=set_and_check_budgets, bg="#009688", fg="white", width=20).grid(row=9, column=0, pady=5, columnspan=2)
tk.Button(frame, text="Manage Categories", command=manage_categories, bg="#3F51B5", fg="white", width=20).grid(row=10, column=0, pady=5, columnspan=2)

# Search Bar
search_frame = tk.Frame(root, bg="#e6f2ff")
search_frame.pack(pady=10)
tk.Label(search_frame, text="Search:", bg="#e6f2ff", font=("Arial", 10)).pack(side=tk.LEFT)
entry_search = tk.Entry(search_frame)
entry_search.pack(side=tk.LEFT)
tk.Button(search_frame, text="Go", command=search_expense, bg="#607D8B", fg="white").pack(side=tk.LEFT, padx=5)

root.mainloop()
