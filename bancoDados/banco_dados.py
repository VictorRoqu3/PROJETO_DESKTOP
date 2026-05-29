import mysql.connector
import bcrypt
from tkinter import messagebox
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

############################## CRIAÇÃO DO BANCO DE DADOS #######################################

class BancoDados:
    def __init__(self):
        conexao = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password=""
        )
        cursor = conexao.cursor()
        cursor.execute('SELECT COUNT(*) FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = "Roque_Invest";')
        numero_resultado = cursor.fetchone()[0]
        conexao.close()

        if numero_resultado == 0:

            conexao = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password=""
        )
            cursor = conexao.cursor()
            cursor.execute('CREATE DATABASE Roque_Invest;')
            conexao.commit()
            conexao.close()

        try:
            self.conector = mysql.connector.connect( 
                host='localhost',
                user='root',
                password='',
                database='Roque_Invest'
            )
            self.cursor = self.conector.cursor()
            self.criar_tabela_usuario()
            self.criar_tabela_login()
            self.criar_tabela_receitas()
            self.criar_tabela_despesas()
            self.criar_tabela_despesas_usuario()
            self.usuario_admin()

        except:
            print(f"Erro ao conectar ao MYSQL")
            raise

############################## CRIAÇÃO DAS TABELAS DO BANCO DE DADOS #######################################

    def criar_tabela_usuario(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario VARCHAR(255) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL, 
                senha VARCHAR(255) NOT NULL,
                perfil VARCHAR(255) NOT NULL DEFAULT 'usuario'
            )
        """)
        self.conector.commit()

    def criar_tabela_login(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS logins (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT NOT NULL,
                data_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            )
        """)
        self.conector.commit()

    def criar_tabela_receitas(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS receitas(
                id INT AUTO_INCREMENT PRIMARY KEY,
                descricao_receita VARCHAR(255) NOT NULL,
                valor_receita VARCHAR(255) NOT NULL,
                tipo_receita VARCHAR(255) NOT NULL,
                status_receita VARCHAR(255) NOT NULL,
                data_recebimento DATE NOT NULL
            )
        """)
        self.conector.commit()

    def criar_tabela_despesas(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS despesas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                descricao_despesa VARCHAR(255) NOT NULL,
                valor_despesa VARCHAR(255) NOT NULL,
                usuario_id INT NOT NULL,
                tipo_despesa VARCHAR(255) NOT NULL,
                status_despesa VARCHAR(255) NOT NULL,
                quantidade_parcelas INT NOT NULL,
                data_vencimento DATE NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            )
        """)

        self.conector.commit()

    def criar_tabela_despesas_usuario(self):
        self.cursor.execute("""  
            CREATE TABLE IF NOT EXISTS despesas_usuario (
                id INT AUTO_INCREMENT PRIMARY KEY,
                despesa_id INT NOT NULL,
                usuario_id INT NOT NULL,
                quantidade_parcelas INT NOT NULL,
                status_despesa VARCHAR(255) NOT NULL,
                data_vencimento DATE NOT NULL,
                FOREIGN KEY (despesa_id) REFERENCES despesas(id) ON DELETE CASCADE,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            )
        """)
        self.conector.commit()

############################## SALVAR USUÁRIO NA TELA DE LOGIN E CADASTRAMENTO COM VALIDAÇÃO #######################################

    def salvar_usuario(self, usuario, email, senha, perfil='usuário', grupo_nome=None):
        self.cursor.execute("SELECT * FROM usuarios WHERE usuario = %s", (usuario,))
        if self.cursor.fetchone():
            raise ValueError("Usuário já existe.")
       
        senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

        self.cursor.execute(
            "INSERT INTO usuarios (usuario, email, senha, perfil) VALUES (%s, %s, %s, %s)",
            (usuario, email, senha_hash, perfil)
        )
        self.conector.commit()

        self.cursor.execute("SELECT id FROM usuarios WHERE usuario = %s", (usuario,))
        usuario_id = self.cursor.fetchone()[0]

        if grupo_nome:
            self.associar_usuario_grupo(usuario_id, grupo_nome)

    def validar_credenciais(self, usuario, senha):
        query = "SELECT senha FROM usuarios WHERE usuario = %s"
        self.cursor.execute(query, (usuario,))
        resultado = self.cursor.fetchone()
        if resultado:
            senha_hash = resultado[0]
            return bcrypt.checkpw(senha.encode(), senha_hash.encode())
        return False

    def registrar_login(self, usuario):
        self.cursor.execute("SELECT id FROM usuarios WHERE usuario = %s", (usuario,))
        usuario_id = self.cursor.fetchone()
        if usuario_id:
            self.cursor.execute("INSERT INTO logins (usuario_id) VALUES (%s)", (usuario_id[0],))
            self.conector.commit()

    def buscar_usuario_id(self, nome_usuario):
        try:
            self.cursor.execute("SELECT id FROM usuarios WHERE usuario = %s", (nome_usuario,))
            resultado = self.cursor.fetchone()
            if resultado:
                return int(resultado[0])  # retorna o id
            else:
                return None
        except Exception as e:
            print(f"Erro ao buscar usuário: {e}")
            return None

