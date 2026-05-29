
import customtkinter as ctk
import os
from PIL import Image
from tkinter import messagebox
from tkinter import ttk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MenuPrincipal:
    def __init__(self):
        self.janela_principal = ctk.CTk()
        self.janela_principal.title("Menu Principal")
        self.janela_principal.geometry("1000x600")

        # Ícone opcional
        caminho = os.path.join(os.path.dirname(__file__), "")
        if os.path.exists(caminho):
            self.janela_principal.iconbitmap(caminho)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self.janela_principal, width=200, height=600, corner_radius=0)
        self.sidebar.place(x=0, y=0)

        titulo_sidebar = ctk.CTkLabel(self.sidebar, text="Funcionalidades", font=("Arial", 18, "bold"))
        titulo_sidebar.place(x=20, y=20)

        # Área principal
        self.main_frame = ctk.CTkFrame(self.janela_principal, width=780, height=600, corner_radius=10)
        self.main_frame.place(x=210, y=0)

        # Botões da sidebar
        botoes = [
            ("Painel principal", self.painel_principal),
            ("Cadastrar Receitas", self.cadastro_receitas),
            ("Cadastrar Pagamentos", self.cadastro_pagamentos),
            ("Despesas", self.listar_despesas),
            ("Gerar PDF", self.gerar_pdf)
        ]

        # REVER ISSO SE PRECISA OU NÃO DO Y_POS
        y_pos = 70
        for texto, comando in botoes:
            btn = ctk.CTkButton(self.sidebar, text=texto, width=160, command=comando)
            btn.place(x=20, y=y_pos)
            y_pos += 50

        # Exibe tela inicial
        self.painel_principal()

        self.janela_principal.mainloop()

    def limpar_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def painel_principal(self):
        self.limpar_main_frame()
        titulo = ctk.CTkLabel(self.main_frame, text="Orçamento pessoal", font=("Arial", 24, "bold"))
        titulo.place(x=20, y=20)

        # Frame para gráfico
        grafico_frame = ctk.CTkFrame(self.main_frame, width=500, height=200)
        grafico_frame.place(x=20, y=70)
        ctk.CTkLabel(grafico_frame, text="[Futuro gráfico aqui]", font=("Arial", 16)).place(relx=0.5, rely=0.5, anchor="center")

        # Calcula valores
        total_receitas = 200
        total_despesas = 260
        restante = total_receitas - total_despesas

        # Exibe cards com valores
        card_receitas = ctk.CTkFrame(self.main_frame, width=200, height=100, corner_radius=10)
        card_receitas.place(x=20, y=300)
        ctk.CTkLabel(card_receitas, text="Total Receitas", font=("Arial", 14)).place(relx=0.5, y=25, anchor="center")
        ctk.CTkLabel(card_receitas, text=f"R$ {total_receitas:.2f}", font=("Arial", 18, "bold")).place(relx=0.5, y=65, anchor="center")

        card_despesas = ctk.CTkFrame(self.main_frame, width=200, height=100, corner_radius=10)
        card_despesas.place(x=240, y=300)
        ctk.CTkLabel(card_despesas, text="Total Despesas", font=("Arial", 14)).place(relx=0.5, y=25, anchor="center")
        ctk.CTkLabel(card_despesas, text=f"R$ {total_despesas:.2f}", font=("Arial", 18, "bold")).place(relx=0.5, y=65, anchor="center")

        card_restante = ctk.CTkFrame(self.main_frame, width=200, height=100, corner_radius=10)
        card_restante.place(x=460, y=300)
        ctk.CTkLabel(card_restante, text="Restante", font=("Arial", 14)).place(relx=0.5, y=25, anchor="center")
        ctk.CTkLabel(card_restante, text=f"R$ {restante:.2f}", font=("Arial", 18, "bold")).place(relx=0.5, y=65, anchor="center")


    def cadastro_receitas(self):
        self.limpar_main_frame()
        titulo = ctk.CTkLabel(self.main_frame, text="Cadastrar Receita", font=("Arial", 24, "bold"))
        titulo.place(x=20, y=20)

        ctk.CTkLabel(self.main_frame, text="Descrição:").place(x=20, y=80)
        descricao = ctk.CTkEntry(self.main_frame, width=300)
        descricao.place(x=120, y=80)

        ctk.CTkLabel(self.main_frame, text="Valor:").place(x=20, y=130)
        valor = ctk.CTkEntry(self.main_frame, width=300)
        valor.place(x=120, y=130)

        tipos = ["Pix", "Dinheiro", "Transferência", "Salário"]
        ctk.CTkLabel(self.main_frame, text="Tipo:").place(x=20, y=180)
        tipo_rec = ctk.CTkComboBox(self.main_frame, values=tipos, width=300)
        tipo_rec.place(x=120, y=180)

        salvar_btn = ctk.CTkButton(self.main_frame, text="Salvar Receita", width=200,command="")
        salvar_btn.place(x=120, y=230)

    def cadastro_pagamentos(self):
        self.limpar_main_frame()
        titulo = ctk.CTkLabel(self.main_frame, text="Cadastrar Pagamento", font=("Arial", 24, "bold"))
        titulo.place(x=20, y=20)

        ctk.CTkLabel(self.main_frame, text="Descrição:").place(x=20, y=80)
        descricao = ctk.CTkEntry(self.main_frame, width=300)
        descricao.place(x=120, y=80)

        ctk.CTkLabel(self.main_frame, text="Valor:").place(x=20, y=130)
        valor = ctk.CTkEntry(self.main_frame, width=300)
        valor.place(x=120, y=130)

        tipos = ["Pix", "Crédito", "Débito", "Dinheiro", "Parcelado", "Consignado"]
        ctk.CTkLabel(self.main_frame, text="Tipo:").place(x=20, y=180)
        tipo_pag = ctk.CTkComboBox(self.main_frame, values=tipos, width=300)
        tipo_pag.place(x=120, y=180)

        parcelas = ["À vista", "1x", "2x", "3x", "4x", "5x", "6x", "7x", "8x", "9x", "10x", "12x", "24x", "36x", "48x", "60x", "72x", "84x", "96x", "128x"]
        ctk.CTkLabel(self.main_frame, text="Parcelas:").place(x=20, y=230)
        Quant_parc = ctk.CTkComboBox(self.main_frame, values=parcelas, width=300)
        Quant_parc.place(x=120, y=230)

        salvar_btn = ctk.CTkButton(self.main_frame, text="Salvar Pagamento", width=200, command="")
        salvar_btn.place(x=120, y=280)

    def listar_despesas(self):
        self.limpar_main_frame()

        titulo = ctk.CTkLabel(self.main_frame, text="Lista de Receitas", font=("Arial", 24, "bold"))
        titulo.place(x=20, y=20)

        # Scrollable Frame para tabela
        scroll_frame = ctk.CTkScrollableFrame(self.main_frame, width=730, height=500)
        scroll_frame.place(x=20, y=70)

        # Cabeçalho
        headers = ["Descrição", "Valor", "Tipo", "Parcelas", "Ações"]
        x_positions = [10, 250, 400, 550, 650]
        for i, header in enumerate(headers):
            ctk.CTkLabel(scroll_frame, text=header, font=("Arial", 14, "bold")).place(x=x_positions[i], y=10)
        y_offset = 40

        descricao = "Comida"
        valor = int(1000)
        tipo = "Crédito"
        parcelas = "2x"
        
        dados = [descricao, f"R$ {valor:.2f}", tipo, parcelas]

            # Exibe dados
        for i, dado in enumerate(dados):
            ctk.CTkLabel(scroll_frame, text=dado).place(x=x_positions[i], y=y_offset)

            # Botão Editar
        ctk.CTkButton(scroll_frame, text="Editar", width=60,
        command=lambda i=descricao, d=descricao, v=valor, t=tipo, p=parcelas: self.abrir_popup_editar_receita(i, d, v, t, p)
        ).place(x=x_positions[4], y=y_offset)

            # Botão Excluir
        ctk.CTkButton(scroll_frame, text="Excluir", width=60,
        command=lambda i=descricao: self.excluir_receita(i)
        ).place(x=x_positions[4] + 70, y=y_offset)

        y_offset += 40
    
    def abrir_popup_editar_receita(self, id_pg, descricao_atual, valor_atual, tipo_atual, parcelas_atual):
        popup = ctk.CTkToplevel(self.janela_principal)
        popup.title("Editar Receita")
        popup.geometry("400x350")
        popup.grab_set()

        ctk.CTkLabel(popup, text="Descrição:").place(x=20, y=20)
        entry_desc = ctk.CTkEntry(popup, width=300)
        entry_desc.place(x=20, y=50)
        entry_desc.insert(0, descricao_atual)

        ctk.CTkLabel(popup, text="Valor:").place(x=20, y=90)
        entry_valor = ctk.CTkEntry(popup, width=300)
        entry_valor.place(x=20, y=120)
        entry_valor.insert(0, str(valor_atual))

        ctk.CTkLabel(popup, text="Tipo:").place(x=20, y=160)
        entry_tipo = ctk.CTkEntry(popup, width=300)
        entry_tipo.place(x=20, y=190)
        entry_tipo.insert(0, tipo_atual)

        ctk.CTkLabel(popup, text="Parcelas:").place(x=20, y=230)
        entry_parc = ctk.CTkEntry(popup, width=300)
        entry_parc.place(x=20, y=260)
        entry_parc.insert(0, parcelas_atual)

        def salvar_edicao():
            nova_desc = entry_desc.get().strip()
            novo_valor = entry_valor.get().strip()
            novo_tipo = entry_tipo.get().strip()
            novas_parc = entry_parc.get().strip()

            if not nova_desc or not novo_valor or not novo_tipo:
                messagebox.showerror("Erro", "Preencha todos os campos.")
                return

            try:
                messagebox.showinfo("Sucesso", "Receita atualizada!")
                popup.destroy()
                self.listar_receitas()  # Atualiza lista
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar: {e}")

            ctk.CTkButton(popup, text="Salvar", command=salvar_edicao).place(x=150, y=300)

    def gerar_pdf(self):
        self.limpar_main_frame()
        titulo = ctk.CTkLabel(self.main_frame, text="Ainda em construção 🔧", font=("Arial", 50, "bold"))
        titulo.place(x=100, y=250)

    def iniciar(self):
        self.janela_principal.mainloop()

if __name__ == "__main__":
    mp = MenuPrincipal()
    mp.iniciar()