# 🧾 Expense Tracker GUI (Python + Tkinter)
output:
![Expense recorder system](image.png)
![summary](image-8.png)
![Visualization](image-7.png)
![view by period](image-3.png)
![highest lowest expense](image-4.png)
![Search](image-5.png)
![budget](image-6.png)

This is a personal **Expense Tracker Application** built using **Python** and **Tkinter**. It allows users to easily add, manage, and visualize their daily expenses with both default and custom categories.

## 📌 Features

- ✅ **Add Expenses** with amount, description, date, and category.
- 🗂️ **Default and Custom Categories** supported.
- 📆 **View by Period**: Filter expenses by today, last 7 days, or this month.
- 💰 **Set & Check Budgets**: Define monthly budgets per category and get alerts when overspending.
- 📊 **Visualize Expenses**: View bar charts of your spending by category.
- 🔍 **Search Functionality**: Search expenses by keyword or date.
- ⬆️ **Export to Excel (.xlsx)**.
- 📉 **View Highest & Lowest Expenses**.
- 🧩 **Category Management**: Add, edit, or delete custom categories.

## 🚀 How to Run

1. **Install Python** (version 3.7 or higher).
2. Install dependencies:

    ```bash
    pip install pandas matplotlib openpyxl
    ```

3. **Run the app**:

    ```bash
    python expense_tracker_gui.py
    ```

## 📁 File Structure

- `expenses.json`: Stores all expense entries.
- `custom_categories.json`: Stores user-defined categories.
- `budgets.json`: Stores budget limits for categories.

## 🛠 Technologies Used

- `Tkinter`: GUI framework
- `Pandas`: Data analysis and grouping
- `Matplotlib`: Charts and visualizations
- `JSON`: Local data storage
- `Openpyxl`: Excel file export

## 📝 Notes

- Default categories are always loaded even if no custom ones exist.
- Placeholder functions are already set for features like **View by Period**, **Budget**, and **Category Management** — customize them as needed.
- UI is styled with light pastel colors (`#e6f2ff`) for a clean user experience.

---

💡 Happy Budgeting!
