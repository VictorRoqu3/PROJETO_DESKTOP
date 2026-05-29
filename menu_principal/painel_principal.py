
import sys
import os
import customtkinter as ctk
from bancoDados.banco_dados import BancoDados
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

class PainelPrincipal:
    def __init__(self, menu):
        self.menu = menu
        self.banco = BancoDados()
          
    def painel_principal(self):
        self.menu.limpar_main_frame()
        titulo = ctk.CTkLabel(self.menu.main_frame, text="Orçamento pessoal", font=("Arial", 24, "bold"))
        titulo.place(x=20, y=20)

        grafico_frame = ctk.CTkFrame(self.menu.main_frame, width=500, height=200)
        grafico_frame.place(x=20, y=70)
        ctk.CTkLabel(grafico_frame, text="[Futuro gráfico aqui]", font=("Arial", 16, "bold")).place(relx=0.5, rely=0.5, anchor="center")

        total_receitas = self.banco.total_receitas()
        total_despesas = self.banco.total_despesas()

        restante = total_receitas - total_despesas

        if restante < 0:
            pass

        card_receitas = ctk.CTkFrame(self.menu.main_frame, width=200, height=100, corner_radius=10)
        card_receitas.place(x=20, y=300)
        ctk.CTkLabel(card_receitas, text="Total Receitas", font=("Arial", 16, "bold"), text_color="green").place(relx=0.5, y=25, anchor="center")
        ctk.CTkLabel(card_receitas, text=f"R$ {total_receitas:.2f}", font=("Arial", 18, "bold")).place(relx=0.5, y=65, anchor="center")

        card_despesas = ctk.CTkFrame(self.menu.main_frame, width=200, height=100, corner_radius=10)
        card_despesas.place(x=240, y=300)
        ctk.CTkLabel(card_despesas, text="Total Despesas", font=("Arial", 16, "bold"), text_color="white").place(relx=0.5, y=25, anchor="center")
        ctk.CTkLabel(card_despesas, text=f"R$ {total_despesas:.2f}", font=("Arial", 18, "bold")).place(relx=0.5, y=65, anchor="center")

        card_restante = ctk.CTkFrame(self.menu.main_frame, width=200, height=100, corner_radius=10)
        card_restante.place(x=460, y=300)
        ctk.CTkLabel(card_restante, text="Saldo", font=("Arial", 20, "bold")).place(relx=0.5, y=25, anchor="center")
        ctk.CTkLabel(card_restante, text=f"R$ {restante:}", font=("Arial", 18, "bold")).place(relx=0.5, y=65, anchor="center")

        total_despesas_vencidas = self.banco.total_despesas_vencidas()

        grafico_vencido = ctk.CTkFrame(self.menu.main_frame, width=230, height=120, corner_radius=10)
        grafico_vencido.place(x= 20, y=420)
        ctk.CTkLabel(grafico_vencido, text="Despesas Vencidas", font=("Arial", 16, "bold"), text_color="Red").place(relx=0.5, y=25, anchor="center")
        ctk.CTkLabel(grafico_vencido, text=f"R$ {total_despesas_vencidas:.2f}", font=("Arial", 18, "bold")).place(relx=0.5, y=65, anchor="center")
        
        total_despesas_nao_vencidas = self.banco.total_despesas_nao_vencidas()

        grafico_nao_vencido = ctk.CTkFrame(self.menu.main_frame, width=240, height=120, corner_radius=10)
        grafico_nao_vencido.place(x= 280, y=420)
        ctk.CTkLabel(grafico_nao_vencido, text="Despesas Não Vencidas", font=("Arial", 16, "bold"), text_color="Yellow").place(relx=0.5, y=25, anchor="center")
        ctk.CTkLabel(grafico_nao_vencido, text=f"R$ {total_despesas_nao_vencidas:.2f}", font=("Arial", 18, "bold")).place(relx=0.5, y=65, anchor="center")

        total_despesas_futuras = float(0.0)

        grafico_futuro = ctk.CTkFrame(self.menu.main_frame, width=230, height=120, corner_radius=10)
        grafico_futuro.place(x= 540, y=420)
        ctk.CTkLabel(grafico_futuro, text="Despesas Futuras", font=("Arial", 16, "bold"), text_color="Green").place(relx=0.5, y=25, anchor="center")
        ctk.CTkLabel(grafico_futuro, text=f"R$ {total_despesas_futuras:.2f}", font=("Arial", 18, "bold")).place(relx=0.5, y=65, anchor="center")
