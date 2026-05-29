import customtkinter as ctk
from tkinter import messagebox

class App(ctk.CTk):
    def __init__(self, banco):
        super().__init__()
        self.title("Filtro de Receitas")
        self.geometry("820x650")
        self.banco = banco

        self.main_frame = ctk.CTkFrame(self, width=800, height=600)
        self.main_frame.place(x=10, y=10)

        # Campo de filtro
        lbl_filtro = ctk.CTkLabel(self.main_frame, text="Filtrar por descrição:", font=("Arial", 16))
        lbl_filtro.place(x=20, y=20)

        self.entry_filtro = ctk.CTkEntry(self.main_frame, width=300)
        self.entry_filtro.place(x=200, y=20)

        btn_filtrar = ctk.CTkButton(self.main_frame, text="Aplicar Filtro", width=150, command=self.aplicar_filtro)
        btn_filtrar.place(x=520, y=20)

        # Frame para lista
        self.scroll_frame = ctk.CTkScrollableFrame(self.main_frame, width=770, height=500)
        self.scroll_frame.place(x=20, y=70)

        self.listar_receitas()

    def limpar_lista(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

    def listar_receitas(self, filtro=""):
        self.limpar_lista()

        try:
            receitas = self.banco.listar_receitas()

            # Aplica filtro (case insensitive)
            if filtro:
                receitas = [r for r in receitas if filtro.lower() in r[1].lower()]

            if not receitas:
                vazio = ctk.CTkLabel(self.scroll_frame, text="Nenhuma receita encontrada.", font=("Arial", 16))
                vazio.place(x=10, y=10)
            else:
                for i, receita in enumerate(receitas):
                    id_pg, descricao, valor, tipo, status = receita
                    try:
                        valor = float(valor)
                    except ValueError:
                        valor = 0.0

                    texto = f"ID: {id_pg} | {descricao} - R$ {valor:.2f} | Tipo: {tipo} | Status: {status}"

                    bg_color = "#3065AC" if i % 2 == 0 else "#333333"
                    fg_color = "#FFFFFF"

                    item_frame = ctk.CTkFrame(self.scroll_frame, fg_color=bg_color, width=740, height=60)
                    item_frame.place(x=10, y=10 + (i * 65))

                    item_label = ctk.CTkLabel(item_frame, text=texto, anchor="w", font=("Arial", 18), text_color=fg_color)
                    item_label.place(x=10, y=15)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar receitas: {e}")

    def aplicar_filtro(self):
        filtro = self.entry_filtro.get()
        self.listar_receitas(filtro)


# ----------------------------
# Banco mock para teste
# ----------------------------
class BancoMock:
    def listar_receitas(self):
        return [
            (1, "Salário", 3500.00, "Entrada", "Ativo"),
            (2, "Freelance", 1200.00, "Entrada", "Ativo"),
            (3, "Investimento", 500.00, "Entrada", "Pendente"),
            (4, "Aluguel", 1500.00, "Saída", "Pago"),
        ]


if __name__ == "__main__":
    banco = BancoMock()
    app = App(banco)
    app.mainloop()
