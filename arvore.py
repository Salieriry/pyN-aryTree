class Node:
    
    
    # Construtor da classe Node
    def __init__(self, value): # Inicializa o nó com um valor e uma lista vazia de filhos
        self.value = value
        self.children = []
        
        
        
    # Método para inserir um novo nó filho    
    def insert(self, value):
        new_node = Node(value)  # Cria um novo nó com o valor fornecido 
        self.children.append(new_node) # Adiciona o novo nó à lista de filhos do nó atual
    
    
    
    # Método para remover um nó com um valor específico
    def remove(self, value):
        
        # Verifica se o valor do nó atual é o valor procurado
        for i, child in enumerate(self.children):
            if child.value == value:
                self.children.pop(i)  # Remove o nó filho com o valor especificado
                return True
        
        # Percorre os filhos do nó atual para procurar o valor    
        for child in self.children:
            if child.remove(value):  # Chama recursivamente o método remove nos filhos
                return True
        
        return False  # Retorna False se o valor não for encontrado
            
    
    
    # Método para buscar um nó com um valor específico
    def find(self, value):
        # Verifica se o valor do nó atual é o valor procurado
        if self.value == value:
            return self
        
        # Percorre os filhos do nó atual para procurar o valor
        for filho in self.children:
            found_node = filho.find(value)
            
            # Se o nó for encontrado em um dos filhos, retorna o nó encontrado
            if found_node:
                return found_node
        
        # Se o valor não for encontrado, retorna None    
        return None
    
    
    # Método para exibir a árvore a partir do nó atual
    def display(self):
        print(self.value)  # Exibe o valor do nó raiz
        self._recursive_display(self, "")  # Chama o método auxiliar para exibir a árvore recursivamente
     
     
       
    # Método auxiliar para exibir a árvore recursivamente   
    def _recursive_display(self, node, prefix):
        
        # Obtém os filhos do nó atual
        children = node.children
        # Percorre os filhos do nó atual
        for i, child in enumerate(children):
            is_last = (i == len(children) - 1)  # Verifica se o nó atual é o último filho
            connector = "└── " if is_last else "├── "  # Define o conector apropriado
            print(prefix + connector + str(child.value))  # Exibe o valor do nó filho com o prefixo adequado
            new_prefix = prefix + ("    " if is_last else "│   ")  # Atualiza o prefixo para os filhos do nó atual
            
            self._recursive_display(child, new_prefix)  # Chama recursivamente para exibir os filhos do nó atual
            
            
