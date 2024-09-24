import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class SalesScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Register Sales")
        self.root.geometry("800x600")
        
        # Database connection
        self.conn = sqlite3.connect('sistema_caixa.db')  # Replace with your DB name
        self.cursor = self.conn.cursor()
        
        # Load products from the database
        self.products = self.load_products()
        
        # Initialize the shopping cart
        self.cart_items = []
        
        # UI Elements
        self.create_widgets()
    
    def load_products(self):
        """Load products from the 'produtos' table."""
        self.cursor.execute("SELECT id, descricao, preco_unitario FROM produtos")
        products = self.cursor.fetchall()
        # Convert to a dictionary for easy lookup
        return {str(prod[0]): {'descricao': prod[1], 'preco_unitario': prod[2]} for prod in products}
    
    def create_widgets(self):
        # Product Selection Frame
        product_frame = tk.Frame(self.root)
        product_frame.pack(pady=10)
        
        # Product Code Entry
        tk.Label(product_frame, text="Product ID:").grid(row=0, column=0, padx=5)
        self.product_id_entry = tk.Entry(product_frame)
        self.product_id_entry.grid(row=0, column=1, padx=5)
        
        # OR Product Name Dropdown
        tk.Label(product_frame, text="or Select Product:").grid(row=0, column=2, padx=5)
        self.product_name_var = tk.StringVar()
        self.product_name_combobox = ttk.Combobox(product_frame, textvariable=self.product_name_var)
        self.product_name_combobox['values'] = [prod['descricao'] for prod in self.products.values()]
        self.product_name_combobox.grid(row=0, column=3, padx=5)
        self.product_name_combobox.bind("<<ComboboxSelected>>", self.on_product_select)
        
        # Price Display
        tk.Label(product_frame, text="Price:").grid(row=1, column=0, padx=5)
        self.price_var = tk.StringVar(value="0.00")
        self.price_label = tk.Label(product_frame, textvariable=self.price_var)
        self.price_label.grid(row=1, column=1, padx=5)
        
        # Quantity Entry
        tk.Label(product_frame, text="Quantity:").grid(row=1, column=2, padx=5)
        self.quantity_entry = tk.Entry(product_frame)
        self.quantity_entry.insert(0, "1")
        self.quantity_entry.grid(row=1, column=3, padx=5)
        
        # Add to Cart Button
        self.add_to_cart_button = tk.Button(product_frame, text="Add to Cart", command=self.add_to_cart)
        self.add_to_cart_button.grid(row=2, column=0, columnspan=4, pady=10)
        
        # Shopping Cart Frame
        cart_frame = tk.Frame(self.root)
        cart_frame.pack(pady=10)
        
        # Cart Items List
        self.cart_tree = ttk.Treeview(cart_frame, columns=('Product ID', 'Description', 'Quantity', 'Unit Price', 'Total Price'), show='headings')
        self.cart_tree.heading('Product ID', text='Product ID')
        self.cart_tree.heading('Description', text='Description')
        self.cart_tree.heading('Quantity', text='Quantity')
        self.cart_tree.heading('Unit Price', text='Unit Price')
        self.cart_tree.heading('Total Price', text='Total Price')
        self.cart_tree.pack()
        
        # Remove and Clear Cart Buttons
        self.remove_item_button = tk.Button(cart_frame, text="Remove Selected Item", command=self.remove_item)
        self.remove_item_button.pack(side='left', padx=5)
        self.clear_cart_button = tk.Button(cart_frame, text="Clear Cart", command=self.clear_cart)
        self.clear_cart_button.pack(side='left', padx=5)
        
        # Total Amount Label
        total_frame = tk.Frame(self.root)
        total_frame.pack(pady=10)
        tk.Label(total_frame, text="Total Amount:").pack(side='left')
        self.total_amount_var = tk.StringVar(value="0.00")
        tk.Label(total_frame, textvariable=self.total_amount_var, font=("Helvetica", 14)).pack(side='left')
        
        # Payment Method Selection
        payment_frame = tk.Frame(self.root)
        payment_frame.pack(pady=10)
        tk.Label(payment_frame, text="Payment Method:").pack(side='left')
        self.payment_method_var = tk.StringVar(value="Cash")
        payment_methods = ["Cash", "Debit", "Credit"]
        self.payment_method_menu = ttk.Combobox(payment_frame, textvariable=self.payment_method_var, values=payment_methods, state="readonly")
        self.payment_method_menu.pack(side='left')
        
        # Register Sale Button
        self.register_sale_button = tk.Button(self.root, text="Register Sale", command=self.register_sale)
        self.register_sale_button.pack(pady=20)
    
    def on_product_select(self, event):
        """Event handler when a product is selected from the dropdown."""
        selected_product_name = self.product_name_var.get()
        # Find product ID based on the description
        for prod_id, details in self.products.items():
            if details['descricao'] == selected_product_name:
                # Set the product ID in the entry field
                self.product_id_entry.delete(0, tk.END)
                self.product_id_entry.insert(0, prod_id)
                # Update the price
                self.price_var.set(f"{details['preco_unitario']:.2f}")
                break
    
    def add_to_cart(self):
        """Add the selected product to the cart."""
        product_id = self.product_id_entry.get()
        quantity = self.quantity_entry.get()
        
        if not product_id or not quantity:
            messagebox.showerror("Error", "Please enter a product ID and quantity.")
            return
        
        if product_id not in self.products:
            messagebox.showerror("Error", "Product ID not found.")
            return
        
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a positive integer.")
            return
        
        product = self.products[product_id]
        unit_price = product['preco_unitario']
        total_price = unit_price * quantity
        
        # Add to cart items
        cart_item = {
            'product_id': product_id,
            'descricao': product['descricao'],
            'quantidade': quantity,
            'preco_unitario': unit_price,
            'valor_total': total_price
        }
        self.cart_items.append(cart_item)
        
        # Update the cart display
        self.cart_tree.insert('', tk.END, values=(product_id, product['descricao'], quantity, f"{unit_price:.2f}", f"{total_price:.2f}"))
        
        # Update the total amount
        self.update_total_amount()
        
        # Clear input fields
        self.product_id_entry.delete(0, tk.END)
        self.product_name_var.set('')
        self.price_var.set("0.00")
        self.quantity_entry.delete(0, tk.END)
        self.quantity_entry.insert(0, "1")
    
    def remove_item(self):
        """Remove the selected item from the cart."""
        selected_item = self.cart_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No item selected.")
            return
        # Remove from cart_items
        item_index = self.cart_tree.index(selected_item)
        del self.cart_items[item_index]
        # Remove from treeview
        self.cart_tree.delete(selected_item)
        # Update total amount
        self.update_total_amount()
    
    def clear_cart(self):
        """Clear all items from the cart."""
        self.cart_items.clear()
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        self.update_total_amount()
    
    def update_total_amount(self):
        """Calculate and update the total amount."""
        total = sum(item['valor_total'] for item in self.cart_items)
        self.total_amount_var.set(f"{total:.2f}")
    
    def register_sale(self):
        """Finalize the sale and save to the database."""
        if not self.cart_items:
            messagebox.showerror("Error", "Cart is empty.")
            return
        
        total_amount = sum(item['valor_total'] for item in self.cart_items)
        payment_method = self.payment_method_var.get()
        
        # Insert into 'vendas' table
        self.cursor.execute("INSERT INTO vendas (valor_total, forma_pagamento) VALUES (?, ?)", (total_amount, payment_method))
        sale_id = self.cursor.lastrowid
        
        # Insert into 'venda_produtos' table
        for item in self.cart_items:
            self.cursor.execute(
                '''INSERT INTO venda_produtos (venda_id, produto_id, quantidade, preco_unitario, valor_total)
                   VALUES (?, ?, ?, ?, ?)''',
                (sale_id, item['product_id'], item['quantidade'], item['preco_unitario'], item['valor_total'])
            )
        
        # Commit the transaction
        self.conn.commit()
        
        # Clear the cart and reset
        self.clear_cart()
        messagebox.showinfo("Success", "Sale registered successfully!")
    
    def __del__(self):
        # Close the database connection when the window is closed
        self.conn.close()
