import tkinter as tk
from tkinter import ttk
import sqlite3
from tkcalendar import DateEntry
import pandas as pd

class SalesViewScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Sales View")
        self.root.geometry("800x600")

        # Filters: Initial Date, Final Date, and Payment Method
        tk.Label(self.root, text="Initial Date").grid(row=0, column=0, padx=10, pady=10)
        self.initial_date = DateEntry(self.root, width=12, background='darkblue',
                                      foreground='white', borderwidth=2, year=2023)
        self.initial_date.grid(row=0, column=1)

        tk.Label(self.root, text="Final Date").grid(row=0, column=2, padx=10, pady=10)
        self.final_date = DateEntry(self.root, width=12, background='darkblue',
                                    foreground='white', borderwidth=2, year=2023)
        self.final_date.grid(row=0, column=3)

        tk.Label(self.root, text="Payment Method").grid(row=0, column=4, padx=10, pady=10)
        self.payment_method = ttk.Combobox(self.root, values=["All", "Cash", "Debit", "Credit"])
        self.payment_method.grid(row=0, column=5)
        self.payment_method.set("All")

        # Search Button
        search_button = tk.Button(self.root, text="Search", command=self.search_sales)
        search_button.grid(row=0, column=6, padx=10)

        # Treeview for displaying sales
        self.sales_tree = ttk.Treeview(self.root, columns=("date", "venda_id", "produto_id", "descricao", 
                                                           "quantidade", "valor_produto", "valor_venda", 
                                                           "forma_pagamento"), show="headings")
        self.sales_tree.heading("date", text="Date")
        self.sales_tree.heading("venda_id", text="Venda ID")
        self.sales_tree.heading("produto_id", text="Produto ID")
        self.sales_tree.heading("descricao", text="Description")
        self.sales_tree.heading("quantidade", text="Quantity")
        self.sales_tree.heading("valor_produto", text="Product Value")
        self.sales_tree.heading("valor_venda", text="Sale Value")
        self.sales_tree.heading("forma_pagamento", text="Payment Method")
        self.sales_tree.grid(row=1, column=0, columnspan=7, padx=10, pady=10, sticky="nsew")

        # Button to generate Excel report
        self.export_button = tk.Button(self.root, text="Generate Report", command=self.generate_report)
        self.export_button.grid(row=2, column=6, padx=10, pady=10)

    def search_sales(self):
        # Fetch sales data from database based on the filters
        conn = sqlite3.connect('sistema_caixa.db')
        cursor = conn.cursor()

        query = '''
        SELECT vendas.data_venda, vendas.id, venda_produto.produto_id, produtos.descricao, venda_produto.quantidade, 
               venda_produto.valor_total, vendas.valor_total, vendas.forma_pagamento
        FROM vendas
        JOIN venda_produto ON vendas.id = venda_produto.venda_id
        JOIN produtos ON venda_produto.produto_id = produtos.produto_id
        WHERE vendas.data_venda BETWEEN ? AND ?
        '''
        params = [self.initial_date.get_date(), self.final_date.get_date()]

        if self.payment_method.get() != "All":
            query += " AND vendas.forma_pagamento = ?"
            params.append(self.payment_method.get())

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        # Clear existing rows in Treeview
        for row in self.sales_tree.get_children():
            self.sales_tree.delete(row)

        # Insert fetched rows into the Treeview
        for row in rows:
            self.sales_tree.insert('', 'end', values=row)

    def generate_report(self):
        # Fetch the data displayed in the Treeview
        rows = [self.sales_tree.item(item)["values"] for item in self.sales_tree.get_children()]

        # Create a DataFrame and export to Excel
        df = pd.DataFrame(rows, columns=["Date", "Venda ID", "Produto ID", "Description", 
                                         "Quantity", "Product Value", "Sale Value", "Payment Method"])
        file_path = "sales_report.xlsx"
        df.to_excel(file_path, index=False)
        tk.messagebox.showinfo("Report Generated", f"Report saved as {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SalesViewScreen(root)
    root.mainloop()
