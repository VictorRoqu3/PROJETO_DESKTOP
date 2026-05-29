import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
from bancoDados.banco_dados import BancoDados
from bancoDados.sessao import Sessao
from PROJETO_DESKTOP.menu_principal.menu_principal import MenuPrincipal

# Tema global
ctk.set_appearance_mode("System")
cor_botões = "#8B0101"

class TelaLogin:
    def __init__(self, banco):
        self.banco = banco
        self.janela_principal = ctk.CTk()
        self.janela_principal.title("Login")
        self.janela_principal.geometry("800x600")
        self.janela_principal.resizable(False, False)

        self.criar_layout()
        self.carregar_imagem()
        self.carregar_logo()
        self.campos_login()
        self.criar_botoes()

    def criar_layout(self):
        self.frame_esquerda = ctk.CTkFrame(self.janela_principal)
        self.frame_esquerda.place(relx=0, rely=0, relwidth=0.5, relheight=1)

        self.frame_login = ctk.CTkFrame(self.frame_esquerda, width=380, height=200)
        self.frame_login.place(relx=0.5, rely=0.5, anchor="center")

        self.frame_imagem = ctk.CTkFrame(self.janela_principal)
        self.frame_imagem.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

    def carregar_imagem(self):
        caminho = os.path.join(os.path.dirname(__file__), "teste.jpg")
        if not os.path.exists(caminho):
            return

        try:
            img = Image.open(caminho)
            img = img.resize((800, 2000))
            self.imagem = ctk.CTkImage(light_image=img, dark_image=img, size=(480, 600))
            
            label_imagem = ctk.CTkLabel(self.frame_imagem, image=self.imagem, text="")
            label_imagem.place(relx=0.5, rely=0.5, anchor="center")
        except Exception as e:
            print(f"Falha ao carregar imagem: {e}")

    def carregar_logo(self):
        caminho = os.path.join(os.path.dirname(__file__), "RoquINVEST.jpg")
        if not os.path.exists(caminho):
            return

        try:
            img = Image.open(caminho)
            img = img.resize((100, 100))
            self.imagem = ctk.CTkImage(light_image=img, dark_image=img, size=(100, 100))

            label_imagem = ctk.CTkLabel(self.frame_esquerda, image=self.imagem, text="")
            label_imagem.place(x=350, y=130, anchor="center")
        except Exception as e:
            print(f"Falha ao carregar imagem: {e}")

    def campos_login(self):
        label_titulo = ctk.CTkLabel(self.frame_esquerda, text="RoquINVEST", font=("Arial", 48))
        label_titulo.place(x=10, y=100)

        label_usuario = ctk.CTkLabel(self.frame_login, text="Usuário", font=("Arial", 20))
        label_usuario.place(x=20, y=20)
        self.entry_nome = ctk.CTkEntry(self.frame_login, width=200, font=("Arial", 14))
        self.entry_nome.place(x=100, y=20)

        label_senha = ctk.CTkLabel(self.frame_login, text="Senha", font=("Arial", 20))
        label_senha.place(x=20, y=70)
        self.entry_senha = ctk.CTkEntry(self.frame_login, width=200, show="*", font=("Arial", 14))
        self.entry_senha.place(x=100, y=70)

        self.entry_nome.bind("<Return>", self.acionar_login)
        self.entry_senha.bind("<Return>", self.acionar_login)
    
    def acionar_login(self, event=None):
        self.validar_login()

    def criar_botoes(self):
        botao_logar = ctk.CTkButton(self.frame_login, text="Logar", width=100, font=("Arial", 14), fg_color="#8b0101", command=self.validar_login)
        botao_logar.place(y=130, x=60)

        botao_cadastrar = ctk.CTkButton(self.frame_login, text="Cadastrar", font=("Arial", 14), width=100, fg_color="#c5a31a", command=self.abrir_cadastro)
        botao_cadastrar.place(y=130, x=200)

    def validar_login(self):
        usuario = self.entry_nome.get().strip()
        senha = self.entry_senha.get().strip()

        if not usuario or not senha:
            messagebox.showerror("Erro", "Preencha os campos de usuário e senha!")
            return

        if self.banco.validar_credenciais(usuario, senha):
            try:
                self.banco.registrar_login(usuario)
            except Exception as e:
                print(f"Registro de teste/login falhou: {e}")

            Sessao.usuario_logado = usuario
            Sessao.login(usuario)
            print(f"Login: Sessao.usuario_logado = {Sessao.usuario_logado}")
            self.janela_principal.withdraw()
            usuario_id = self.banco.buscar_usuario_id(usuario)
            if usuario_id is not None:
                print(f"ID: banco.buscar_usuario_id = {usuario_id}")
                app = MenuPrincipal(usuario_id, self.janela_principal, self.banco)
                app.iniciar()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")

    def abrir_cadastro(self):
        self.janela_principal.withdraw()
        cadastro = ctk.CTkToplevel(self.janela_principal)
        cadastro.title("Cadastrar Usuário")
        cadastro.geometry("400x400")
        cadastro.resizable(False, False)

        frame_cadastro = ctk.CTkFrame(cadastro, corner_radius=15, width=360, height=360)
        frame_cadastro.place(relx=0.5, rely=0.5, anchor="center")

        titulo = ctk.CTkLabel(frame_cadastro, text="Cadastro de Usuário", font=("Arial", 20, "bold"))
        titulo.place(relx=0.5, y=30, anchor="center")

        label_usuario = ctk.CTkLabel(frame_cadastro, text="Novo Usuário:", font=("Arial", 14))
        label_usuario.place(x=20, y=50)
        entrada_novo_usuario = ctk.CTkEntry(frame_cadastro, width=300, placeholder_text="Digite o nome")
        entrada_novo_usuario.place(x=20, y=80)

        label_email = ctk.CTkLabel(frame_cadastro, text="Email:", font=("Arial", 14))
        label_email.place(x=20, y=110)
        entrada_novo_email = ctk.CTkEntry(frame_cadastro, width=300, placeholder_text="exemplo@email.com")
        entrada_novo_email.place(x=20, y=140)

        label_senha = ctk.CTkLabel(frame_cadastro, text="Nova Senha:", font=("Arial", 14))
        label_senha.place(x=20, y=170)
        entrada_nova_senha = ctk.CTkEntry(frame_cadastro, width=300, show="*", placeholder_text="Mínimo 12 caracteres")
        entrada_nova_senha.place(x=20, y=200)

        label_grupo = ctk.CTkLabel(frame_cadastro, text="Grupo:", font=("Arial", 14))
        label_grupo.place(x=20, y=230)
        tipo_grupo = ["", "Administrador", "Desenvolvedor", "Usuário"]
        entrada_grupo = ctk.CTkComboBox(frame_cadastro, values=tipo_grupo, width=300)
        entrada_grupo.place(x=20, y=260)

        def salvar_usuario():
            novo_usuario = entrada_novo_usuario.get().strip()
            novo_email = entrada_novo_email.get().strip()
            nova_senha = entrada_nova_senha.get().strip()
            novo_grupo = entrada_grupo.get().strip()

            if not novo_usuario or not nova_senha or not novo_email or not novo_grupo:
                messagebox.showerror("Erro", "Preencha usuário, email, senha e grupo!",parent=cadastro)
                return
            
            def validar_usuario(usuario):
                if not usuario:
                    return False, "Usuário deve ser preenchido."
                
                return True, ""

            def validar_email(email):
                contem_arroba = '@' in email
                termina_com = email.endswith('.com')

                if not contem_arroba or not termina_com:
                    return False, "Usuário deve conter '@' e terminar com '.com'."

                return True, ""

            def validar_senha(senha):
                if len(senha) < 12:
                    return False, "A senha deve ter no mínimo 12 caracteres."

                tem_maiuscula = False
                for caractere in senha:
                    if caractere.isupper():
                        tem_maiuscula = True
                        break
                if not tem_maiuscula:
                    return False, "A senha deve conter pelo menos uma letra maiúscula."

                tem_numero = False
                for caractere in senha:
                    if caractere.isdigit():
                        tem_numero = True
                        break
                if not tem_numero:
                    return False, "A senha deve conter pelo menos um número."

                caracteres_especiais = "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?`~"
                tem_especial = False
                for caractere in senha:
                    if caractere in caracteres_especiais:
                        tem_especial = True
                        break
                if not tem_especial:
                    return False, "A senha deve conter pelo menos um caractere especial."

                return True, ""
            
            def validar_grupo(grupo):
                if not grupo:
                    return False, "O grupo deve ser preenchido."
            
                return True, ""

            # Chama a função de validação do usuário, que retorna duas informações:
            # valido do tipo bool indica se o usuário é válido ou não,
            # e mensagem do tipo str contém a mensagem de erro caso não seja válido.
            valido, mensagem = validar_usuario(novo_usuario)
            if not valido:
                messagebox.showerror("Erro", mensagem,parent=cadastro)
                return
            
            valido, mensagem = validar_email(novo_email)
            if not valido:
                messagebox.showerror("Erro", mensagem,parent=cadastro)
                return

            valido, mensagem = validar_senha(nova_senha)
            if not valido:
                messagebox.showerror("Erro", mensagem,parent=cadastro)
                return
            
            valido, mensagem = validar_grupo(novo_grupo)
            if not valido:
                messagebox.showerror("Erro", mensagem,parent=cadastro)
                return

            try:
                self.banco.salvar_usuario(novo_usuario, novo_email, nova_senha, novo_grupo)
                messagebox.showinfo(f"Cadastrado", f"Usuário '{novo_usuario}' cadastrado com sucesso!")
                cadastro.destroy()
                self.janela_principal.deiconify()
            except ValueError as e:
                messagebox.showerror("Erro", str(e),parent=cadastro)

        botao_salvar = ctk.CTkButton(frame_cadastro, text="Salvar", width=220, fg_color="green", command=salvar_usuario)
        botao_salvar.place(relx=0.5, y=330, anchor="center")


    def iniciar(self):
        self.janela_principal.mainloop()

if __name__ == "__main__":
    bd = BancoDados
    ti = TelaLogin()
    ti.iniciar(bd)
