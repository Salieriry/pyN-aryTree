import tkinter as tk
from tkinter import messagebox
from arvore import Node

class TreeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Visualizador de Árvore N-ária")
        self.master.geometry("800x600")
        
        self.tree = Node("Root")  # Inicializa a árvore com um nó raiz
        
        control_frame = tk.Frame(self.master, padx=10, pady=10)
        control_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        tk.Label(control_frame, text="Root:").grid(row=0, column=0, padx=5, pady=5)
        self.parent_entry = tk.Entry(control_frame)
        self.parent_entry.grid(row=0, column=1, padx=5, pady=5)
        
        
        self.parent_entry.insert(0, "Root")
        
        tk.Label(control_frame, text="New Node").grid(row=0, column=2, padx=5, pady=5)
        self.new_node_entry = tk.Entry(control_frame)
        self.new_node_entry.grid(row=0, column=3, padx=5, pady = 5)
        

        
        self.add_button = tk.Button(control_frame, text="Add", command=self.add_node)
        self.add_button.grid(row=0, column=4, padx=10, pady=5)
        
        tk.Label(control_frame, text="Remove Node:").grid(row=1, column=0, padx=5, pady=5)
        self.remove_entry = tk.Entry(control_frame)
        self.remove_entry.grid(row=1, column=1, padx=5, pady=5)
        
        
        self.remove_button = tk.Button(control_frame, text="Remove", command=self.remove_node)
        self.remove_button.grid(row=1, column=4, padx=10, pady=5)
        
        
        
        
    def add_node(self):
        parent_value = self.parent_entry.get()
        new_node_value = self.new_node_entry.get()
        
        if not parent_value or not new_node_value:
            print("Entrada inválida.")
            return
        
        parent_node = self.tree.find(parent_value)
        
        if parent_node:
            parent_node.insert(new_node_value)
            print(f"Nó '{new_node_value}' adicionado sob '{parent_value}'.")
            self.new_node_entry.delete(0, tk.END)
            self.tree.display()
        else: 
            print(f"Nó pai '{parent_value}' não encontrado.") 
        
    def remove_node(self):
        node_to_remove = self.remove_entry.get()
        
        if not node_to_remove:
            messagebox.showwarning("Entrada Inválida", "Por favor, insira o valor do nó a ser removido.")
            return  
        
        if node_to_remove == self.tree.value:
            messagebox.showwarning("Remoção Inválida", "Não é possível remover o nó raiz.")
            return
        
        if self.tree.remove(node_to_remove):
            print(f"Nó '{node_to_remove}' removido.")
            self.remove_entry.delete(0, tk.END)
            self.tree.display()
        else:
            print(f"Nó '{node_to_remove}' não encontrado.")
        
        
        
if __name__ == "__main__":
    root = tk.Tk()
    app = TreeGUI(root)
    root.mainloop()