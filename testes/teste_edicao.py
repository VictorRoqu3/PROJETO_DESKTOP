import customtkinter as ctk
from tkinter import messagebox, Toplevel, ttk
import sqlite3

# ----------------------------
# Banco SQLite
# ----------------------------
class BancoSQLite:
    def __init__(self, db_name="receitas.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.criar_tabela()

    def criar_tabela(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS receitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT,
            valor REAL,
            tipo TEXT,
            status TEXT
        )
        """)
        self.conn.commit()

    def listar_receitas(self):
        self.cursor.execute("SELECT * FROM receitas")
        return self.cursor.fetchall()

    def buscar_receita(self, id_pg):
        self.cursor.execute("SELECT * FROM receitas WHERE id=?", (id_pg,))
        return self.cursor.fetchone()

    def atualizar_receita(self, id_pg, descricao, valor, tipo, status):
        self.cursor.execute(
            "UPDATE receitas SET descricao=?, valor=?, tipo=?, status=? WHERE id=?",
            (descricao, float(valor), tipo, status, id_pg)
        )
        self.conn.commit()

    def excluir_receita(self, id_pg):
        self.cursor.execute("DELETE FROM receitas WHERE id=?", (id_pg,))
        self.conn.commit()

    def inserir_receita(self, descricao, valor, tipo, status):
        self.cursor.execute(
            "INSERT INTO receitas (descricao, valor, tipo, status) VALUES (?, ?, ?, ?)",
            (descricao, float(valor), tipo, status)
        )
        self.conn.commit()


# ----------------------------
# Aplicação
# ----------------------------
class App(ctk.CTk):
    def __init__(self, banco):
        super().__init__()
        self.title("Gerenciador de Receitas")
        self.geometry("820x650")
        self.banco = banco

        self.main_frame = ctk.CTkFrame(self, width=800, height=600)
        self.main_frame.place(x=10, y=10)

        # Botão para abrir editor
        btn_editar = ctk.CTkButton(self.main_frame, text="Editar Receitas", command=self.abrir_editor)
        btn_editar.place(x=20, y=20)

        # Botão para adicionar receita de teste
        btn_add = ctk.CTkButton(self.main_frame, text="Adicionar Receita Teste", command=self.add_teste)
        btn_add.place(x=200, y=20)

    def add_teste(self):
        self.banco.inserir_receita("Teste", 100.0, "Entrada", "Ativo")
        messagebox.showinfo("Sucesso", "Receita de teste adicionada!")

    def abrir_editor(self):
        # Cria janela Toplevel
        editor = Toplevel(self)
        editor.title("Editar Receitas")
        editor.geometry("700x400")

        # Treeview
        colunas = ("ID", "Descrição", "Valor", "Tipo", "Status")
        tree = ttk.Treeview(editor, columns=colunas, show="headings")
        tree.place(x=20, y=20, width=650, height=200)

        # Cabeçalhos
        for col in colunas:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        # Preenche com receitas
        receitas = self.banco.listar_receitas()
        for r in receitas:
            tree.insert("", "end", values=r)

        # Campos de edição
        lbl_desc = ctk.CTkLabel(editor, text="Descrição:")
        lbl_desc.place(x=20, y=240)
        entry_desc = ctk.CTkEntry(editor, width=200)
        entry_desc.place(x=120, y=240)

        lbl_valor = ctk.CTkLabel(editor, text="Valor:")
        lbl_valor.place(x=20, y=280)
        entry_valor = ctk.CTkEntry(editor, width=200)
        entry_valor.place(x=120, y=280)

        lbl_tipo = ctk.CTkLabel(editor, text="Tipo:")
        lbl_tipo.place(x=350, y=240)
        entry_tipo = ctk.CTkEntry(editor, width=200)
        entry_tipo.place(x=420, y=240)

        lbl_status = ctk.CTkLabel(editor, text="Status:")
        lbl_status.place(x=350, y=280)
        entry_status = ctk.CTkEntry(editor, width=200)
        entry_status.place(x=420, y=280)

        # Função para carregar dados da linha selecionada
        def carregar_selecao(event):
            item = tree.selection()
            if item:
                valores = tree.item(item, "values")
                entry_desc.delete(0, "end")
                entry_desc.insert(0, valores[1])
                entry_valor.delete(0, "end")
                entry_valor.insert(0, valores[2])
                entry_tipo.delete(0, "end")
                entry_tipo.insert(0, valores[3])
                entry_status.delete(0, "end")
                entry_status.insert(0, valores[4])

        tree.bind("<<TreeviewSelect>>", carregar_selecao)

        # Função salvar edição
        def salvar_edicao():
            item = tree.selection()
            if not item:
                messagebox.showwarning("Aviso", "Selecione uma receita para editar.")
                return
            valores = tree.item(item, "values")
            id_pg = valores[0]

            nova_desc = entry_desc.get()
            novo_valor = entry_valor.get()
            novo_tipo = entry_tipo.get()
            novo_status = entry_status.get()

            try:
                self.banco.atualizar_receita(id_pg, nova_desc, novo_valor, novo_tipo, novo_status)
                messagebox.showinfo("Sucesso", "Receita atualizada com sucesso!")
                editor.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar: {e}")

        # Função excluir
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
                self.abrir_editor()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir: {e}")

        # Botões
        btn_salvar = ctk.CTkButton(editor, text="Salvar Alterações", command=salvar_edicao)
        btn_salvar.place(x=200, y=330)

        btn_excluir = ctk.CTkButton(editor, text="Excluir Receita", fg_color="red", command=excluir_receita)
        btn_excluir.place(x=400, y=330)


# ----------------------------
# Executar o app
# ----------------------------
if __name__ == "__main__":
    banco = BancoSQLite()
    app = App(banco)
    app.mainloop()