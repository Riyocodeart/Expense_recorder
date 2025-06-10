import pandas as pd                                              #----import module ---
import matplotlib.pyplot as plt
from datetime import datetime ,timedelta
import json
import os
# .                                                               # ---- data handling ----
# file to store expenses 
data_file = "expenses.json"
budget_file = "budgets.json"
category_file = "custom_categories.json"

# load existing data
def load_data():
    if os.path.exists(data_file):
        with open(data_file,'r') as file:
            return json.load(file)
    return[]

# save data to file        
def save_data(data):
    with open(data_file,'w') as file:
        json.dump(data,file, indent = 4)

# Predefined categories 
categories = {
    "groceries":"food",
    "travel":"train,bus,taxi,auto", 
    "stationer":"pen,pencile,book",
    "fees":"college fees",
    "bill":"electricity bill or rent"
}

# Load custom categories                                           ----category section----
def load_custom_categories():
    if os.path.exists(category_file):
        with open(category_file, 'r') as file:
            return json.load(file)
    return {}

# Save custom categories
def save_custom_categories(custom_cats):
    with open(category_file, 'w') as file:
        json.dump(custom_cats, file, indent=4)

# Manage custom categories
def manage_categories():
    custom_cats = load_custom_categories()
    while True:
        print("\nCategory Management:")
        print("1. View Custom Categories")
        print("2. Add Category")
        print("3. Edit Category")
        print("4. Remove Category")
        print("5. Back to Main Menu")
        choice = input("Select an option (1-5): ")

        if choice == '1':
            print("\nCustom Categories:")
            for cat in custom_cats:
                print(f"- {cat}")
        elif choice == '2':
            new_cat = input("Enter new category name: ")
            custom_cats[new_cat] = "User-added"
            print(f"Category '{new_cat}' added.")
        elif choice == '3':
            old_cat = input("Enter existing category name to edit: ")
            if old_cat in custom_cats:
                new_cat = input("Enter new category name: ")
                custom_cats[new_cat] = custom_cats.pop(old_cat)
                print(f"Category '{old_cat}' updated to '{new_cat}'.")
            else:
                print("Category not found.")
        elif choice == '4':
            cat_to_remove = input("Enter category name to remove: ")
            if cat_to_remove in custom_cats:
                del custom_cats[cat_to_remove]
                print(f"Category '{cat_to_remove}' removed.")
            else:
                print("Category not found.")
        elif choice == '5':
            break
        else:
            print("Invalid option.")

    save_custom_categories(custom_cats)

# Load budget data                                              ----budget section ----
def load_budgets():
    if os.path.exists(budget_file):
        with open(budget_file, 'r') as file:
            return json.load(file)
    return {}

# Save budget data
def save_budgets(budgets):
    with open(budget_file, 'w') as file:
        json.dump(budgets, file, indent=4)

# Set or check category budgets
def set_and_check_budgets():
    data = load_data()
    if not data:
        print("No expense data available.")
        return

    df = pd.DataFrame(data)
    category_totals = df.groupby("category")["amount"].sum().to_dict()
    budgets = load_budgets()

    print("\n--- Set or Update Budgets for Categories ---")
    for cat in category_totals:
        current_budget = budgets.get(cat, None)
        print(f"Category: {cat}")
        print(f"Current Spending: ₹{category_totals[cat]:.2f}")
        if current_budget:
            print(f"Existing Budget: ₹{current_budget}")
        try:
            new_budget = float(input(f"Enter new budget for '{cat}' (or press Enter to keep current): ") or current_budget or 0)
            budgets[cat] = new_budget
        except ValueError:
            print("Invalid input. Skipping...")

    save_budgets(budgets)

    print("\n--- Budget Status ---")
    for cat in category_totals:
        spent = category_totals[cat]
        budget = budgets.get(cat, None)
        if budget is not None:
            if spent > budget:
                print(f"⚠  Over Budget for '{cat}' - Spent: ₹{spent:.2f} / Budget: ₹{budget:.2f}")
            else:
                print(f"✅ Within Budget for '{cat}' - Spent: ₹{spent:.2f} / Budget: ₹{budget:.2f}")
        else:
            print(f"ℹ  No budget set for '{cat}' - Spent: ₹{spent:.2f}")

# add expenses                                                          ---- expense add section ----
def add_expense():
    data = load_data()
    custom_cats = load_custom_categories()

    try:
        amount = float(input("enter amount:"))
    except ValueError:
        print("Invalid entry")
        return

    description = input("enter description")

    print("\nAvailable Categories:")
    for cat in list(categories) + list(custom_cats):
        print("-", cat)

    category = input("enter your category: ")
    if category not in categories and category not in custom_cats:
        add_custom = input("Category not found. Do you want to add it as custom? (y/n): ")
        if add_custom.lower() == 'y':
            custom_cats[category] = "User-added"
            save_custom_categories(custom_cats)
        else:
            print("Expense not recorded.")
            return

    date = datetime.today().date().isoformat()

    # add all the data 
    data.append({
        "amount":amount,
        "description":description,
        "category":category,
        "date":date
    })

    save_data(data)
    print("Expense recorded successfully")