############################## REGISTRAR AS RECEITAS E DESPESAS #######################################

    def registrar_receita(self, descricao, valor, tipo_pag, status, data_recebimento):
        data_recebimento_bras = datetime.strptime(data_recebimento, "%d/%m/%Y")
        try:
            self.cursor.execute("""
                INSERT INTO receitas (descricao_receita, valor_receita, tipo_receita, status_receita, data_recebimento)
                VALUES (%s, %s, %s, %s, %s)
            """, (descricao, valor, tipo_pag, status, data_recebimento_bras))
            self.conector.commit()
            print("Receita registrada com sucesso!")
        except Exception as e:
            print(f"Erro ao registrar despesa: {e}")
    
    def registrar_despesa(self, descricao, valor, tipo_pag, usuario_id, status, parcelas, data_vencimento):
        data_vencimento_bras = datetime.strptime(data_vencimento, "%d/%m/%Y")
        try:
            self.cursor.execute("""
                INSERT INTO despesas (descricao_despesa, valor_despesa, tipo_despesa, usuario_id, status_despesa, quantidade_parcelas, data_vencimento)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (descricao, valor, tipo_pag, usuario_id, status, parcelas, data_vencimento_bras))


            despesa_id = self.cursor.lastrowid

            # Data base = momento do cadastro
            data_base = datetime.now()

            if parcelas and int(parcelas) > 0:
                for i in range(int(parcelas)):
                    data_vencimento_parcela = data_base + timedelta(days=30 * i)
                    
                    self.cursor.execute("""
                        INSERT INTO despesas_usuario (despesa_id, usuario_id, quantidade_parcelas, data_vencimento)
                        VALUES (%s, %s, %s, %s)
                    """, (despesa_id, usuario_id, i+1, data_vencimento_parcela.strftime("%Y-%m-%d")))

            self.conector.commit()

        except Exception as e:
            self.conector.rollback()
            print(f"Erro ao registrar despesa: {e}")




############################## LISTAGEM DAS RECEITAS E DESPESAS #######################################

    def listar_receitas_banco(self):
        try:
            self.cursor.execute("""
                SELECT descricao_receita, valor_receita, tipo_receita, status_receita, data_recebimento
                FROM receitas
            """)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Erro ao buscar receitas: {e}")
            return []
        
    def listar_despesas_banco(self):
        try:
            self.cursor.execute("""
                SELECT descricao_despesa, valor_despesa, tipo_despesa, status_despesa, quantidade_parcelas, data_vencimento
                FROM despesas
            """)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Erro ao buscar despesas: {e}")
            return []
        
    def listar_despesas_vigentes_banco(self):
        try:
            self.cursor.execute("""
                SELECT descricao_despesa, valor_despesa, tipo_despesa, status_despesa, quantidade_parcelas, data_vencimento
                FROM despesas 
                WHERE status_despesa = 'Não pago'
            """)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Erro ao buscar despesas: {e}")
            return []
        
############################## ALTERAR E EXCLUIR AS RECEITAS #######################################

    def atualizar_receita(self, id_pg, descricao, valor, tipo, status):
        try:
            self.cursor.execute(
                "UPDATE receitas SET descricao_receita=%s, valor_receita=%s, tipo_receita=%s, status_receita=%s WHERE id=%s",
                (descricao, valor, tipo, status, id_pg)
            )
            self.conector.commit()
        except Exception as e:
            print("Erro SQL:", e)
            raise

    def excluir_receita(self, id_pg):
        self.cursor.execute("DELETE FROM receitas WHERE id=%s", (id_pg,))
        self.conector.commit()

############################## ALTERAR E EXCLUIR AS DESPESAS #######################################

    def atualizar_despesa(self, id_pg, descricao, valor, tipo, status, quant_parc):
        try:
            self.cursor.execute(
                "UPDATE despesas SET descricao_despesa=%s, valor_despesa=%s, tipo_despesa=%s, status_despesa=%s, quantidade_parcelas=%s WHERE id=%s",
                (descricao, valor, tipo, status, quant_parc, id_pg)
            )
            self.conector.commit()
        except Exception as e:
            print("Erro SQL:", e)
            raise
    
    def excluir_despesa(self, id_pg):
        self.cursor.execute("DELETE FROM despesas WHERE id=%s", (id_pg,))
        self.conector.commit()

############################## SOMATÓRIO DOS TOTAIS NO BANCO #######################################

    def total_receitas(self):
        try:
            self.cursor.execute("SELECT COALESCE(SUM(valor_receita), 0) FROM receitas")
            return self.cursor.fetchone()[0]
        except Exception as e:
            print(f"Erro ao calcular total de receitas: {e}")
            return 0

    def total_despesas(self):
        try:
            self.cursor.execute("SELECT COALESCE(SUM(valor_despesa), 0) FROM despesas")
            return self.cursor.fetchone()[0]
        except Exception as e:
            print(f"Erro ao calcular total de despesas: {e}")
            return 0
        
    def total_despesas_vencidas(self):
        try:
            self.cursor.execute("""
                SELECT COALESCE(SUM(valor_despesa), 0) 
                FROM despesas 
                WHERE status_despesa = 'Não pago'
            """)
            return self.cursor.fetchone()[0]
        except Exception as e:
            print(f"Erro ao calcular total de despesas vencidas: {e}")
            return 0
        
    def total_despesas_nao_vencidas(self):
        try:
            self.cursor.execute("""
                SELECT COALESCE(SUM(valor_despesa), 0) 
                FROM despesas 
                WHERE status_despesa = 'Pago'
            """)
            return self.cursor.fetchone()[0]
        except Exception as e:
            print(f"Erro ao calcular total de despesas nao vencidas: {e}")
            return 0
        
############################## CRIAÇÃO - USUÁRIO: ADMIN, SENHA: 123  #######################################

    def usuario_admin(self):
        self.cursor.execute("SELECT COUNT(*) FROM usuarios WHERE usuario = %s", ("admin",))
        if self.cursor.fetchone()[0] == 0:
            senha_hash = bcrypt.hashpw("123".encode(), bcrypt.gensalt()).decode()
            self.cursor.execute(
                "INSERT INTO usuarios (usuario, email, senha, perfil) VALUES (%s, %s, %s, %s)",
                ("admin", "admin@admin.com", senha_hash, "administrador")
            )
            self.conector.commit()
            self.cursor.execute("SELECT id FROM usuarios WHERE usuario = %s", ("admin",))
            admin_id = self.cursor.fetchone()[0]
            self.associar_usuario_grupo(admin_id, "administrador")
            print("Usuário 'admin' criado com sucesso.")

    def associar_usuario_grupo(self, usuario_id, grupo_nome):
        self.cursor.execute("SELECT id FROM grupos WHERE nome = %s", (grupo_nome,))
        grupo = self.cursor.fetchone()
        if not grupo:
            self.adicionar_grupo(grupo_nome)
            self.cursor.execute("SELECT id FROM grupos WHERE nome = %s", (grupo_nome,))
            grupo = self.cursor.fetchone()

        grupo_id = grupo[0]
       
        self.cursor.execute(
            "SELECT * FROM usuario_grupo WHERE usuario_id = %s AND grupo_id = %s",
            (usuario_id, grupo_id)
        )

    def criar_grupos(self):
        setores = ["Administrador", "Desenvolvedor", "Usuário"]
        for grupo in setores:
            self.adicionar_grupo(grupo)

    def adicionar_grupo(self, nome_grupo):
        try:
            self.cursor.execute("INSERT INTO grupos (nome) VALUES (%s)", (nome_grupo,))
            self.conector.commit()
        except mysql.connector.IntegrityError:
            pass



    def __del__(self):
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'conexao') and self.conector:
            self.conector.close()