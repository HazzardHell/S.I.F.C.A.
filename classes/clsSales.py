import tkinter as tk
from tkinter import messagebox

class SalesScreen(tk.Frame):
    def __init__(self, parent, cursor, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.cursor = cursor
        
        # Labels and Entry fields for product ID, quantity, etc.
        self.label_produto = tk.Label(self, text="Product ID:")
        self.label_produto.grid(row=0, column=0)
        self.entry_produto = tk.Entry(self)
        self.entry_produto.grid(row=0, column=1)

        self.label_quantidade = tk.Label(self, text="Quantity:")
        self.label_quantidade.grid(row=1, column=0)
        self.entry_quantidade = tk.Entry(self)
        self.entry_quantidade.grid(row=1, column=1)

        self.button_add = tk.Button(self, text="Add Product", command=self.add_product)
        self.button_add.grid(row=2, column=0, columnspan=2)

        self.sales_items = []  # Store products for this sale
        
        self.total_label = tk.Label(self, text="Total: $0.00")
        self.total_label.grid(row=3, column=0, columnspan=2)
        
        self.button_finalize = tk.Button(self, text="Finalize Sale", command=self.finalize_sale)
        self.button_finalize.grid(row=4, column=0, columnspan=2)
    
    def add_product(self):
        product_id = self.entry_produto.get()
        quantity = int(self.entry_quantidade.get())
        
        # Fetch product details from the database
        self.cursor.execute("SELECT descricao, preco_unitario FROM produtos WHERE produto_id=?", (product_id,))
        product = self.cursor.fetchone()
        
        if product:
            descricao, preco_unitario = product
            valor_total = preco_unitario * quantity
            self.sales_items.append({
                'produto_id': product_id,
                'quantidade': quantity,
                'preco_unitario': preco_unitario,
                'valor_total': valor_total
            })
            # Update the total displayed on the screen
            total_value = sum(item['valor_total'] for item in self.sales_items)
            self.total_label.config(text=f"Total: ${total_value:.2f}")
        else:
            messagebox.showerror("Error", "Product not found!")
    
    def finalize_sale(self):
        if not self.sales_items:
            messagebox.showerror("Error", "No products added to the sale!")
            return
        
        # Insert the sale in the 'vendas' table
        total_value = sum(item['valor_total'] for item in self.sales_items)
        self.cursor.execute("INSERT INTO vendas (valor_total, forma_pagamento) VALUES (?, ?)", (total_value, "Cash"))
        sale_id = self.cursor.lastrowid
        
        # Insert each product into the 'venda_produtos' table
        for item in self.sales_items:
            self.cursor.execute('''INSERT INTO venda_produtos (venda_id, produto_id, quantidade, preco_unitario, valor_total)
                                   VALUES (?, ?, ?, ?, ?)''', 
                                   (sale_id, item['produto_id'], item['quantidade'], item['preco_unitario'], item['valor_total']))
        
        # Clear the screen after saving
        self.sales_items.clear()
        self.entry_produto.delete(0, tk.END)
        self.entry_quantidade.delete(0, tk.END)
        self.total_label.config(text="Total: $0.00")
        messagebox.showinfo("Success", "Sale registered successfully!")

