import sys
import os
import customtkinter as ctk
from tkinter import messagebox
from bancoDados.banco_dados import BancoDados
from menu_principal.painel_principal import PainelPrincipal
from menu_principal.listar_registros import ListarRegistro
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

ctk.set_appearance_mode("System")
cor_botões = "#8B0101"
class MenuPrincipal:
    def __init__(self, id_usuario, master=None, banco=None):
        self.janela_principal = ctk.CTk()
        self.janela_principal.title("Menu Principal")
        self.janela_principal.geometry("1200x600")
        self.janela_principal.resizable(False, False)
        self.banco = banco
        self.bancoDados = BancoDados()
        self.id_usuario = id_usuario
        self.painel = PainelPrincipal(self)
        self.lista_registro = ListarRegistro(self)

        caminho = os.path.join(os.path.dirname(__file__), "")
        if os.path.exists(caminho):
            self.janela_principal.iconbitmap(caminho)

        self.sidebar = ctk.CTkFrame(self.janela_principal, width=200, height=600, corner_radius=0)
        self.sidebar.place(x=10, y=10)

        titulo_sidebar = ctk.CTkLabel(self.sidebar, text="Funcionalidades", font=("Arial", 18, "bold"))
        titulo_sidebar.place(x=10, y=20)

        self.main_frame = ctk.CTkFrame(self.janela_principal, width=980, height=600, corner_radius=10)
        self.main_frame.place(x=210, y=0)

        y_pos = 70

        ctk.CTkLabel(self.sidebar, text="Geral", font=("Arial", 14, "bold")).place(x=20, y=y_pos)
        y_pos += 30
        botoes_geral = [
            ("Painel principal", self.painel.painel_principal),
            ("Pagamentos vigentes", self.lista_registro.listar_despesas_vigentes),
            ("Relatórios", self.gerar_pdf)
        ]
        for texto, comando in botoes_geral:
            btn = ctk.CTkButton(self.sidebar, text=texto, width=160, fg_color="#8B0101",command=comando)
            btn.place(x=20, y=y_pos)
            y_pos += 40

        ctk.CTkLabel(self.sidebar, text="Receitas", font=("Arial", 14, "bold")).place(x=20, y=y_pos)
        y_pos += 30
        botoes_receitas = [
            ("Cadastrar receitas", self.cadastro_receitas),
            ("Lista de receitas", self.lista_registro.listar_receitas)
        ]
        for texto, comando in botoes_receitas:
            btn = ctk.CTkButton(self.sidebar, text=texto, width=160, fg_color="#8B0101", command=comando)
            btn.place(x=20, y=y_pos)
            y_pos += 40

        ctk.CTkLabel(self.sidebar, text="Despesas", font=("Arial", 14, "bold")).place(x=20, y=y_pos)
        y_pos += 30
        botoes_despesas = [
            ("Cadastrar despesa", self.cadastro_pagamentos),
            ("Lista de despesas", self.lista_registro.listar_despesas)
        ]
        for texto, comando in botoes_despesas:
            btn = ctk.CTkButton(self.sidebar, text=texto, width=160, fg_color=cor_botões, command=comando)
            btn.place(x=20, y=y_pos)
            y_pos += 40

        self.janela_principal.mainloop()

    def limpar_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            

