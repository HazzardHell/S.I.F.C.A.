import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from gui.produtos_screen import ProdutosScreen
from gui.salesscreen import SalesScreen
from gui.salesviewscreen import SalesViewScreen

class BoasVindas:
    def __init__(self, root):
        self.root = root
        self.root.title("S.I.F.C.A. 0.1")
        self.root.geometry("800x600")  # Set the initial window size

        # Load the image using Pillow
        self.original_image = Image.open("img\Empório.png")  # Replace with your image path

        # Resize the image to fit the window
        self.bg_image = ImageTk.PhotoImage(self.original_image.resize((800, 600)))
        self.bg_label = tk.Label(root, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)

        # Create a menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Add 'File' menu with 'Register Sales' and 'Exit' options
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Arquivo", menu=self.file_menu)
        self.file_menu.add_command(label="Vender", command=self.open_register_sales)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Registro de vendas", command=self.open_sales_hist)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Sair", command=self.exit)

        self.adm_menu = tk.Menu(self.menu_bar, tearoff= 0)
        self.menu_bar.add_cascade(label="Administracao",menu=self.adm_menu)
        self.adm_menu.add_command(label="Produtos", command=self.open_produtos)

        # Add 'Help' menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Ajuda", menu=self.help_menu)
        self.help_menu.add_command(label="Sobre", command=self.show_about)

        # Title
        self.title = tk.Label(root, text="Sistema Integrado de Fluxo de Caixa", font=("Helvetica", 16),fg="#444444", )
        self.title.place(relx=0.01, rely=0.95, anchor="sw")

        self.root.configure(bg='#ffffff')

        # Button to register sales (optional, can remove since it's in the menu now)
        self.register_sales_button = tk.Button(root, text="Register Sales", command=self.open_register_sales)
        self.register_sales_button.pack(pady=10)
        

        # Button to exit (optional, can remove since it's in the menu now)
        #self.exit_button = tk.Button(root, text="Exit", command=self.exit)
        #self.exit_button.pack(pady=10)

        # Bind resizing event
        self.root.bind("<Configure>", self.resize_background)

    def resize_background(self, event):
        # Resize the image to the new window size
        new_width = event.width
        new_height = event.height
        resized_image = self.original_image.resize((new_width, new_height))
        self.bg_image = ImageTk.PhotoImage(resized_image)

        # Update the background image
        self.bg_label.config(image=self.bg_image)
        self.bg_label.image = self.bg_image  # Keep a reference to prevent garbage collection

    def open_register_sales(self):
        """Open the Sales screen."""
        sales_window = tk.Toplevel(self.root)
        SalesScreen(sales_window)  # Load the Sales screen inside the new window

    def open_produtos(self):
        """Open the Produtos screen."""
        produtos_window = tk.Toplevel(self.root)
        ProdutosScreen(produtos_window)  # Load th

    def open_sales_hist(self):
        """Open the Produtos screen."""
        sales_hist_window = tk.Toplevel(self.root)
        SalesViewScreen(sales_hist_window)  # Load th

    def exit(self):
        self.root.quit()

    def show_about(self):
        # Show 'About' message
        messagebox.showinfo("About", "Cash Register System v1.0")

if __name__ == "__main__":
    root = tk.Tk()
    app = BoasVindas(root)
    root.mainloop()