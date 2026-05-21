# Algoritmo A*

## Autores
GABRIELLE RIBEIRO SILVA
MARIA EDUARDA PEREIRA LIMA
WENDEL DAVI REIS COSTA

## Instrução
Modelar um problema de busca como grafo, implementar e demonstrar a solução usando A* no NetworkX. O resultado deve ser apresentado de forma clara e reprodutível.

Código: repositório GitHub/GitLab ou arquivo compactado. Não esqueça de comentar o código.

Não esqueça de fazer um arquivo README com as seguintes

Informações:
- Descrição do problema;
- Como rodar passo a passo.
- Vídeo (até 15 minutos) no YouTube que atenda aos seguintes itens: Problema e modelagem em grafo; Implementação do A*; Demonstração executando o código; As limitações e próximos passos.

## Tema escolhido
Implementação do algoritmo A\* (A-Star) para roteamento inteligente em São Luís - MA.

## Descrição do Problema
Encontrar o caminho mais curto de qualquer bairro de São Luís até a UFMA (Campus Bacanga).

### Modelagem como grafo
| Elemento do grafo | Representação no problema |
|---|---|
| **Nó** | Bairro ou ponto de referência em São Luís |
| **Aresta** | Via/estrada que conecta dois bairros |
| **Peso da aresta** | Distância estimada do trecho em quilômetros |
 
O grafo é **não-dirigido** (mão dupla) e **ponderado** (com distâncias reais estimadas).

### Bairros mapeados (12 nós)
```
Quebra-Pote · Cidade Operária · Turu · Calhau · Cohama
Anil · Vinhais · Renascença · São Francisco
Centro · Itaqui-Bacanga · UFMA (destino)
```

## Estrutura do projeto
 
```
astar-sao-luis/
├── main.py                    # Código principal
├── requirements.txt           # Dependências Python
├── README.md                  # Este arquivo
└── rota_astar_sao_luis.png    # Gerado ao rodar o programa
```