################################### CADASTRO DE RECEITA E DESPESA ########################################

    def cadastro_receitas(self):
        self.limpar_main_frame()
        titulo = ctk.CTkLabel(self.main_frame, text="Cadastrar Receita", font=("Arial", 24, "bold"))
        titulo.place(x=20, y=20)

        ctk.CTkLabel(self.main_frame, text="Descrição:").place(x=20, y=80)
        descricao = ctk.CTkEntry(self.main_frame, width=300, placeholder_text="Ex.: Conta de Luz")
        descricao.place(x=120, y=80)

        ctk.CTkLabel(self.main_frame, text="Valor:").place(x=20, y=130)
        valor = ctk.CTkEntry(self.main_frame, width=300, placeholder_text="Ex.: R$ 1200")
        valor.place(x=120, y=130)
        
        tipos = ["", "Pix", "Dinheiro", "Transferência", "Depósito"]
        ctk.CTkLabel(self.main_frame, text="Tipo:").place(x=20, y=180)
        tipo_rec = ctk.CTkComboBox(self.main_frame, values=tipos, width=300)
        tipo_rec.place(x=120, y=180)

        registro = ["", "Recebido", "Não recebido"]
        ctk.CTkLabel(self.main_frame, text="Status:").place(x=20, y=230)
        status_rec = ctk.CTkComboBox(self.main_frame, values=registro, width=300)
        status_rec.place(x=120, y=230)

        ctk.CTkLabel(self.main_frame, text="Recebimento:").place(x=20, y=280)
        data_rec = ctk.CTkEntry(self.main_frame, width=300, placeholder_text="DD/MM/AAAA")
        data_rec.place(x=120, y=280)
 

        def salvar_receita():
            try:
                desc = descricao.get().strip()
                val = valor.get().strip()
                tipo = tipo_rec.get().strip()
                stat = status_rec.get().strip()
                dat_rec = data_rec.get().strip()

                if desc and val and tipo and stat and data_rec:
                    self.bancoDados.registrar_receita(desc, val, tipo, stat, dat_rec)
                    messagebox.showinfo("Sucesso", "Receita salva!")
                    self.lista_registro.listar_receitas()
                else:
                    messagebox.showerror("Erro", "Preencha todos os campos")
            except Exception as e:
                print(f"Erro: {e}")

        salvar_btn = ctk.CTkButton(self.main_frame, text="Salvar", width=200, fg_color="#8B0101",command=salvar_receita)
        salvar_btn.place(x=120, y=330)

    def cadastro_pagamentos(self):
        self.limpar_main_frame()
        titulo = ctk.CTkLabel(self.main_frame, text="Cadastrar Despesa", font=("Arial", 24, "bold"))
        titulo.place(x=20, y=20)

        ctk.CTkLabel(self.main_frame, text="Descrição:").place(x=20, y=80)
        descricao = ctk.CTkEntry(self.main_frame, width=300, placeholder_text="Ex.: Conta Luz")
        descricao.place(x=120, y=80)

        ctk.CTkLabel(self.main_frame, text="Valor:").place(x=20, y=130)
        valor = ctk.CTkEntry(self.main_frame, width=300, placeholder_text="Ex.: 1200")
        valor.place(x=120, y=130)

        tipos = ["", "Pix", "Crédito", "Débito", "Dinheiro", "Parcelado", "Consignado"]
        ctk.CTkLabel(self.main_frame, text="Tipo:").place(x=20, y=180)
        tipo_pag = ctk.CTkComboBox(self.main_frame, values=tipos, width=300)
        tipo_pag.place(x=120, y=180)

        ctk.CTkLabel(self.main_frame, text="Vencimento:").place(x=20, y=230)
        data_ven = ctk.CTkEntry(self.main_frame, width=300, placeholder_text="Ex.: DD/MM/AAAA")
        data_ven.place(x=120, y=230)

        tipos = ["", "Pago", "Não pago"]
        ctk.CTkLabel(self.main_frame, text="Status:").place(x=20, y=280)
        status_pag = ctk.CTkComboBox(self.main_frame, values=tipos, width=300)
        status_pag.place(x=120, y=280)

        ctk.CTkLabel(self.main_frame, text="Parcelas:").place(x=20, y=330)
        slider = ctk.CTkSlider(self.main_frame, from_=0, to=128)
        slider.place(x=120, y=330)
        label_res = ctk.CTkLabel(self.main_frame, text=f"Quantidade de Parcelas:")
        label_res.place(x=120, y=350)

        def atualizar_valor(event=None):
            valor = slider.get()
            valor_novo = int(valor)
            label_res.configure(text=f"Quantidade de Parcelas: {valor_novo}x")

        slider.bind("<B1-Motion>", atualizar_valor)
        slider.bind("<ButtonRelease-1>", atualizar_valor)
        slider.set(50)
        atualizar_valor()

        def salvar_despesa():
            try:
                desc = descricao.get().strip()
                val = valor.get().strip()
                tipo = tipo_pag.get().strip()
                stat = status_pag.get().strip()
                parc = slider.get()
                dat_ven = data_ven.get().strip()
                usua_i = self.id_usuario

                if desc and val and tipo and stat and data_ven:
                    self.bancoDados.registrar_despesa(desc, val, tipo, usua_i, stat, parc, dat_ven)
                    messagebox.showinfo("Sucesso", "Pagamento salvo!")
                    self.limpar_main_frame()
                    self.lista_registro.listar_despesas()
                else:
                    messagebox.showerror("Erro", "Preencha todos os campos")
            except Exception as e:
                print(f"Erro: {e}")

        salvar_btn = ctk.CTkButton(self.main_frame, text="Salvar", width=200, fg_color="#8B0101", command=salvar_despesa)
        salvar_btn.place(x=120, y=380)




################################### GERAR PDF EM CONSTRUÇÃO AINDA🔧########################################

    def gerar_pdf(self):
        self.limpar_main_frame()
        titulo = ctk.CTkLabel(self.main_frame, text="Ainda em construção 🔧", font=("Arial", 50, "bold"))
        titulo.place(x=100, y=250)

    def iniciar(self):
        self.janela_principal.mainloop()

if __name__ == "__main__":
    mp = MenuPrincipal()
    mp.iniciar()