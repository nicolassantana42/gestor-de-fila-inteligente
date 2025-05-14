"""
Módulo para visualização do mercado e caminhos.
"""
import tkinter as tk
import random
import time
from src.data.market_graph import MarketGraph
from src.algorithms.bfs import bfs
from src.algorithms.dfs import dfs

class MarketApp:
    """Classe que gerencia a interface gráfica e a simulação do mercado."""
    
    def __init__(self, root):
        """
        Inicializa a aplicação com janela, canvas e botões.
        
        Args:
            root: Janela principal do tkinter
        """
        self.root = root
        self.root.title("Mercado Inteligente - Navegação Otimizada")
        self.cell_size = 40
        self.grid_size = (10, 10)
        self.start = (0, 0)
        # 5 caixas, incluindo a posição (9, 9)
        self.cashiers = [(9, 1), (9, 3), (9, 5), (9, 7)]
        self.blocked = []  # Produtos (📦)
        self.forklifts = []  # Empilhadeiras (🚜)
        self.path = None
        self.current_step = 0

        # Configura a interface gráfica
        self._setup_ui()
        # Inicializa o grafo e bloqueios
        self.graph = MarketGraph()
        self.reset()

    def _setup_ui(self):
        """Configura o canvas, botões e label da interface."""
        # Main frame
        main_frame = tk.Frame(self.root, bg="#F5F6F5")
        main_frame.pack(padx=10, pady=10)

        # Canvas for the grid
        canvas_width = self.grid_size[1] * self.cell_size + 20
        canvas_height = self.grid_size[0] * self.cell_size + 20
        self.canvas = tk.Canvas(main_frame, width=canvas_width, height=canvas_height,
                                bg="#FFFFFF", highlightthickness=2, highlightbackground="#4CAF50")
        self.canvas.pack(pady=10)
        
        # Adicionar captura de clique no canvas para mover o carrinho
        self.canvas.bind("<Button-1>", self.move_cart)

        # Frame for buttons
        btn_frame = tk.Frame(main_frame, bg="#F5F6F5")
        btn_frame.pack(fill=tk.X)
        buttons = [
            ("Navegar com BFS", self.run_bfs, "#4CAF50", "white"),
            ("Navegar com DFS", self.run_dfs, "#2196F3", "white"),
            ("Adicionar Produtos", self.generate_random_blocks, "#FF9800", "white"),
            ("Mover Carrinho (Aleatório)", self.move_cart_random, "#9C27B0", "white"),
            ("Resetar Mercado", self.reset, "#F44336", "white")
        ]
        for text, command, bg, fg in buttons:
            tk.Button(btn_frame, text=text, command=command, bg=bg, fg=fg,
                      font=("Arial", 10, "bold"), relief="flat").pack(side=tk.LEFT, padx=5, pady=5)

        # Status label
        self.result_label = tk.Label(main_frame, text="Bem-vindo ao Mercado Inteligente!", 
                                    font=("Arial", 12), bg="#F5F6F5", fg="#333333")
        self.result_label.pack(pady=5)

    def generate_graph(self):
        """Cria o grafo do mercado com base no grid e bloqueios."""
        self.graph = MarketGraph()
        rows, cols = self.grid_size
        for i in range(rows):
            for j in range(cols):
                vertex = (i, j)
                if vertex in self.blocked or vertex in self.forklifts:
                    continue
                if i < rows - 1 and (i + 1, j) not in self.blocked and (i + 1, j) not in self.forklifts:
                    self.graph.add_edge(vertex, (i + 1, j))
                if j < cols - 1 and (i, j + 1) not in self.blocked and (i, j + 1) not in self.forklifts:
                    self.graph.add_edge(vertex, (i, j + 1))

    def generate_random_blocks(self):
        """Gera 15 produtos (📦) e 1 empilhadeira (🚜), evitando início, caixas e suas adjacências."""
        self.blocked = []
        self.forklifts = []

        # Define posições adjacentes aos caixas (espaço de segurança)
        forbidden_positions = set()
        for cashier in self.cashiers:
            i, j = cashier
            # Adiciona posições adjacentes (cima, baixo, esquerda, direita)
            adjacents = [
                (i-1, j) if i > 0 else None,  # Cima
                (i+1, j) if i < self.grid_size[0] - 1 else None,  # Baixo
                (i, j-1) if j > 0 else None,  # Esquerda
                (i, j+1) if j < self.grid_size[1] - 1 else None  # Direita
            ]
            for pos in adjacents:
                if pos:
                    forbidden_positions.add(pos)

        # Adiciona os próprios caixas e o carrinho às posições proibidas
        forbidden_positions.update(self.cashiers)
        forbidden_positions.add(self.start)

        # Gera posições possíveis para produtos e empilhadeira
        possible = [(i, j) for i in range(self.grid_size[0]) for j in range(self.grid_size[1])
                    if (i, j) not in forbidden_positions]

        # Gera 15 produtos (📦)
        if len(possible) >= 16:  # Garante espaço para produtos e empilhadeira
            self.blocked = random.sample(possible, 15)
            # Atualiza posições possíveis removendo os produtos já colocados
            possible = [(i, j) for i, j in possible if (i, j) not in self.blocked]
            # Gera 1 empilhadeira (🚜) em um corredor (coluna ímpar)
            corridor_positions = [(i, j) for i, j in possible if j % 2 == 1 and 2 <= i <= 5]
            if corridor_positions:
                self.forklifts = random.sample(corridor_positions, 1)

        self.generate_graph()
        self.draw_market()
        self.result_label.config(text="Produtos e empilhadeira adicionados!")
        print("Produtos e empilhadeira adicionados!")

    def move_cart_random(self):
        """Move o carrinho para uma posição aleatória que não seja bloqueada, empilhadeira ou um caixa."""
        possible = [(i, j) for i in range(self.grid_size[0]) for j in range(self.grid_size[1])
                    if (i, j) not in self.blocked and (i, j) not in self.forklifts and (i, j) not in self.cashiers]
        if possible:
            self.start = random.choice(possible)
            self.draw_market()
            self.result_label.config(text=f"Carrinho movido para {self.start}!")
            print(f"Carrinho movido para {self.start}!")
        else:
            self.result_label.config(text="Não há posições livres para mover o carrinho!")
            print("Não há posições livres para mover o carrinho!")

    def move_cart(self, event):
        """Move o carrinho para a posição clicada se esta for válida."""
        col = (event.x - 10) // self.cell_size
        row = (event.y - 10) // self.cell_size
        
        if 0 <= row < self.grid_size[0] and 0 <= col < self.grid_size[1]:
            position = (row, col)
            if position not in self.blocked and position not in self.forklifts and position not in self.cashiers:
                self.start = position
                self.path = None
                self.draw_market()
                self.result_label.config(text=f"Carrinho movido para {position}!")
                print(f"Carrinho movido para {position}!")
            else:
                self.result_label.config(text="Não é possível mover para essa posição!")
                print("Não é possível mover para essa posição!")

    def draw_market(self):
        """Desenha o grid do mercado no canvas com tema de supermercado, corredores e paredes entre caixas."""
        self.canvas.delete("all")
        rows, cols = self.grid_size
        for i in range(rows):
            for j in range(cols):
                x1, y1 = j * self.cell_size + 10, i * self.cell_size + 10
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                # Define corredores (colunas 2, 5, 8 com 4 blocos de altura)
                if (j == 2 or j == 5 or j == 8) and 2 <= i <= 5:
                    fill_color = "#8B4513"  # Marrom para corredores
                else:
                    fill_color = "#E0E0E0"  # Cinza claro para áreas externas
                if (i, j) == self.start:
                    # Desenha o carrinho
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#4CAF50", outline="#388E3C", width=2)
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="🛒", font=("Arial", 20))
                elif (i, j) in self.cashiers:
                    # Desenha o caixa
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#2196F3", outline="#1976D2", width=2)
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="💳", font=("Arial", 20))
                elif (i, j) in self.blocked:
                    # Desenha produtos
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#FF9800", outline="#F57C00", width=2)
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="📦", font=("Arial", 20))
                elif (i, j) in self.forklifts:
                    # Desenha empilhadeira
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#B0BEC5", outline="#78909C", width=2)
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="🚜", font=("Arial", 20))
                else:
                    # Desenha chão do corredor ou área externa
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="#B0B0B0", width=1)
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=f"{i},{j}", 
                                            font=("Arial", 8), fill="#666666")

        # Desenha paredes verticais entre os caixas
        for j in range(1, len(self.cashiers)):
            x_wall = (self.cashiers[j][1] * self.cell_size) + 10
            self.canvas.create_line(x_wall, 9 * self.cell_size + 10, x_wall, 10 * self.cell_size + 10,
                                    fill="#444444", width=3)

    def animate_path(self):
        """Anima o caminho desenhando passo a passo."""
        if self.path and self.current_step < len(self.path):
            if self.current_step > 0:
                prev = self.path[self.current_step - 1]
                curr = self.path[self.current_step]
                x1 = prev[1] * self.cell_size + self.cell_size // 2 + 10
                y1 = prev[0] * self.cell_size + self.cell_size // 2 + 10
                x2 = curr[1] * self.cell_size + self.cell_size // 2 + 10
                y2 = curr[0] * self.cell_size + self.cell_size // 2 + 10
                self.canvas.create_line(x1, y1, x2, y2, fill="#FFC107", width=4)
            self.current_step += 1
            self.root.after(200, self.animate_path)
        else:
            self.current_step = 0

    def run_search(self, algorithm):
        """
        Executa o algoritmo de busca especificado (bfs ou dfs).
        
        Args:
            algorithm: Função de busca (bfs ou dfs)
        """
        self.draw_market()
        start_time = time.time()
        
        if algorithm == bfs:
            self.path, cashier = bfs(self.graph, self.start, set(self.cashiers))
            algorithm_name = "BFS"
        else:
            self.path, cashier = dfs(self.graph, self.start, set(self.cashiers))
            algorithm_name = "DFS"
            
        elapsed = (time.time() - start_time) * 1000
        
        if self.path:
            steps = len(self.path) - 1
            msg = f"{algorithm_name}: {steps} passos até o caixa {cashier}, {elapsed:.2f}ms"
            print(msg + f": {self.path}")
            self.result_label.config(text=msg)
            self.current_step = 0
            self.animate_path()
        else:
            msg = f"{algorithm_name}: Nenhum caminho encontrado!"
            print(msg)
            self.result_label.config(text=msg)

    def run_bfs(self):
        """Executa a busca em largura."""
        self.run_search(bfs)

    def run_dfs(self):
        """Executa a busca em profundidade."""
        self.run_search(dfs)

    def reset(self):
        """Reseta o mercado, removendo bloqueios e recriando o grafo."""
        self.blocked = []
        self.forklifts = []
        self.path = None
        self.current_step = 0
        self.generate_graph()
        self.draw_market()
        self.result_label.config(text="Mercado resetado! Pronto para nova navegação.")
        print("Mercado resetado!")