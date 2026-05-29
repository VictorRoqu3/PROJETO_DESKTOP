import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

# 1. Configurar a aparência do CTk (opcional, mas recomendado)
ctk.set_appearance_mode("System")  # Ou "Dark", "Light"
ctk.set_default_color_theme("blue") # Define o tema de cor

# 2. Criar a janela principal da aplicação
app = ctk.CTk()
app.title("Gráfico no CustomTkinter com Matplotlib")
app.geometry("600x500")

# 3. Função para criar e exibir o gráfico
def criar_grafico():
    # Dados de exemplo
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    # Criar a figura e os eixos do Matplotlib
    # Configurações para combinar com o tema escuro do CTk, se aplicável
    fig, ax = plt.subplots(figsize=(5, 4), facecolor='#2b2b2b') # Cor de fundo da figura
    ax.plot(x, y, color="#b41f1f") # Cor da linha
    ax.set_title("Exemplo de Gráfico Senoidal", color='white')
    ax.set_xlabel("Eixo X", color='white')
    ax.set_ylabel("Eixo Y", color='white')
    ax.tick_params(colors='white') # Cor dos ticks dos eixos
    ax.set_facecolor('#2b2b2b') # Cor de fundo da área de plotagem
    
    # 4. Integrar o gráfico ao widget CTkFrame usando FigureCanvasTkAgg
    # Criar um frame para hospedar o canvas
    graph_frame = ctk.CTkFrame(master=app, width=500, height=400)
    graph_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Canvas é o objeto que desenha a figura Tkinter
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    # canvas.draw() # Desenha o gráfico

    # Adicionar o widget do canvas ao frame
    canvas.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)

    toolbar = NavigationToolbar2Tk(canvas, graph_frame)
    toolbar.update()
    canvas.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)


# 5. Adicionar um botão para gerar o gráfico (ou chamar a função diretamente)
button = ctk.CTkButton(master=app, text="Gerar Gráfico", command=criar_grafico)
button.pack(pady=10)

# 6. Iniciar o loop principal da aplicação
app.mainloop()
