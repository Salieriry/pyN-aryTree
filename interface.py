import tkinter as tk
from tkinter import messagebox
from arvore import Node

# Interface gráfica para visualização e manipulação da árvore n-ária
class TreeGUI:
    # Construtor da classe TreeGUI
    def __init__(self, master):
        self.master = master # Referência para a janela principal
        self.master.title("Visualizador de Árvore N-ária") # Título da janela
        self.master.geometry() # Tamanho da janela
        
        self.tree = Node("Root")  # Inicializa a árvore com um nó raiz
        self.selected_node = None  # Nó atualmente selecionado (inicialmente nenhum)
        
        # Frame para os controles de adicionar e remover nós
        control_frame = tk.Frame(self.master, padx=10, pady=10)
        control_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Controles para adicionar e remover nós
        tk.Label(control_frame, text="Root:").grid(row=0, column=0, padx=5, pady=5)
        self.parent_entry = tk.Entry(control_frame)
        self.parent_entry.grid(row=0, column=1, padx=5, pady=5)
        
        
        self.parent_entry.insert(0, "Root")
        
        # Entrada para o valor do novo nó
        tk.Label(control_frame, text="New Node").grid(row=0, column=2, padx=5, pady=5)
        self.new_node_entry = tk.Entry(control_frame)
        self.new_node_entry.grid(row=0, column=3, padx=5, pady = 5)
        

        # Botão para adicionar o novo nó
        self.add_button = tk.Button(control_frame, text="Add", command=self.add_node)
        self.add_button.grid(row=0, column=4, padx=10, pady=5)
        
        # Controles para remover um nó
        tk.Label(control_frame, text="Remove Node:").grid(row=1, column=0, padx=5, pady=5)
        self.remove_entry = tk.Entry(control_frame)
        self.remove_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Botão para remover o nó especificado
        self.remove_button = tk.Button(control_frame, text="Remove", command=self.remove_node)
        self.remove_button.grid(row=1, column=4, padx=10, pady=5)
        
        # Canvas para desenhar a árvore
        canvas_frame = tk.Frame(self.master)
        canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(canvas_frame, bg="ivory")
        
        h_scroll = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        v_scroll = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
        
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        
        
        # Desenha a árvore inicialmente
        self.master.after(100, self.draw_tree)
        
        
    # Método para desenhar a árvore no canvas    
    def draw_tree(self):
        self.canvas.delete("all") # Limpa o canvas antes de redesenhar a árvore
        
        self.canvas.tag_bind("node", "<Button-1>", self._on_node_click)
        
        # Desenha a árvore recursivamente a partir do nó raiz
        if self.tree:
            
            landscape_width = 2000
                      
            start_x = landscape_width // 2 # Posição x inicial para desenhar o nó raiz
            start_y = 50 # Posição y inicial para desenhar o nó raiz
            
            h_spacing = landscape_width // 4 # Espaçamento horizontal entre os nós
                   
            # Chama o método recursivo para desenhar os nós
            self._recursive_node_draw(self.tree, start_x, start_y, h_spacing)
            
            bbox = self.canvas.bbox("all")
            if bbox:
                self.canvas.config(scrollregion=bbox)
    
    # Método recursivo para desenhar cada nó e seus filhos        
    def _recursive_node_draw(self, node, x, y, h_spacing):
        node_radius = 20 # Raio do círculo que representa o nó
        radius_hitbox = node_radius + 5 # Raio da área clicável do nó
        vertical_spacing = 100 # Espaçamento vertical entre os níveis da árvore
        
        # Desenha a área clicável do nó (hitbox)
        self.canvas.create_oval(
            x - radius_hitbox, y - radius_hitbox, x + radius_hitbox, y + radius_hitbox,
            fill="", outline="", tags=("node", node.value)
        )
        
        # Desenha o nó atual como um círculo com o valor do nó
        self.canvas.create_oval(
            x - node_radius, y - node_radius, x + node_radius, y + node_radius,
            fill="skyblue", outline="black", tags=(f"visual_{node.value}",)
        )
        
        # Desenha o valor do nó no centro do círculo
        self.canvas.create_text(x, y, text=node.value, font=("Arial", 10, "bold"))
        
        # Calcula a posição dos filhos e desenha as linhas de conexão
        child_count = len(node.children)
        if child_count > 0:
            child_total_width = (child_count - 1) * h_spacing
            x_start_child = x - child_total_width // 2
            
            for i, child in enumerate(node.children):
                x_child = x_start_child + i * h_spacing
                y_child = y + vertical_spacing
                
                self.canvas.create_line(x, y + node_radius, x_child, y_child - node_radius, width=1)
                
                self._recursive_node_draw(child, x_child, y_child, h_spacing * 0.5)
                
    def _on_node_click(self, event):
        item_id_list = self.canvas.find_withtag("current")
        if not item_id_list: return
        
        item_id = item_id_list[0]
        
        tags = self.canvas.gettags(item_id)
        if len(tags) < 2: return
        
        node_value = tags[1]
        
        if self.selected_node:
            self.canvas.itemconfig(f"visual_{self.selected_node.value}", fill="skyblue")
            
        self.selected_node = self.tree.find(node_value)
        
        if self.selected_node:
            self.canvas.itemconfig(f"visual_{node_value}", fill="lightgreen")
        
        self.parent_entry.delete(0, tk.END)
        self.parent_entry.insert(0, node_value)
        
        self.remove_entry.delete(0, tk.END)
        self.remove_entry.insert(0, node_value)                    
    
    # Método para adicionar um novo nó à árvore    
    def add_node(self):
        parent_value = self.parent_entry.get() # Valor do nó pai onde o novo nó será adicionado
        new_node_value = self.new_node_entry.get() # Valor do novo nó a ser adicionado
        
        # Validações básicas para entradas vazias
        if not parent_value or not new_node_value:
            print("Entrada inválida.")
            return
        
        # Procura o nó pai na árvore
        parent_node = self.tree.find(parent_value)
        
        # Se o nó pai for encontrado, insere o novo nó como filho
        if parent_node:
            parent_node.insert(new_node_value)
            print(f"Nó '{new_node_value}' adicionado sob '{parent_value}'.")
            self.new_node_entry.delete(0, tk.END)
            self.draw_tree()
        else: 
            print(f"Nó pai '{parent_value}' não encontrado.") 
    
    # Método para remover um nó da árvore    
    def remove_node(self):
        node_to_remove = self.remove_entry.get()
        
        # Validação básica para entrada vazia
        if not node_to_remove:
            messagebox.showwarning("Entrada Inválida", "Por favor, insira o valor do nó a ser removido.")
            return  
        
        # Impede a remoção do nó raiz
        if node_to_remove == self.tree.value:
            messagebox.showwarning("Remoção Inválida", "Não é possível remover o nó raiz.")
            return
        
        # Tenta remover o nó especificado
        if self.tree.remove(node_to_remove):
            print(f"Nó '{node_to_remove}' removido.")
            self.remove_entry.delete(0, tk.END)
            self.draw_tree()
        else:
            print(f"Nó '{node_to_remove}' não encontrado.")
    

        
        
        
if __name__ == "__main__":
    root = tk.Tk()
    app = TreeGUI(root)
    root.mainloop()