# summary                                                           ---- Summary and analysis -----
def view_summary():
    data = load_data()
    if not data:
        print("No data available.")
        return

    df = pd.DataFrame(data)

    category_filter = input("Do you want to filter by category? (y/n): ").lower()
    if category_filter == 'y':
        selected_category = input("Enter category to filter: ")
        df = df[df['category'] == selected_category]

    print("\n--- Expense Summary ---")
    print(df.groupby("category")["amount"].sum())
    print("Total Spending: ₹{:.2f}".format(df["amount"].sum()))

    df["date"] = pd.to_datetime(df["date"])
    print("Average Daily Expense: ₹{:.2f}".format(df.groupby(df.date.dt.date)["amount"].sum().mean()))
    print("Average Weekly Expense: ₹{:.2f}".format(df.groupby(df.date.dt.isocalendar().week)["amount"].sum().mean()))
    print("Average Monthly Expense: ₹{:.2f}".format(df.groupby(df.date.dt.month)["amount"].sum().mean()))

# filter by period                                          ----- filter by period -----
def view_by_period():
    data = load_data()
    if not data:
        print("No data available.")
        return

    print("\nChoose period to filter by:")
    print("1. Today")
    print("2. Last 7 days")
    print("3. This month")
    choice = input("Enter your choice (1-3): ")

    today = datetime.today().date()

    if choice == '1':
        start_date = today
    elif choice == '2':
        start_date = today - timedelta(days=7)
    elif choice == '3':
        start_date = today.replace(day=1)
    else:
        print("Invalid choice.")
        return

    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"]).dt.date
    filtered = df[df["date"] >= start_date]

    category_filter = input("Do you want to filter by category? (y/n): ").lower()
    if category_filter == 'y':
        selected_category = input("Enter category to filter: ")
        filtered = filtered[filtered['category'] == selected_category]

    if filtered.empty:
        print("No expenses found for this period.")
    else:
        print("\n--- Expenses ---")
        for _, row in filtered.iterrows():
            print(f"{row['date']} | {row['category']}: ₹{row['amount']:.2f} - {row['description']}")

        print("\n--- Grouped Summary ---")
        print(filtered.groupby("category")["amount"].sum())

# Visualization 
def visualize():
    data = load_data()
    if not data:
        print("no data to visualize")
        return

    df = pd.DataFrame(data)
    summary = df.groupby("category")["amount"].sum()
    summary.plot(kind="bar", color="#3498db", figsize=(8, 5))
    plt.title("---Expense Summary Visualization---")
    plt.xlabel("categories")
    plt.ylabel("total expense")
    plt.grid(axis = 'y', linestyle = '--', alpha = 0.7)
    plt.tight_layout()
    plt.show()

# export to excel
def export_to_excel():
    data = load_data()
    if not data:
        print("No data to export.")
        return
    df = pd.DataFrame(data)
    df.to_excel("expenses_export.xlsx", index=False)
    print("Data exported to expenses_export.xlsx")

# find highest and lowest expense 
def highest_lowest():
    data = load_data()
    if not data:
        print("no data available")
        return

    df = pd.DataFrame(data)
    highest = df.loc[df["amount"].idxmax()]
    lowest = df.loc[df["amount"].idxmin()]

    print(f"Highest Expense: ₹{highest['amount']} | {highest['description']} | {highest['category']} | {highest['date']}")
    print(f"Lowest Expense: ₹{lowest['amount']} | {lowest['description']} | {lowest['category']} | {lowest['date']}")

# search expense 
def search_expense():
    keyword = input("enter your keyword to search:").lower()
    data = load_data()
    results = [exp for exp in data if keyword in exp["description"].lower() or keyword in exp["category"].lower()]

    if results:
        print("\n--- Search Results ---")
        for row in results:
            print(f"{row['date']} | {row['category']}: ₹{row['amount']:.2f} - {row['description']}")
    else:
        print("No matching records found.")

# Main menu
def main():
    while True:
        print("\nMenu:")
        print("1. Add Expense")
        print("2. View Summary")
        print("3. Visualize (Bar Chart)")
        print("4. View by Period")
        print("5. Export to Excel")
        print("6. Highest & Lowest Expense")
        print("7. Search Expense")
        print("8. Set & Check Budgets")
        print("9. Manage Categories")
        print("10. Exit")
        choice = input("Select an option (1-10): ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_summary()
        elif choice == '3':
            visualize()
        elif choice == '4':
            view_by_period()
        elif choice == '5':
            export_to_excel()
        elif choice == '6':
            highest_lowest()
        elif choice == '7':
            search_expense()
        elif choice == '8':
            set_and_check_budgets()
        elif choice == '9':
            manage_categories()
        elif choice == '10':
            print("Thank you! Exiting...")
            break
        else:
            print("Invalid option.")


# Run the program
if __name__ == "__main__":
    main()
print("All done ...bye bye!")