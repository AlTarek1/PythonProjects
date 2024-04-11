import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")

        self.create_widgets()

    def create_widgets(self):
        # Create labels and entries
        self.labels = ["Amount:", "Currency:", "Category:", "Date (YYYY-MM-DD):", "Payment Method:"]
        self.entries = {}

        for i, label_text in enumerate(self.labels):
            label = ttk.Label(self.root, text=label_text)
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
            if label_text == "Currency:":
                entry = ttk.Combobox(self.root, state="readonly")
            elif label_text == "Category:":
                entry = ttk.Combobox(self.root, state="readonly", values=["Life Expenses", "Gas", "Rental", "Grocery", "Savings", "Education", "Charity"])
            elif label_text == "Payment Method:":
                entry = ttk.Combobox(self.root, state="readonly", values=["Cash", "Credit Card", "Paypal"])
            else:
                entry = ttk.Entry(self.root)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            self.entries[label_text] = entry

        # Create add expense button
        self.add_button = ttk.Button(self.root, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=len(self.labels), column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # Create expenses table
        self.expenses_treeview = ttk.Treeview(self.root, columns=("Amount", "Currency", "Category", "Payment Method"), show="headings")
        self.expenses_treeview.grid(row=len(self.labels) + 1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        for col in ("Amount", "Currency", "Category", "Payment Method"):
            self.expenses_treeview.heading(col, text=col, anchor=tk.CENTER)

        # Create total row for sum of amounts
        self.total_row_id = None

        # Update currency options
        self.update_currency()

    def update_currency(self):
        response = requests.get("https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_gFjthjtzhcIA0z8sHnWuUTcBaV1eV44MVUUOtbL9")
        if response.status_code == 200:
            data = response.json()
            currencies = list(data['data'].keys())
            self.entries["Currency:"]["values"] = currencies

    def add_expense(self):
        # Get values from entries
        values = {label: entry.get() for label, entry in self.entries.items()}
        
        # Validate date
        try:
            datetime.strptime(values["Date (YYYY-MM-DD):"], "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return

        # Validate amount as integer
        try:
            amount = int(values["Amount:"])
        except ValueError:
            messagebox.showerror("Error", "Amount must be an integer.")
            return

        # Validate non-empty fields
        for label, value in values.items():
            if not value:
                messagebox.showerror("Error", f"Please fill in {label}.")
                return

        # Remove existing total row
        if self.total_row_id:
            self.expenses_treeview.delete(self.total_row_id)

        # Insert expense into treeview
        self.expenses_treeview.insert("", "end", values=list(values.values()))

        # Calculate and add the sum of amounts in USD to the expenses view list
        total_usd = self.calculate_total_usd()
        self.total_row_id = self.expenses_treeview.insert("", "end", values=(total_usd, "USD", "", ""), tags=("total_row",))

        # Clear entries
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def calculate_total_usd(self):
        total_usd = 0
        for item in self.expenses_treeview.get_children():
            values = self.expenses_treeview.item(item)["values"]
            amount = values[0]
            currency = values[1]
            if currency == "USD":
                total_usd += float(amount)
            else:
                # Convert amount to USD using the conversion rate from the API
                conversion_rate = self.get_conversion_rate(currency)
                total_usd += float(amount) * float(conversion_rate)  # Convert amount to float
        return round(total_usd, 2)

    def get_conversion_rate(self, currency):
        response = requests.get(f"https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_gFjthjtzhcIA0z8sHnWuUTcBaV1eV44MVUUOtbL9&base={currency}")
        if response.status_code == 200:
            data = response.json()
            conversion_rate = data['data'][currency]
            return conversion_rate
        else:
            return 1  # Default conversion rate if API call fails

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
