from collections import deque

def bfs(graph, start, goals):
    """
    Executa a Busca em Largura para encontrar o caminho mais curto de start até um dos goals.
    
    Args:
        graph: Instância de MarketGraph
        start: Vértice inicial
        goals: Lista ou conjunto de vértices de destino
        
    Returns:
        tuple: (caminho, vértice de destino) ou (None, None) se não encontrar caminho
    """
    if not isinstance(goals, set):
        goals = set(goals)
        
    visited = set()
    queue = deque([[start]])
    
    while queue:
        path = queue.popleft()
        vertex = path[-1]
        
        if vertex in goals:
            return path, vertex
            
        if vertex not in visited:
            visited.add(vertex)
            for neighbor in graph.graph[vertex]:
                if neighbor not in visited:
                    queue.append(path + [neighbor])
                    
    return None, None