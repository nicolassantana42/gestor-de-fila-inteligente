"""
Testes para o algoritmo BFS.
"""
import unittest
import sys
import os

# Adiciona o diretório raiz do projeto ao caminho Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data.market_graph import MarketGraph
from src.algorithms.bfs import bfs


class TestBFS(unittest.TestCase):
    """Classe de teste para o algoritmo BFS."""

    def setUp(self):
        """Configura um grafo simples para testes."""
        self.graph = MarketGraph()
        
        # Criar um grafo 3x3 simples
        for i in range(3):
            for j in range(3):
                self.graph.add_vertex((i, j))
        
        # Adicionar arestas horizontais e verticais
        for i in range(3):
            for j in range(2):
                self.graph.add_edge((i, j), (i, j+1))  # Horizontal
                self.graph.add_edge((j, i), (j+1, i))  # Vertical

    def test_bfs_simple_path(self):
        """Testa se o BFS encontra o caminho correto em um grafo simples."""
        start = (0, 0)
        goals = {(2, 2)}
        path, goal = bfs(self.graph, start, goals)
        
        # Verificar se encontrou um caminho
        self.assertIsNotNone(path)
        self.assertEqual(goal, (2, 2))
        
        # Verificar se o caminho começa no ponto inicial e termina no objetivo
        self.assertEqual(path[0], start)
        self.assertEqual(path[-1], (2, 2))
        
        # Verificar se o caminho tem comprimento correto (deve ser o mais curto)
        self.assertEqual(len(path), 5)  # [(0,0), (0,1), (0,2), (1,2), (2,2)] ou equivalente

    def test_bfs_multiple_goals(self):
        """Testa se o BFS encontra o objetivo mais próximo quando há múltiplos objetivos."""
        start = (0, 0)
        goals = {(1, 1), (2, 2)}
        path, goal = bfs(self.graph, start, goals)
        
        self.assertIsNotNone(path)
        self.assertEqual(goal, (1, 1))  # Deve encontrar (1,1) por ser mais próximo
        self.assertEqual(len(path), 3)  # [(0,0), (0,1), (1,1)] ou [(0,0), (1,0), (1,1)]

    def test_bfs_unreachable(self):
        """Testa se o BFS retorna None quando não há caminho para o objetivo."""
        # Criar um grafo desconectado
        disconnected_graph = MarketGraph()
        disconnected_graph.add_vertex((0, 0))
        disconnected_graph.add_vertex((1, 1))
        
        path, goal = bfs(disconnected_graph, (0, 0), {(1, 1)})
        
        self.assertIsNone(path)
        self.assertIsNone(goal)


if __name__ == '__main__':
    unittest.main()