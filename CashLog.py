import sqlite3
from datetime import datetime

class ExpenseTracker:
    def __init__(self):
        self.conn = sqlite3.connect('expenses.db')
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS expenses
                             (id INTEGER PRIMARY KEY, 
                             amount REAL, category TEXT, 
                             date TEXT, description TEXT)''')
    
    def add_expense(self):
        amount = float(input("Enter amount spent: Rs"))
        category = input("Category (e.g., Food, Transport,Rent,clothes): ")
        description = input("Description (optional): ")
        self.cursor.execute('''INSERT INTO expenses (amount, category, date, description)
                             VALUES (?, ?, ?, ?)''', 
                             (amount, category, datetime.now().strftime("%Y-%m-%d"), description))
        self.conn.commit()
        print("Expense added successfully!")
    
    def generate_report(self):
        self.cursor.execute('''SELECT category, SUM(amount) FROM expenses GROUP BY category''')
        print("\n--- Monthly Report ---")
        for row in self.cursor.fetchall():
            print(f"{row[0]}: Rs{row[1]:.2f}")
        print("---------------------")

    def run(self):
        while True:
            print("\n1. Add Expense\n2. View Report\n3. Exit")
            choice = input("Choose an option (1-3): ")
            if choice == "1":
                self.add_expense()
            elif choice == "2":
                self.generate_report()
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Try again.")

# Run the tracker
if __name__ == "__main__":
    tracker = ExpenseTracker()
    tracker.run()