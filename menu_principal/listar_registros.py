import sys
import os
import customtkinter as ctk
from tkinter import messagebox
from bancoDados.banco_dados import BancoDados
from tkinter import ttk
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

class ListarRegistro:
    def __init__(self, menu):
        self.menu = menu
        self.banco = BancoDados()

    def listar_receitas(self):
        self.menu.limpar_main_frame()
        titulo = ctk.CTkLabel(self.menu.main_frame, text="Lista de Receitas", font=("Arial", 24, "bold"))
        titulo.place(x=20, y=20)

        scroll_frame = ctk.CTkScrollableFrame(self.menu.main_frame, width=935, height=520)
        scroll_frame.place(x=20, y=70)

        try:
            receitas = self.banco.listar_receitas_banco()

            if not receitas:
                vazio = ctk.CTkLabel(scroll_frame, text="Nenhuma receita cadastrada.", font=("Arial", 16))
                vazio.pack(anchor="w", pady=10)
            else:
                header_frame = ctk.CTkFrame(scroll_frame, fg_color="#222222")
                header_frame.pack(fill="x", pady=2)

                headers = ["Descrição", "Valor", "Tipo", "Status", "Recebimento"]
                widths = [250, 120, 150, 150, 120]

                for i, header in enumerate(headers):
                    lbl = ctk.CTkLabel(header_frame, text=header, font=("Arial", 14, "bold"),
                                    text_color="#FFFFFF", width=widths[i])
                    lbl.grid(row=0, column=i, padx=5, pady=5)

                for i, receita in enumerate(receitas):
                    descricao, valor, tipo, status, data_recebimento = receita

                    try:
                        data_formatada = data_recebimento.strftime("%d/%m/%Y")
                    except Exception:
                        print("Erro ao listar despesa retornado sem data")
                        data_formatada = ""

                    try:
                        valor = float(valor)
                    except ValueError:
                        valor = 0.0

                    bg_color = "#4d4c4c" if i % 2 == 0 else "#333333"
                    fg_color = "#FFFFFF"

                    item_frame = ctk.CTkFrame(scroll_frame, fg_color=bg_color)
                    item_frame.pack(fill="x", pady=2)

                    valores = [descricao, f"R$ {valor:.2f}", tipo, status, data_formatada]
                    for j, val in enumerate(valores):
                        lbl = ctk.CTkLabel(item_frame, text=str(val), anchor="w", font=("Arial", 12),
                                        text_color=fg_color, width=widths[j])
                        lbl.grid(row=0, column=j, padx=5, pady=5)

        except Exception as e:
            print(f"Erro ao listar receitas: {e}")
            messagebox.showerror("Erro", f"Erro ao listar receitas: {e}")

        salvar_btn = ctk.CTkButton(self.menu.main_frame, text="Editar", width=150, command=self.abrir_editor_receita)
        salvar_btn.place(x=800, y=20)


