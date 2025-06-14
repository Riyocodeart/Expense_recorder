This is a personal **Expense Tracker Application**.It allows users to easily add, manage, and visualize their daily expenses with both default and custom categories.
# 🧾 Expense Tracker GUI (Python + Tkinter + Matplotlib + Pandas + JSON)
## 📌 Features

- ✅ **Add Expenses** with amount, description, date, and category.
- 🗂️ **Default and Custom Categories** supported.<br>
  
![Expense recorder system](image.png)<br>

- **Total expense summary<br> 
![Summary](image-1.png)<br>
- 📊 **Visualize Expenses**: View bar charts of your spending by category.<br>
![Visualization](image-2a.png)<br>
- ⬆️ **Export to Excel (.xlsx)**.<br>
![Export to excel](image-2.png)<br>
- 📆 **View by Period**: Filter expenses by today, last 7 days, or this month.<br>
![view by period](image-3.png)<br>
- 📉 **View Highest & Lowest Expenses**.<br>
![highest lowest expense](image-4.png)<br>
- 🔍 **Search Functionality**: Search expenses by keyword or date.<br>
![search](image-8.png)<br>
- 💰 **Set & Check Budgets**: Define monthly budgets per category and get alerts when overspending.<br>
![budget](image-6.png)<br>
![set budget](image-9.png)<br>
- 🧩 **Category Management**: Add, edit, or delete custom categories.<br>



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


- UI is styled with light pastel colors (`#e6f2ff`) for a clean user experience.

---

💡 Happy Budgeting!
