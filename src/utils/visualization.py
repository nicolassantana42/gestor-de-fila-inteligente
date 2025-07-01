"""
Módulo para visualização do mercado e caminhos.
"""
import tkinter as tk
import random
import time
from src.data.market_graph import MarketGraph
from src.algorithms.bfs import bfs

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
        self.grid_size = (11, 11)
        self.start = (0, 0)  # Apenas um carrinho
        self.cashiers = [(10, 1), (10, 3), (10, 5), (10, 7), (10, 9)]
        self.blocked = []  # Produtos (📦)
        self.forklifts = []  # Empilhadeiras (🚜)
        self.path = None  # Caminho do carrinho
        self.current_step = 0
        self.is_animating = False  # Controle para animação
        self.corridor_positions = [(i, j) for i in range(2, 8) for j in (2, 5, 8)]
        # Lista para armazenar resultados de desempenho (agora apenas para BFS)
        self.performance_results = []

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
            ("Adicionar Produtos", self.generate_random_blocks, "#FF9800", "white"),
            ("Mover Carrinho (Aleatório)", self.move_cart_random, "#9C27B0", "white"),
            ("Resetar Mercado", self.reset, "#F44336", "white"),
            ("Mostrar Análise de Desempenho", self.show_performance_analysis, "#607D8B", "white")
        ]
        for text, command, bg, fg in buttons:
            tk.Button(btn_frame, text=text, command=command, bg=bg, fg=fg,
                      font=("Arial", 10, "bold"), relief="flat").pack(side=tk.LEFT, padx=5, pady=5)

        # Status label
        self.result_label = tk.Label(main_frame, text="Bem-vindo ao Mercado Inteligente!", 
                                    font=("Arial", 12), bg="#F5F6F5", fg="#333333")
        self.result_label.pack(pady=5)

    def generate_graph(self):
        """Cria o grafo do mercado com base no grid e bloqueios, excluindo corredores marrons."""
        self.graph = MarketGraph()
        rows, cols = self.grid_size
        # Define os corredores marrons (colunas 2, 5, 8, linhas 2 a 7)
        corridor_positions = [(i, j) for i in range(2, 8) for j in (2, 5, 8)]

        for i in range(rows):
            for j in range(cols):
                vertex = (i, j)
                # Exclui vértices que estão nos corredores marrons, bloqueados ou com empilhadeiras
                if vertex in corridor_positions or vertex in self.blocked or vertex in self.forklifts:
                    continue
                # Adiciona arestas para baixo
                if i < rows - 1:
                    next_vertex = (i + 1, j)
                    if next_vertex not in corridor_positions and next_vertex not in self.blocked and next_vertex not in self.forklifts:
                        self.graph.add_edge(vertex, next_vertex)
                # Adiciona arestas para a direita
                if j < cols - 1:
                    next_vertex = (i, j + 1)
                    if next_vertex not in corridor_positions and next_vertex not in self.blocked and next_vertex not in self.forklifts:
                        self.graph.add_edge(vertex, next_vertex)

    def generate_random_blocks(self):
        """Gera 10 produtos (📦) e 2 empilhadeiras (🚜), evitando início, caixas, suas adjacências e corredores."""
        self.blocked = []
        self.forklifts = []

        # Define posições adjacentes aos caixas (espaço de segurança)
        forbidden_positions = set()
        for cashier in self.cashiers:
            i, j = cashier
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

        # Define os corredores (colunas 2, 5, 8, linhas 2 a 7) como posições proibidas para produtos e empilhadeiras
        corridor_positions = [(i, j) for i in range(2, 8) for j in (2, 5, 8)]

        # Gera posições possíveis para produtos e empilhadeiras (excluindo corredores)
        possible_positions = [(i, j) for i in range(self.grid_size[0]) for j in range(self.grid_size[1])
                             if (i, j) not in forbidden_positions and (i, j) not in corridor_positions]

        # Gera 10 produtos (📦)
        if len(possible_positions) >= 12:  # 10 produtos + 2 empilhadeiras
            self.blocked = random.sample(possible_positions, 10)
            # Atualiza posições possíveis removendo os produtos já colocados
            possible_for_forklifts = [(i, j) for i in range(self.grid_size[0]) for j in range(self.grid_size[1])
                                      if (i, j) not in forbidden_positions and (i, j) not in self.blocked and (i, j) not in corridor_positions]
            # Gera 2 empilhadeiras (🚜) fora dos corredores
            if len(possible_for_forklifts) >= 2:
                self.forklifts = random.sample(possible_for_forklifts, 2)

        self.generate_graph()
        self.draw_market()
        self.result_label.config(text="Produtos e empilhadeiras adicionados!")
        print("Produtos e empilhadeiras adicionados!")

    def move_cart_random(self):
        """Move o carrinho para uma posição aleatória que não seja bloqueada, empilhadeira ou um caixa."""
        corridor_positions = [(i, j) for i in range(2, 8) for j in (2, 5, 8)]
        possible = [(i, j) for i in range(self.grid_size[0]) for j in range(self.grid_size[1])
                    if (i, j) not in self.blocked 
                    and (i, j) not in self.forklifts 
                    and (i, j) not in self.cashiers
                    and (i, j) not in self.corridor_positions]
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
                # Define corredores (colunas 2, 5, 8 com 6 blocos de altura)
                if (j == 2 or j == 5 or j == 8) and 2 <= i <= 7:
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

        # Desenha o caminho, se existir
        if self.path and self.current_step < len(self.path) - 1:
            for i in range(self.current_step + 1):
                if i > 0:  # Não desenha a linha do início
                    prev = self.path[i - 1]
                    curr = self.path[i]
                    x1 = prev[1] * self.cell_size + self.cell_size // 2 + 10
                    y1 = prev[0] * self.cell_size + self.cell_size // 2 + 10
                    x2 = curr[1] * self.cell_size + self.cell_size // 2 + 10
                    y2 = curr[0] * self.cell_size + self.cell_size // 2 + 10
                    self.canvas.create_line(x1, y1, x2, y2, fill="#FFC107", width=4)

    def animate_path(self):
        """Anima o caminho desenhando passo a passo até o final."""
        if self.path and self.current_step < len(self.path) - 1:
            self.is_animating = True  # Indica que a animação está em andamento
            prev = self.path[self.current_step]
            curr = self.path[self.current_step + 1]
            x1 = prev[1] * self.cell_size + self.cell_size // 2 + 10
            y1 = prev[0] * self.cell_size + self.cell_size // 2 + 10
            x2 = curr[1] * self.cell_size + self.cell_size // 2 + 10
            y2 = curr[0] * self.cell_size + self.cell_size // 2 + 10
            self.canvas.create_line(x1, y1, x2, y2, fill="#FFC107", width=4)
            self.current_step += 1
            self.root.after(200, self.animate_path)
        else:
            self.current_step = 0  # Reinicia para a próxima animação
            self.is_animating = False  # Indica que a animação terminou

    def run_bfs(self):
        """Executa a busca em largura."""
        print("Iniciando BFS...")
        start_time = time.time()
        self.path, cashier = bfs(self.graph, self.start, set(self.cashiers))
        elapsed = (time.time() - start_time) * 1000
        
        if self.path:
            steps = len(self.path) - 1
            msg = f"BFS: {steps} passos até o caixa {cashier}, {elapsed:.2f}ms"
            print(msg + f": {self.path}")
            self.result_label.config(text=msg)
            # Armazena o resultado para análise
            self.performance_results.append({
                "algorithm": "BFS",
                "steps": steps,
                "time_ms": elapsed,
                "start": self.start,
                "cashier": cashier,
                "path": self.path
            })
            self.current_step = 0
            self.animate_path()
        else:
            msg = "BFS: Nenhum caminho encontrado!"
            print(msg)
            self.result_label.config(text=msg)

    def show_performance_analysis(self):
        """Exibe uma análise de desempenho para BFS."""
        if not self.performance_results:
            self.result_label.config(text="Nenhum resultado de desempenho disponível!")
            print("Nenhum resultado de desempenho disponível!")
            return

        # Calcula médias para BFS
        bfs_results = self.performance_results
        bfs_avg_steps = sum(r["steps"] for r in bfs_results) / len(bfs_results) if bfs_results else 0
        bfs_avg_time = sum(r["time_ms"] for r in bfs_results) / len(bfs_results) if bfs_results else 0

        # Monta a mensagem de análise
        analysis_msg = (
            "Análise de Desempenho (BFS):\n"
            f"Média de Passos: {bfs_avg_steps:.2f}, Média de Tempo: {bfs_avg_time:.2f}ms\n"
            f"Total de Execuções: {len(bfs_results)}"
        )

        # Exibe no terminal
        print(analysis_msg)

        # Exibe na interface gráfica
        self.result_label.config(text=analysis_msg.replace("\n", " | "))

        # Opcional: Exibe uma janela com detalhes de cada execução
        details_window = tk.Toplevel(self.root)
        details_window.title("Detalhes de Desempenho (BFS)")
        details_text = tk.Text(details_window, height=20, width=80)
        details_text.pack(padx=10, pady=10)
        details_text.insert(tk.END, "Detalhes de Cada Execução (BFS):\n\n")
        for i, result in enumerate(self.performance_results, 1):
            details_text.insert(tk.END, f"Execução {i}:\n")
            details_text.insert(tk.END, f"  Início: {result['start']}, Caixa: {result['cashier']}\n")
            details_text.insert(tk.END, f"  Passos: {result['steps']}, Tempo: {result['time_ms']:.2f}ms\n")
            details_text.insert(tk.END, f"  Caminho: {result['path']}\n\n")
        details_text.config(state=tk.DISABLED)

    def reset(self):
        """Reseta o mercado, removendo bloqueios e recriando o grafo."""
        self.start = (0, 0)
        self.blocked = []
        self.forklifts = []
        self.path = None
        self.current_step = 0
        self.is_animating = False  # Reseta o controle de animação
        self.performance_results = []  # Limpa os resultados de desempenho
        self.generate_graph()
        self.draw_market()
        self.result_label.config(text="Mercado resetado! Pronto para nova navegação.")
        print("Mercado resetado!")