################################## EDITOR DE RECEITA ######################################################

    def abrir_editor_receita(self):
        self.menu.janela_principal.withdraw()
        editor = ctk.CTkToplevel(self.menu.janela_principal)
        editor.title("Editar Receitas")
        editor.geometry("700x400")
        editor.resizable(False, False)

        colunas = ("ID", "Descrição", "Valor", "Tipo", "Status")
        tree = ttk.Treeview(editor, columns=colunas, show="headings")
        tree.place(x=20, y=20, width=650, height=200)

        for col in colunas:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        receitas = self.banco.listar_receitas_banco()
        for r in receitas:
            tree.insert("", "end", values=r)

        label_desc = ctk.CTkLabel(editor, text="Descrição:")
        label_desc.place(x=20, y=240)
        entry_desc_r = ctk.CTkEntry(editor, width=200)
        entry_desc_r.place(x=120, y=240)

        label_valor = ctk.CTkLabel(editor, text="Valor:")
        label_valor.place(x=20, y=280)
        entry_valor_r = ctk.CTkEntry(editor, width=200)
        entry_valor_r.place(x=120, y=280)

        label_tipo = ctk.CTkLabel(editor, text="Tipo:")
        label_tipo.place(x=350, y=240)
        tipos = ["", "Pix", "Dinheiro", "Transferência", "Salário"]
        entry_tipo_r = ctk.CTkComboBox(editor, values=tipos, width=200)
        entry_tipo_r.place(x=420, y=240)

        label_status = ctk.CTkLabel(editor, text="Status:")
        label_status.place(x=350, y=280)
        registro = ["", "Recebido", "Não recebido"]
        entry_status_r = ctk.CTkComboBox(editor, values=registro, width=200)
        entry_status_r.place(x=420, y=280)

        def carregar_selecao(event):
            item = tree.selection()
            if item:
                valores = tree.item(item, "values")
                entry_desc_r.delete(0, "end")
                entry_desc_r.insert(0, valores[1])
                entry_valor_r.delete(0, "end")
                entry_valor_r.insert(0, valores[2])
                entry_tipo_r.set(valores[3])
                entry_status_r.set(valores[4])

        tree.bind("<<TreeviewSelect>>", carregar_selecao)

        def salvar_edicao_receita():
            item = tree.selection()
            if not item:
                messagebox.showwarning("Aviso", "Selecione uma receita para editar.")
                return

            valores = tree.item(item, "values")
            id_pg = int(valores[0])

            nova_desc = entry_desc_r.get().strip()
            novo_valor = entry_valor_r.get().strip()
            novo_tipo = entry_tipo_r.get().strip()
            novo_status = entry_status_r.get().strip()

            try:
                valor_convertido = float(novo_valor) if novo_valor else 0.0

                self.banco.atualizar_receita(id_pg, nova_desc, valor_convertido, novo_tipo, novo_status)
                messagebox.showinfo("Sucesso", "Receita atualizada com sucesso!")
                editor.destroy()
                self.listar_receitas()
                self.menu.janela_principal.deiconify()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar: {e}")

################################### EXCLUSÃO DE RECEITA ######################################################

        def excluir_receita():
            item = tree.selection()
            if not item:
                messagebox.showwarning("Aviso", "Selecione uma receita para excluir.")
                return
            valores = tree.item(item, "values")
            id_pg = valores[0]

            try:
                self.banco.excluir_receita(id_pg)
                messagebox.showinfo("Sucesso", "Receita excluída com sucesso!")
                editor.destroy()
                self.listar_receitas()
                self.menu.janela_principal.deiconify()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir: {e}")

        btn_salvar = ctk.CTkButton(editor, text="Salvar Alterações", command=salvar_edicao_receita)
        btn_salvar.place(x=200, y=330)

        btn_excluir = ctk.CTkButton(editor, text="Excluir Receita", fg_color="red", command=excluir_receita)
        btn_excluir.place(x=400, y=330)


    def listar_despesas(self):
        self.menu.limpar_main_frame()
        titulo = ctk.CTkLabel(self.menu.main_frame, text="Lista de Despesas", font=("Arial", 24, "bold"))
        titulo.place(x=20, y=20)

        scroll_frame = ctk.CTkScrollableFrame(self.menu.main_frame, width=935, height=520)
        scroll_frame.place(x=20, y=70)

        try:
            despesas = self.banco.listar_despesas_banco()

            if not despesas:
                vazio = ctk.CTkLabel(scroll_frame, text="Nenhuma despesa cadastrada.", font=("Arial", 16))
                vazio.pack(anchor="w", pady=10)
            else:
                header_frame = ctk.CTkFrame(scroll_frame, fg_color="#222222")
                header_frame.pack(fill="x", pady=2)

                headers = ["Descrição", "Valor", "Tipo", "Status", "Parcelas", "Vencimento"]
                widths = [200, 100, 120, 120, 100, 200]

                for i, header in enumerate(headers):
                    lbl = ctk.CTkLabel(header_frame, text=header, font=("Arial", 14, "bold"), text_color="#FFFFFF", width=widths[i])
                    lbl.grid(row=0, column=i, padx=5, pady=5)

                for i, despesa in enumerate(despesas):
                    descricao, valor, tipo, status, parcelas, vencimento = despesa

                    try:
                        data_formatada = vencimento.strftime("%d/%m/%Y")
                    except Exception:
                        print("Erro ao listar despesa retornado sem data")
                        data_formatada = ""

                    try:
                        valor = float(valor)
                    except ValueError:
                        valor = 0.0

                    bg_color = "#4d4c4c" if i % 2 == 0 else "#333333"
                    fg_color = "#FFFFFF"

                    item_frame = ctk.CTkFrame(scroll_frame, fg_color=bg_color)
                    item_frame.pack(fill="x", pady=2)

                    valores = [descricao, f"R$ {valor:.2f}", tipo, status, parcelas, data_formatada]
                    for j, val in enumerate(valores):
                        lbl = ctk.CTkLabel(item_frame, text=str(val), anchor="w", font=("Arial", 12), text_color=fg_color, width=widths[j])
                        lbl.grid(row=0, column=j, padx=5, pady=5)

        except Exception as e:
            print(f"Erro ao listar despesas: {e}")
            messagebox.showerror("Erro", f"Erro ao listar despesas: {e}")

        salvar_btn = ctk.CTkButton(self.menu.main_frame, text="Editar", width=150, command=self.abrir_editor_despesa)
        salvar_btn.place(x=800, y=20)

