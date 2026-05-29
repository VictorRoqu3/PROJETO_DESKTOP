import customtkinter as ctk

# Configuração inicial
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("400x300")
app.title("Exemplo de ListBox com CustomTkinter")

# Frame rolável que vai funcionar como listbox
list_frame = ctk.CTkScrollableFrame(app, width=200, height=200)
list_frame.pack(pady=20)

# Adicionando itens na "listbox"
items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]

def selecionar_item(item):
    print(f"Selecionado: {item}")

for i in items:
    btn = ctk.CTkButton(list_frame, text=i, width=180,
                        command=lambda x=i: selecionar_item(x))
    btn.pack(pady=5)

app.mainloop()