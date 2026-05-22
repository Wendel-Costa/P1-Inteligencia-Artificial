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

## Link do Vídeo 
https://youtu.be/cvwQpeH3yCY?si=VrMeOVhXC9DH_cbw

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

## Como rodar — passo a passo
 
### Pré-requisitos
 
- Python **3.8+** instalado  
  → Verifique com: `python --version`
### 1. Clone ou baixe o repositório
 
```bash
git clone [https://github.com/seu-usuario/astar-sao-luis.git](https://github.com/Wendel-Costa/App-de-organizacao.git)
cd astar-sao-luis
```
 
> Ou baixe e extraia o `.zip` pelo GitHub.
 
### 2. (Opcional) Crie um ambiente virtual
 
```bash
python -m venv venv
 
# Linux / macOS:
source venv/bin/activate
 
# Windows:
venv\Scripts\activate
```
 
### 3. Instale as dependências
 
```bash
pip install -r requirements.txt
```
 
O arquivo `requirements.txt` contém:
```
networkx>=3.0
matplotlib>=3.7
```
 
### 4. Execute o programa
 
```bash
python main.py
```
 
### 5. Uso interativo
 
O programa listará os bairros disponíveis e pedirá a origem:
 
```
============================================================
    NAVEGADOR A* — SÃO LUÍS, MARANHÃO
  Destino fixo: UFMA — Campus Bacanga
============================================================
 
Bairros disponíveis no mapa:
  Anil        | Calhau      | Centro
  ...
 
 De onde você está saindo? Turu
```
 
Digite o nome do bairro (com maiúscula inicial) e pressione Enter.
 
### 6. Saída esperada
 
O programa exibirá:
1. **Rastreamento passo a passo** do A\* com valores `g(n)`, `h(n)` e `f(n)`
2. **Detalhamento da rota** com distância de cada trecho e custo acumulado
3. **Rota ótima** completa e distância total
4. **Visualização gráfica** abrindo uma janela com o mapa e o caminho destacado
5. Imagem **`rota_astar_sao_luis.png`** salva no diretório atual
### Exemplo de execução (origem: Quebra-Pote)
 
```
Nó Expandido         g(n)   h(n)   f(n)
Quebra-Pote           0.0   22.0   22.0
Cidade Operária      18.0   15.0   33.0
Anil                 25.5    8.5   34.0
Centro               34.5    2.5   37.0
...
UFMA                 41.0    0.0   41.0
 
ROTA ÓTIMA: Quebra-Pote ➔ Cidade Operária ➔ Anil ➔ Centro ➔ Itaqui-Bacanga ➔ UFMA
DISTÂNCIA : 41.0 km
```
 
---
 
## Estrutura do projeto
 
```
astar-sao-luis/
├── main.py                    # Código principal
├── requirements.txt           # Dependências Python
├── README.md                  # Este arquivo
└── rota_astar_sao_luis.png    # Gerado ao rodar o programa
```
 
---
 
## Limitações e Próximos Passos
 
### Limitações atuais
 
| Limitação | Descrição |
|---|---|
| Grafo simplificado | Apenas 12 bairros; São Luís tem dezenas de bairros |
| Pesos estimados | Distâncias aproximadas, não extraídas de API de mapas real |
| Grafo estático | Não considera trânsito, semáforos ou obras em tempo real |
| Destino fixo | Sempre roteia para a UFMA; não permite destino livre |
 
### Próximos passos sugeridos
 
- [ ] Integrar com a API do **OpenStreetMap** ou **Google Maps** para dados reais
- [ ] Implementar **destino variável** (não apenas UFMA)
- [ ] Incluir pesos dinâmicos com dados de **tráfego em tempo real**
- [ ] Desenvolver uma interface web interativa com o mapa real de São Luís
---