################################## EDITOR DE DESPESA ######################################################

    def abrir_editor_despesa(self):
        self.menu.janela_principal.withdraw()
        editor = ctk.CTkToplevel(self.menu.janela_principal)
        editor.title("Editar Despesa")
        editor.geometry("1000x400")
        editor.resizable(False, False)

        colunas = ("ID", "Descrição", "Valor", "Tipo", "Status", "Quantidade de parcelas")
        tree = ttk.Treeview(editor, columns=colunas, show="headings")
        tree.place(x=20, y=20, width=950, height=200)

        for col in colunas:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        despesas = self.banco.listar_despesas_banco()
        for d in despesas:
            tree.insert("", "end", values=d)

        label_desc = ctk.CTkLabel(editor, text="Descrição:")
        label_desc.place(x=20, y=240)
        entry_desc_d = ctk.CTkEntry(editor, width=200)
        entry_desc_d.place(x=120, y=240)

        label_valor = ctk.CTkLabel(editor, text="Valor:")
        label_valor.place(x=20, y=280)
        entry_valor_d = ctk.CTkEntry(editor, width=200)
        entry_valor_d.place(x=120, y=280)

        tipos = ["", "Pix", "Crédito", "Débito", "Dinheiro", "Parcelado", "Consignado"]
        label_tipo = ctk.CTkLabel(editor, text="Tipo:")
        label_tipo.place(x=350, y=240)
        entry_tipo_d = ctk.CTkComboBox(editor, values=tipos, width=200)
        entry_tipo_d.place(x=420, y=240)

        label_status = ctk.CTkLabel(editor, text="Status:")
        label_status.place(x=350, y=280)
        registro = ["", "Pago", "Não pago"]
        entry_status_d = ctk.CTkComboBox(editor, values=registro, width=200)
        entry_status_d.place(x=420, y=280)

        ctk.CTkLabel(editor, text="Parcelas:").place(x=650, y=240)
        slider_d = ctk.CTkSlider(editor, from_=0, to=500)
        slider_d.place(x=750, y=240)
        label_res = ctk.CTkLabel(editor, text=f"Quantidade de Parcelas: À vista")
        label_res.place(x=750, y=260)

        def atualizar_valor(event=None):
            valor = slider_d.get()
            valor_novo = int(valor)
            label_res.configure(text=f"Quantidade de Parcelas: {valor_novo}x")

        slider_d.bind("<B1-Motion>", atualizar_valor)
        slider_d.bind("<ButtonRelease-1>", atualizar_valor)
        slider_d.set(50)
        atualizar_valor()

        def carregar_selecao(event):
            item = tree.selection()
            if item:
                valores = tree.item(item, "values")
                entry_desc_d.delete(0, "end")
                entry_desc_d.insert(0, valores[1])
                entry_valor_d.delete(0, "end")
                entry_valor_d.insert(0, valores[2])
                entry_tipo_d.set(valores[3])
                entry_status_d.set(valores[4])
                slider_d.set(int(valores[5]))

                atualizar_valor()

        tree.bind("<<TreeviewSelect>>", carregar_selecao)

        def salvar_edicao_despesa():
            item = tree.selection()
            if not item:
                messagebox.showwarning("Aviso", "Selecione uma despesa para editar.")
                return

            valores = tree.item(item, "values")
            id_pg = int(valores[0])

            nova_desc = entry_desc_d.get().strip()
            novo_valor = entry_valor_d.get().strip()
            novo_tipo = entry_tipo_d.get().strip()
            novo_status = entry_status_d.get().strip()
            quantidade_parcelas = slider_d.get()

            try:
                valor_convertido = float(novo_valor) if novo_valor else 0.0

                self.banco.atualizar_despesa(id_pg, nova_desc, valor_convertido, novo_tipo, novo_status, quantidade_parcelas)
                messagebox.showinfo("Sucesso", "Receita atualizada com sucesso!")
                editor.destroy()
                self.listar_despesas()
                self.menu.janela_principal.deiconify()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar: {e}")

