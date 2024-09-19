import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class ProdutosScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Product Management")
        self.root.geometry("600x400")

        # Frame for buttons (Add, Remove, Update) at the top
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        # Add buttons to the button_frame
        self.add_button = tk.Button(button_frame, text="Add Product", command=self.add_product)
        self.add_button.pack(side=tk.LEFT, padx=10)

        self.remove_button = tk.Button(button_frame, text="Remove Product", command=self.remove_product)
        self.remove_button.pack(side=tk.LEFT, padx=10)

        self.update_button = tk.Button(button_frame, text="Update Product", command=self.update_product)
        self.update_button.pack(side=tk.LEFT, padx=10)

        # Frame for the product list (Treeview)
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        # Create Treeview to display products
        self.tree = ttk.Treeview(frame, columns=("descricao", "preco_unitario"), show="headings")
        self.tree.heading("descricao", text="Description")
        self.tree.heading("preco_unitario", text="Unit Price")
        self.tree.pack()

        # Load the products from the database
        self.load_products()

    def load_products(self):
        """Fetch and display products from the 'produtos' table."""
        # Clear the existing data
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Connect to the database and fetch products
        conn = sqlite3.connect('sistema_caixa.db')
        cursor = conn.cursor()
        cursor.execute("SELECT descricao, preco_unitario FROM produtos")
        rows = cursor.fetchall()

        # Insert products into the Treeview
        for row in rows:
            self.tree.insert('', tk.END, values=row)

        conn.close()

    def add_product(self):
        """Open a new window to add a product."""
        new_window = tk.Toplevel(self.root)
        new_window.title("Add Product")
        tk.Label(new_window, text="Description").pack(pady=5)
        desc_entry = tk.Entry(new_window)
        desc_entry.pack(pady=5)

        tk.Label(new_window, text="Unit Price").pack(pady=5)
        price_entry = tk.Entry(new_window)
        price_entry.pack(pady=5)

        def save_product():
            desc = desc_entry.get()
            price = price_entry.get()
            if desc and price:
                conn = sqlite3.connect('sistema_caixa.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO produtos (descricao, preco_unitario) VALUES (?, ?)", (desc, price))
                conn.commit()
                conn.close()
                self.load_products()  # Reload product list
                new_window.destroy()
            else:
                messagebox.showerror("Error", "All fields are required.")

        save_button = tk.Button(new_window, text="Save", command=save_product)
        save_button.pack(pady=10)

    def remove_product(self):
        """Remove the selected product."""
        selected_item = self.tree.selection()
        if selected_item:
            product = self.tree.item(selected_item, 'values')
            descricao = product[0]
            conn = sqlite3.connect('sistema_caixa.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM produtos WHERE descricao = ?", (descricao,))
            conn.commit()
            conn.close()
            self.load_products()  # Reload product list
        else:
            messagebox.showerror("Error", "No product selected.")

    def update_product(self):
        """Open a new window to update the selected product."""
        selected_item = self.tree.selection()
        if selected_item:
            product = self.tree.item(selected_item, 'values')
            old_desc, old_price = product

            new_window = tk.Toplevel(self.root)
            new_window.title("Update Product")

            tk.Label(new_window, text="Description").pack(pady=5)
            desc_entry = tk.Entry(new_window)
            desc_entry.pack(pady=5)
            desc_entry.insert(0, old_desc)

            tk.Label(new_window, text="Unit Price").pack(pady=5)
            price_entry = tk.Entry(new_window)
            price_entry.pack(pady=5)
            price_entry.insert(0, old_price)

            def save_update():
                new_desc = desc_entry.get()
                new_price = price_entry.get()
                conn = sqlite3.connect('sistema_caixa.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE produtos SET descricao = ?, preco_unitario = ? WHERE descricao = ?", (new_desc, new_price, old_desc))
                conn.commit()
                conn.close()
                self.load_products()  # Reload product list
                new_window.destroy()

            save_button = tk.Button(new_window, text="Save", command=save_update)
            save_button.pack(pady=10)
        else:
            messagebox.showerror("Error", "No product selected.")
