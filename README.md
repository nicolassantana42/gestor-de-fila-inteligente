# 🚀 SmartQueue Market - Gestor de Filas Inteligentes

**Resumo:** Sistema simulador avançado para otimização de filas em supermercados que utiliza estrutura de grafos e algoritmo de busca BFS para encontrar o caminho mais eficiente até o caixa com menor fila, proporcionando uma experiência mais eficiente aos clientes através de visualização gráfica interativa.

---

## 🎯 Objetivo

O SmartQueue Market resolve o problema de otimização de deslocamento em supermercados, modelando o ambiente como um grafo onde cada nó representa uma posição no espaço e as arestas indicam os possíveis deslocamentos. O sistema permite localizar o caminho mais eficiente até o caixa com menos fila, simular obstáculos e áreas congestionadas utilizando o algoritmo de busca em largura (BFS).

A motivação surge da necessidade de melhorar a experiência do cliente em ambientes comerciais, reduzindo o tempo gasto em filas e otimizando o fluxo de pessoas. O projeto aplica diretamente os conceitos de estrutura de dados (grafos, filas) e algoritmo de busca estudados na disciplina, demonstrando sua aplicação prática em problemas reais.

---

## 👨‍💻 Tecnologias Utilizadas

- **Python 3.6+** - Linguagem principal do projeto
- **Tkinter** - Framework para desenvolvimento da interface gráfica
- **Collections** - Para implementação de filas no BFS
- **Random** - Para geração de bloqueios aleatórios
- **Time** - Para medição de desempenho
- **Unittest** - Para execução de testes unitários
- **Estruturas de Dados Avançadas** - Implementação de grafos e filas
- **Algoritmo de Busca** - BFS otimizado para o contexto de filas

---

## 🗂️ Estrutura do Projeto

```
📦 gestor-de-fila-inteligente
├── 📁 src
│   ├── 📁 algorithms
│   │   └── bfs.py                # Implementação do algoritmo BFS
│   ├── 📁 data
│   │   └── market_graph.py       # Classe base para o grafo do mercado
│   ├── 📁 utils
│   │   └── visualization.py      # Interface gráfica e lógica de simulação
│   └── main.py                   # Ponto de entrada do programa
├── 📁 tests
│   └── test_bfs.py               # Testes unitários para BFS
├── 📁 images
│   ├── Logo.png                  # Logo do projeto
│   └── fluxo-aplicacao.png       # Fluxograma da aplicação
├── requirements.txt              # Dependências do projeto
└── README.md                     # Documentação
```

---

## ⚙️ Como Executar

### ✅ Rodando Localmente

1. Clone o repositório:

```bash
git clone https://github.com/vitorjimenez/gestor-de-fila-inteligente.git
cd gestor-de-fila-inteligente
```

2. Verifique a versão do Python (necessário 3.6+):

```bash
python --version
```

3. Execute a aplicação:

```bash
python src/main.py
# ou
python -m src.main
```

4. Para executar os testes unitários:

```bash
python -m unittest tests/test_bfs.py
```

> 💡 Uma janela gráfica será aberta automaticamente com o simulador de filas.

---

## 🚀 Fluxo da aplicação
- **Fluxo**: Representação do fluxo a aplicação, sendo possível entender um pouco melhor dos requisitos funcionais da aplicação
<img src="./images/fluxo.PNG" width="850px" height="400px">


## 📸 Demonstrações

### Funcionalidades Principais:

- **Modelagem Completa**: Representação do mercado como um grafo em estrutura 11x11
- **Interface Gráfica Interativa**:
  - Visualização do mercado em forma de grade
  - Carrinho inicia na posição (0, 0) - indicado em verde claro 🛒
  - Caixas localizados em (9, 0), (9, 2), (9, 4), (9, 6) e (9, 9) - indicados em azul 💳
  - Bloqueios aleatórios (produtos 📦 em laranja e empilhadeiras 🚜 em cinza)
  - Corredores marrons nas colunas 2, 5 e 8 (linhas 2-5)
  - Caminho calculado mostrado em amarelo 🟡

### Como Usar:
1. Clique em "Adicionar Produtos" para gerar obstáculos aleatórios
2. Use "Mover Carrinho (Aleatório)" ou clique em uma célula livre para reposicionar
3. Selecione "Navegar com BFS" para encontrar o melhor caminho
4. Observe a animação do caminho calculado até o caixa mais próximo
5. Use "Resetar Mercado" para reiniciar a simulação

### Algoritmo Implementado:
- **BFS (Busca em Largura)**: Encontra o caminho mais curto até um caixa disponível

---

## 👥 Equipe

| Nome | GitHub | Função |
|------|--------|--------|
| Nicolas Santana | [@nicolas](https://github.com/nicolassantana42) | Gerente de Projeto |
| Vinicius Cerqueira | [@vinicius](https://github.com/ViniCerqueira/ViniCerqueira) | Desenvolvedor Backend |
| Vitor Jimenez | [@vitorjimenez](https://github.com/vitorjimenez) | Desenvolvedor Frontend |

---

## 🧠 Disciplinas Envolvidas

- **Estrutura de Dados ** - Implementação de grafos e filas
- **Algoritmos de Busca** - Aplicação prática de BFS
- **Programação Orientada a Objetos** - Modelagem das classes do sistema

---

## 🏫 Informações Acadêmicas

- **Universidade:** Universidade Braz Cubas
- **Curso:** Ciência da Computação
- **Semestre:** 4º e 5º
- **Período:** Noite
- **Professora orientadora:** Dra. Andréa Ono Sakai
- **Evento:** Mostra de Tecnologia 1º Semestre de 2025
- **Local:** Laboratório 12
- **Datas:** 05 e 06 de junho de 2025

---

## 📊 Cronograma de Desenvolvimento

| Etapa | Atividades | Prazo | Status |
|-------|-----------|-------|--------|
| 1 | Definição do objetivo | 24/04/2025 | ✅ Concluído |
| 2 | Seleção do algoritmo (BFS) | 30/04/2025 | ✅ Concluído |
| 3 | Escolha das tecnologias | 05/05/2025 | ✅ Concluído |
| 4 | Criação da estrutura de pastas | 10/05/2025 | ✅ Concluído |
| 5 | Implementação do grafo | 10/05/2025 | ✅ Concluído |
| 6 | Implementação de BFS | 12/05/2025 | ✅ Concluído |
| 7 | Interface gráfica | 13/05/2025 | ✅ Concluído |
| 8 | Testes e validação | 13/06/2025 | ✅ Concluído |
| 9 | Documentação | 15/06/2025 | ✅ Concluído |

---

## 🔍 Detalhes Técnicos

### Estrutura do Grafo
- **Vértices**: Representam posições acessíveis no mercado (células da grade 11x11)
- **Arestas**: Representam movimentos possíveis entre vértices adjacentes
- **Restrições**: Corredores marrons, produtos e empilhadeiras bloqueiam o movimento

### Análise de Desempenho
- Medição de tempo de execução do algoritmo BFS
- Contagem de passos necessários para chegar ao destino

---

## 📄 Licença

MIT License — sinta-se à vontade para utilizar, estudar e adaptar este projeto.
