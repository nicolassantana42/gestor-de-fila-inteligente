class MarketGraph:
    """Classe que representa o grafo do mercado como uma lista de adjacência."""
    
    def __init__(self):
        """Inicializa o grafo como um dicionário vazio."""
        self.graph = {}

    def add_vertex(self, vertex):
        """Adiciona um vértice ao grafo se ele não existir e for uma tupla válida.
        
        Args:
            vertex: O vértice a ser adicionado (tupla (i, j)).
        """
        if not isinstance(vertex, tuple) or len(vertex) != 2 or not all(isinstance(x, int) for x in vertex):
            raise ValueError("Vértice deve ser uma tupla (i, j) com inteiros.")
        if vertex not in self.graph:
            self.graph[vertex] = []

    def add_edge(self, v1, v2):
        """Adiciona uma aresta bidirecional entre v1 e v2.
        
        Args:
            v1: Primeiro vértice (tupla (i, j)).
            v2: Segundo vértice (tupla (i, j)).
        """
        self.add_vertex(v1)
        self.add_vertex(v2)
        if v2 not in self.graph[v1]:  # Evita duplicatas
            self.graph[v1].append(v2)
        if v1 not in self.graph[v2]:  # Evita duplicatas
            self.graph[v2].append(v1)
    
    def get_vertices(self):
        """Retorna a lista de todos os vértices do grafo.
        
        Returns:
            list: Lista contendo todos os vértices do grafo.
        """
        return list(self.graph.keys())
    
    def get_neighbors(self, vertex):
        """Retorna a lista de vizinhos de um vértice.
        
        Args:
            vertex: O vértice cujos vizinhos serão retornados.
            
        Returns:
            list: Lista de vizinhos do vértice. Retorna uma lista vazia se o vértice não existir.
        """
        if vertex in self.graph:
            return self.graph[vertex]
        return []