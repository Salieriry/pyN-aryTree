# pyN-aryTree
# Projeto: Árvore n-ária em Python

Esse projeto implementa uma estrutura de dados de árvore n-ária e uma interface gráfica com Tkinter para visualizar e manipular a árvore.

## Pré-requisitos

* Python 3.12.3

## Instruções

1. Abra um terminal na pasta onde estão os arquivos.
2. Crie um ambiente virtual:
    `python -m venv venv`
3. Ative o ambiente virtual:
    `./venv/Scripts/activate`
4. Instale as dependências:
    `pip install -r requirements.txt`
5. Execute a aplicação:
    `python main.py`

## Sobre a interface

Na interface desenvolvida, você consegue adicionar, selecionar e remover árvores e nós. Você consegue reorganizar os nós visualmente clicando e os arrastando pelo canvas.

Para adicionar uma árvore, clique no botão *Nova Árvore* e escreva um nome para ela.

Para selecionar uma árvore, clique na combobox e selecione a árvore desejada.

Para remover uma árvore, selecione a árvore desejada e clique em *Remover Árvore*.

Para selecionar um nó, digite o valor/nome dado a ele na caixa de *Nó Pai*, ou clique no nó desejado no canvas à direita da aplicação.

Para adicionar um nó, selecione o nó pai, escreva um valor/nome na caixa de *Novo Nó* e aperte no botão de *Adicionar Nó*.

Para remover um nó, selecione um nó que não seja a raiz escrevendo seu valor/nome na caixa de *Nó a Remover* ou clicando no canvas e aperte no botão de *Remover Nó*. 