################################### EXCLUSÃO DE DESPESA ######################################################

        def excluir_despesa():
            item = tree.selection()
            if not item:
                messagebox.showwarning("Aviso", "Selecione uma despesa para excluir.")
                return
            valores = tree.item(item, "values")
            id_pg = valores[0]

            try:
                self.banco.excluir_despesa(id_pg)
                messagebox.showinfo("Sucesso", "Despesa excluída com sucesso!")
                editor.destroy()
                self.listar_despesas()
                self.menu.janela_principal.deiconify()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir: {e}")
    
        btn_salvar = ctk.CTkButton(editor, text="Salvar Alterações", command=salvar_edicao_despesa)
        btn_salvar.place(x=200, y=330)

        btn_excluir = ctk.CTkButton(editor, text="Excluir Despesa", fg_color="red", command=excluir_despesa)
        btn_excluir.place(x=400, y=330)

################################### PAGAMENTOS VIGENTE LISTAGEM ######################################################

    def listar_despesas_vigentes(self):
        self.menu.limpar_main_frame()
        titulo = ctk.CTkLabel(self.menu.main_frame, text="Lista de Despesas Vigentes", font=("Arial", 24, "bold"))
        titulo.place(x=20, y=20)

        scroll_frame = ctk.CTkScrollableFrame(self.menu.main_frame, width=935, height=520)
        scroll_frame.place(x=20, y=70)

        try:
            despesas = self.banco.listar_despesas_vigentes_banco()

            if not despesas:
                vazio = ctk.CTkLabel(scroll_frame, text="Nenhuma despesa vigente cadastrada.", font=("Arial", 16))
                vazio.pack(anchor="w", pady=10)
            else:
                header_frame = ctk.CTkFrame(scroll_frame, fg_color="#222222")
                header_frame.pack(fill="x", pady=2)

                headers = ["Descrição", "Valor", "Tipo", "Status", "Parcelas", "Vencimento"]
                widths = [200, 100, 120, 120, 100, 100]

                for i, header in enumerate(headers):
                    lbl = ctk.CTkLabel(header_frame, text=header, font=("Arial", 14, "bold"), text_color="#FFFFFF", width=widths[i])
                    lbl.grid(row=0, column=i, padx=5, pady=5)

                for i, despesa in enumerate(despesas):
                    descricao, valor, tipo, status, parcelas, vencimento = despesa

                    try:
                        data_formatada = vencimento.strftime("%d/%m/%Y")
                    except Exception:
                        print("Erro ao listar despesa retornado sem data")
                        data_formatada = ""
                    try:
                        valor = float(valor)
                    except ValueError:
                        valor = 0.0

                    bg_color = "#4d4c4c" if i % 2 == 0 else "#333333"
                    fg_color = "#FFFFFF"

                    item_frame = ctk.CTkFrame(scroll_frame, fg_color=bg_color)
                    item_frame.pack(fill="x", pady=2)

                    valores = [descricao, f"R$ {valor:.2f}", tipo, status, parcelas, data_formatada]
                    for j, val in enumerate(valores):
                        lbl = ctk.CTkLabel(item_frame, text=str(val), anchor="w", font=("Arial", 12), text_color=fg_color, width=widths[j])
                        lbl.grid(row=0, column=j, padx=5, pady=5)

        except Exception as e:
            print(f"Erro ao listar despesas vigente: {e}")
            messagebox.showerror("Erro", f"Erro ao listar despesas vigentes: {e}")
