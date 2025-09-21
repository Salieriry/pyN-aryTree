import tkinter as tk
from tkinter import ttk, messagebox
from arvore import Node

# Interface gráfica para visualização e manipulação da árvore n-ária
class TreeGUI:
    # Construtor da classe TreeGUI
    def __init__(self, master):
        self.master = master # Referência para a janela principal
        self.master.title("Visualizador de Árvore N-ária") # Título da janela
        self.master.geometry("1200x700") # Tamanho da janela
        
        # Cores padrão
        self.colors = {
            'bg': '#2b2b2b',
            'canvas_bg': '#1e1e1e',
            'node_default': '#4a9eff',
            'node_selected': '#66ff66',
            'node_hover': '#66b3ff',
            'node_border': '#ffffff',
            'text': '#ffffff',
            'line': '#808080',
            'root_node': '#ff6b6b',
            'panel_bg': '#333333',
            'button_bg': '#4a9eff',
            'button_hover': '#66b3ff',
            'entry_bg': '#404040',
            'entry_fg': '#ffffff'
        }
        
        self.trees = []  # Lista para armazenar múltiplas árvores 
        self.current_tree_index = -1  # Índice da árvore atualmente selecionada 
        self.selected_node = None  # Nó atualmente selecionado na interface
        self.selected_tree = None  # Árvore atualmente selecionada na interface
        
        # Variáveis para drag and drop
        self.dragging = False  # Flag para indicar se o canvas está sendo arrastado
        self.drag_data = {"x": 0, "y": 0, "item": None, "node": None, "node_id": None} # Dados do arrasto
        
        # Variável para controle de hover
        self.last_hovered = None
        
        self.custom_positions = {}  # Dicionário para armazenar posições personalizadas dos nós
        self.node_positions = {}  # Dicionário para armazenar posições atuais dos nós
        
        self.setup_styles() # Configura estilos visuais
        
        self.create_widgets() # Configura os widgets da interface
        
        self.master.after(100, self.add_new_tree)  # Aguardar canvas renderizar
    
    
    # Configura estilos visuais da interface    
    def setup_styles(self):
        style = ttk.Style() # Estilo ttk
        style.theme_use('clam') # Tema 'clam' para melhor customização
        
                    
        style.configure('TNotebook', background=self.colors['panel_bg'])
        style.configure('TNotebook.Tab', background=self.colors['panel_bg'],
                        foreground=self.colors['text'], padding=[20, 10])
        style.map('TNotebook.Tab', background=[('selected', self.colors['button_bg'])])
        
        # Configurar botões
        style.configure('Modern.TButton', 
                       background=self.colors['button_bg'],
                       foreground=self.colors['text'],
                       borderwidth=0,
                       focuscolor='none',
                       padding=(10, 5))
        style.map('Modern.TButton',
                 background=[('active', self.colors['button_hover'])])
        
    # Cria os widgets da interface     
    def create_widgets(self):
        self.master.configure(bg=self.colors['bg'])
        
        # Frame principal
        main_frame = tk.Frame(self.master, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                
        # Frame lateral para controles
        control_frame = tk.Frame(main_frame, bg=self.colors['panel_bg'], width=350)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0,10))
        control_frame.pack_propagate(False)
        
        # Título
        title_label = tk.Label(control_frame, text="Controles da Árvore", 
                               font=("Segoe UI", 16, "bold"),
                               bg=self.colors['panel_bg'], 
                               fg=self.colors['text'])
        title_label.pack(pady=(20, 10))
        
        # Frame para gerenciar múltiplas árvores
        tree_mgmt_frame = tk.LabelFrame(control_frame, text="Gerenciar Árvores",
                                        bg=self.colors['panel_bg'],
                                        fg=self.colors['text'],
                                        font=("Segoe UI", 10, "bold"))
        tree_mgmt_frame.pack(padx=20, pady=10, fill=tk.X)
        
        # Combobox para selecionar árvore
        tk.Label(tree_mgmt_frame, text="Árvore Atual:",
                bg=self.colors['panel_bg'], fg=self.colors['text']).pack(pady=5)
        
        self.tree_combo = ttk.Combobox(tree_mgmt_frame, state="readonly", width=25)
        self.tree_combo.pack(padx=10, pady=5)
        self.tree_combo.bind("<<ComboboxSelected>>", self.on_tree_selected)
        
        # Botão para adicionar nova árvore
        btn_frame = tk.Frame(tree_mgmt_frame, bg=self.colors['panel_bg'])
        btn_frame.pack(pady=10)
        
        self.create_button(btn_frame, "Nova Árvore", self.add_new_tree).pack(side=tk.LEFT, padx=5)
        self.create_button(btn_frame, "Remover Árvore", self.remove_current_tree).pack(side=tk.LEFT, padx=5)
        
        ttk.Separator(control_frame, orient='horizontal').pack(fill=tk.X, padx=20, pady=10) # Separador
                
        # Frame para adicionar nós
        add_frame = tk.LabelFrame(control_frame, text="Adicionar Nó",
                                 bg=self.colors['panel_bg'],
                                 fg=self.colors['text'],
                                 font=("Segoe UI", 10, "bold"))
        add_frame.pack(padx=20, pady=10, fill=tk.X)
        
        # Entrada para nó pai
        tk.Label(add_frame, text="Nó Pai:", 
                bg=self.colors['panel_bg'], fg=self.colors['text']).pack(pady=5)
        self.parent_entry = self.create_entry(add_frame)
        self.parent_entry.pack(padx=10, pady=5, fill=tk.X)
        
        # Entrada para novo nó
        tk.Label(add_frame, text="Novo Nó:", 
                bg=self.colors['panel_bg'], fg=self.colors['text']).pack(pady=5)
        self.new_node_entry = self.create_entry(add_frame)
        self.new_node_entry.pack(padx=10, pady=5, fill=tk.X)
        
        # Botão adicionar
        self.create_button(add_frame, "Adicionar Nó", self.add_node).pack(pady=10)
        
        # Separador
        ttk.Separator(control_frame, orient='horizontal').pack(fill=tk.X, padx=20, pady=10)
        
        # Frame para remover nós
        remove_frame = tk.LabelFrame(control_frame, text="Remover Nó",
                                    bg=self.colors['panel_bg'],
                                    fg=self.colors['text'],
                                    font=("Segoe UI", 10, "bold"))
        remove_frame.pack(padx=20, pady=10, fill=tk.X)
        
        tk.Label(remove_frame, text="Nó a Remover:", 
                bg=self.colors['panel_bg'], fg=self.colors['text']).pack(pady=5)
        self.remove_entry = self.create_entry(remove_frame)
        self.remove_entry.pack(padx=10, pady=5, fill=tk.X)
        
        self.create_button(remove_frame, "Remover Nó", self.remove_node).pack(pady=10)
        
        # Separador
        ttk.Separator(control_frame, orient='horizontal').pack(fill=tk.X, padx=20, pady=10)
        
        
        # Canvas para desenhar a árvore
        canvas_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Canvas com scrollbars
        self.canvas = tk.Canvas(canvas_frame, bg=self.colors['canvas_bg'], 
                               highlightthickness=0)
        
        # Scrollbars
        h_scroll = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        v_scroll = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
        
        # Pack do canvas e scrollbars
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.spacing_var = tk.IntVar(value=80)
        
        # Bindings do canvas
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_drag_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_drag_release)
        self.canvas.bind("<Motion>", self.on_hover)
        
        # Status bar
        self.status_bar = tk.Label(self.master, text="Pronto", 
                                  bg=self.colors['panel_bg'], 
                                  fg=self.colors['text'],
                                  anchor=tk.W, relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    # Método para criar botões estilizados    
    def create_button(self, parent, text, command):
        return tk.Button(parent, text=text, command=command,
                        bg=self.colors['button_bg'], fg=self.colors['text'],
                        font=("Segoe UI", 10), bd=0, padx=15, pady=8,
                        activebackground=self.colors['button_hover'],
                        activeforeground=self.colors['text'],
                        cursor="hand2")
    
    # Método para criar entradas estilizadas    
    def create_entry(self, parent):
        
        return tk.Entry(parent, bg=self.colors['entry_bg'], fg=self.colors['entry_fg'],
                       font=("Segoe UI", 10), bd=0, insertbackground=self.colors['text'])
            
    # Método para desenhar a árvore no canvas    
    def add_new_tree(self):
        
        tree_name = f"Árvore {len(self.trees) + 1}"
        
        if len(self.trees) > 0:
            # Pedir nome personalizado para a árvore
            dialog = tk.Toplevel(self.master)
            dialog.title("Nova Árvore")
            dialog.configure(bg=self.colors['panel_bg'])
            dialog.geometry("300x150")
            
            tk.Label(dialog, text="Nome da nova árvore:",
                    bg=self.colors['panel_bg'], fg=self.colors['text']).pack(pady=10)
            
            name_entry = self.create_entry(dialog)
            name_entry.insert(0, tree_name)
            name_entry.pack(padx=20, pady=10, fill=tk.X)
            
            def confirm():
                nonlocal tree_name
                tree_name = name_entry.get() or tree_name
                dialog.destroy()
            
            self.create_button(dialog, "Criar", confirm).pack(pady=10)
            dialog.wait_window()
        
        # Criar nova árvore
        new_tree = {
            'name': tree_name,
            'root': Node(f"Root_{tree_name}"),
            'positions': {}
        }
        
        self.trees.append(new_tree)
        self.update_tree_combo()
        self.tree_combo.current(len(self.trees) - 1)
        self.on_tree_selected()
        
        self.status_bar.config(text=f"Nova árvore '{tree_name}' criada")
        
    # Método para remover a árvore atual    
    def remove_current_tree(self):
        
        if len(self.trees) <= 1:
            messagebox.showwarning("Aviso", "Deve haver pelo menos uma árvore!")
            return
        
        if messagebox.askyesno("Confirmar", f"Remover árvore '{self.trees[self.current_tree_index]['name']}'?"):
            del self.trees[self.current_tree_index]
            self.update_tree_combo()
            self.tree_combo.current(0)
            self.on_tree_selected()
    
    # Atualiza a combobox de seleção de árvores
    def update_tree_combo(self):
        
        self.tree_combo['values'] = [tree['name'] for tree in self.trees]
    
    # Método chamado ao selecionar uma árvore
    def on_tree_selected(self, event=None):
        
        if self.tree_combo.current() >= 0:
            self.current_tree_index = self.tree_combo.current()
            self.selected_node = None
            self.last_hovered = None  # Limpar hover ao mudar de árvore
            self.custom_positions = self.trees[self.current_tree_index]['positions']
            self.draw_tree()
            self.parent_entry.delete(0, tk.END)
            self.parent_entry.insert(0, self.trees[self.current_tree_index]['root'].value)
                
                            
    # Método auxiliar para calcular dimensões da árvore    
    def _calculate_tree_dimensions(self, node):
        
        def count_leaves(n):
            if not n.children:
                return 1
            return sum(count_leaves(child) for child in n.children)
        
        def get_depth(n, d=0):
            if not n.children:
                return d
            return max(get_depth(child, d+1) for child in n.children)
        
        self.tree_leaves = count_leaves(node)
        self.tree_depth = get_depth(node)
       
    # Método para clarear uma cor hex            
    def _lighten_color(self, color, amount):
        
        color = color.lstrip('#')
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, r + amount)
        g = min(255, g + amount)
        b = min(255, b + amount)
        return f'#{r:02x}{g:02x}{b:02x}'
    
    # Obtém todos os descendentes de um nó
    def get_node_descendants(self, node_value):
        descendants = []
        tree = self.trees[self.current_tree_index]['root']
        node = tree.find(node_value)
        
        if node:
            # Função recursiva para coletar todos os descendentes
            def collect_descendants(n):
                for child in n.children:
                    descendants.append(child.value)
                    collect_descendants(child)
            
            collect_descendants(node)
        
        return descendants
        
    # Método para efeito hover nos nós
    def on_hover(self, event):
        
        # Verificar se há árvore atual
        if self.current_tree_index < 0 or not self.trees:
            return
        
        # Encontrar items sob o cursor (área ligeiramente maior para melhor detecção)
        overlapping = self.canvas.find_overlapping(event.x-2, event.y-2, event.x+2, event.y+2)
        
        # Resetar hover anterior se existir
        if hasattr(self, 'last_hovered') and self.last_hovered:
            # Só resetar se não for o nó selecionado
            if not (self.selected_node and self.selected_node.value == self.last_hovered):
                tree = self.trees[self.current_tree_index]['root']
                node = tree.find(self.last_hovered)
                
                # Determinar cor base correta para reset
                if node == tree:
                    base_color = self.colors['root_node']
                else:
                    base_color = self.colors['node_default']
                
                # Resetar gradiente
                for i in range(3):
                    layer_items = self.canvas.find_withtag(f"node_bg_layer_{i}_{self.last_hovered}")
                    color = self._lighten_color(base_color, i * 20)
                    for item in layer_items:
                        self.canvas.itemconfig(item, fill=color)
            
            self.last_hovered = None
        
        # Verificar se está sobre um hitbox
        hovered_node = None
        for item in overlapping:
            tags = self.canvas.gettags(item)
            if "hitbox" in tags:
                for tag in tags:
                    if tag.startswith("hitbox_") and not tag == "hitbox":
                        hovered_node = tag.replace("hitbox_", "")
                        break
                if hovered_node:
                    break
        
        # Aplicar hover se sobre um nó
        if hovered_node:
            # Não aplicar hover se for o nó selecionado
            if not (self.selected_node and self.selected_node.value == hovered_node):
                # Aplicar gradiente de hover
                for i in range(3):
                    layer_items = self.canvas.find_withtag(f"node_bg_layer_{i}_{hovered_node}")
                    color = self._lighten_color(self.colors['node_hover'], i * 20)
                    for item in layer_items:
                        self.canvas.itemconfig(item, fill=color)
                self.last_hovered = hovered_node
            self.canvas.config(cursor="hand2")
        else:
            self.canvas.config(cursor="")
    
    # Método para manipular clique no canvas
    def on_canvas_click(self, event):
        
        # Encontrar items sob o clique (área ligeiramente maior para melhor detecção)
        overlapping = self.canvas.find_overlapping(event.x-2, event.y-2, event.x+2, event.y+2)
        
        clicked_node = None
        node_id = None
        
        # Procurar por hitbox clicada
        for item in overlapping:
            tags = self.canvas.gettags(item)
            if "hitbox" in tags:
                for tag in tags:
                    if tag.startswith("hitbox_") and not tag == "hitbox":
                        clicked_node = tag.replace("hitbox_", "")
                    elif "_" in tag and not tag.startswith("hitbox"):
                        node_id = tag
                if clicked_node and node_id:
                    break
        
        if clicked_node and node_id:
            tree_index, node_value = node_id.split('_', 1)
            
            if int(tree_index) == self.current_tree_index:
                # Selecionar nó
                tree = self.trees[self.current_tree_index]['root']
                node = tree.find(node_value)
                
                if node:
                    self.select_node(node)
                    
                    # Iniciar drag
                    self.dragging = True
                    self.drag_data["x"] = event.x
                    self.drag_data["y"] = event.y
                    self.drag_data["node"] = node_value
                    self.drag_data["node_id"] = node_id
                    
    # Métodos para drag and drop dos nós
    def on_drag_motion(self, event):
        if self.dragging and self.drag_data["node"]:
            # Calcular delta
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]
            
            node_value = self.drag_data["node"]
            
            # Mover o nó principal
            for item in self.canvas.find_withtag(f"node_element_{node_value}"):
                self.canvas.move(item, dx, dy)
            
            # Mover hitbox do nó principal
            for item in self.canvas.find_withtag(f"hitbox_{node_value}"):
                self.canvas.move(item, dx, dy)
            
            # IMPORTANTE: Mover todos os descendentes também
            descendants = self.get_node_descendants(node_value)
            for desc_value in descendants:
                # Mover elementos do descendente
                for item in self.canvas.find_withtag(f"node_element_{desc_value}"):
                    self.canvas.move(item, dx, dy)
                
                # Mover hitbox do descendente
                for item in self.canvas.find_withtag(f"hitbox_{desc_value}"):
                    self.canvas.move(item, dx, dy)
            
            # Mover apenas as linhas conectadas ao nó e seus descendentes
            # Criar conjunto de todos os nós sendo movidos
            moved_nodes = {node_value} | set(descendants)
            
            # Mover linhas que partem destes nós
            for moved_node in moved_nodes:
                for item in self.canvas.find_withtag(f"line_from_{moved_node}"):
                    self.canvas.move(item, dx, dy)
            
            # Mover linha que chega ao nó principal (do pai para ele)
            for item in self.canvas.find_withtag(f"line_to_{node_value}"):
                self.canvas.move(item, dx, dy)
            
            # Atualizar posição de referência
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

    # Método chamado ao soltar o nó arrastado
    def on_drag_release(self, event):
        if self.dragging and self.drag_data["node"]:
            node_value = self.drag_data["node"]
            node_id = self.drag_data["node_id"]
            
            # Coletar todos os nós movidos (principal + descendentes)
            moved_nodes = [node_value] + self.get_node_descendants(node_value)
            
            # Para cada nó movido, salvar sua nova posição
            for moved_node_value in moved_nodes:
                moved_node_id = f"{self.current_tree_index}_{moved_node_value}"
                
                # Encontrar a hitbox para obter as coordenadas atuais
                hitbox_items = self.canvas.find_withtag(f"hitbox_{moved_node_value}")
                if hitbox_items:
                    coords = self.canvas.coords(hitbox_items[0])
                    if len(coords) >= 4:
                        x = (coords[0] + coords[2]) / 2
                        y = (coords[1] + coords[3]) / 2
                        
                        # Salvar posição customizada
                        self.custom_positions[moved_node_id] = (x, y)
                        self.trees[self.current_tree_index]['positions'][moved_node_id] = (x, y)
            
            # Redesenhar para garantir que tudo está sincronizado
            # (principalmente as linhas de conexão)
            self.draw_tree()
            
            # Se o nó estava selecionado, mantê-lo selecionado após o redesenho
            if self.selected_node and self.selected_node.value == node_value:
                tree = self.trees[self.current_tree_index]['root']
                node = tree.find(node_value)
                if node:
                    self.select_node(node)
        
        # Resetar dados do drag
        self.dragging = False
        self.drag_data = {"x": 0, "y": 0, "item": None, "node": None, "node_id": None}
                    
    # Método para desenhar a árvore no canvas
    def draw_tree(self):
        
        self.canvas.delete("all")
        
        # Limpar dicionário de posições
        self.node_positions = {}
        
        if self.current_tree_index < 0 or not self.trees:
            return
        
        tree = self.trees[self.current_tree_index]['root']
        
        if tree:
            # Calcular dimensões da árvore
            self._calculate_tree_dimensions(tree)
            
            canvas_width = self.canvas.winfo_width() or 800
            start_x = canvas_width // 2
            start_y = 60
            
            # Desenhar a árvore
            self._draw_node(tree, start_x, start_y, canvas_width // 2, None, None, None)
            
            # Atualizar região de scroll
            bbox = self.canvas.bbox("all")
            if bbox:
                padding = 50
                x1, y1, x2, y2 = bbox
                self.canvas.config(scrollregion=(x1-padding, y1-padding, 
                                                 x2+padding, y2+padding))
                    
    # Método recursivo para desenhar cada nó
    def _draw_node(self, node, x, y, h_spacing, parent_x=None, parent_y=None, parent_value=None):
        node_id = f"{self.current_tree_index}_{node.value}"
        
        # Verificar se existe posição customizada
        if node_id in self.custom_positions:
            x, y = self.custom_positions[node_id]
        
        # Salvar posição do nó para referência
        self.node_positions = getattr(self, 'node_positions', {})
        self.node_positions[node.value] = (x, y)
        
        # Desenhar linha do pai se existir
        if parent_x is not None and parent_y is not None and parent_value is not None:
            # Criar linha curva com tags específicas
            mid_y = (parent_y + y) // 2
            self.canvas.create_line(parent_x, parent_y + 25, parent_x, mid_y,
                                x, mid_y, x, y - 25,
                                fill=self.colors['line'], width=2, smooth=True,
                                tags=("line", f"line_from_{parent_value}", f"line_to_{node.value}"))
        
        # Determinar cor do nó
        node_color = self.colors['node_default']
        if node == self.trees[self.current_tree_index]['root']:
            node_color = self.colors['root_node']
        if self.selected_node and self.selected_node.value == node.value:
            node_color = self.colors['node_selected']
        
        # Tag única para todos os elementos deste nó
        node_tag = f"node_element_{node.value}"
        
        # Criar gradiente visual (simulado com múltiplos círculos)
        for i in range(3):
            radius = 25 - i * 2
            color = self._lighten_color(node_color, i * 20)
            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                                fill=color, outline="",
                                tags=(node_tag, f"node_bg_{node.value}", f"node_bg_layer_{i}_{node.value}"))
        
        # Círculo principal do nó
        self.canvas.create_oval(x - 22, y - 22, x + 22, y + 22,
                            fill="", outline=self.colors['node_border'], width=2,
                            tags=(node_tag, f"node_circle_{node.value}"))
        
        # Texto do nó
        self.canvas.create_text(x, y, text=node.value,
                            font=("Segoe UI", 10, "bold"),
                            fill=self.colors['text'],
                            tags=(node_tag, f"node_text_{node.value}"))
        
        # Desenhar filhos ANTES da hitbox
        if node.children:
            child_count = len(node.children)
            spacing = self.spacing_var.get()
            
            # Calcular largura total necessária
            total_width = (child_count - 1) * spacing
            start_x = x - total_width // 2
            
            for i, child in enumerate(node.children):
                child_x = start_x + i * spacing
                child_y = y + 120
                
                # Reduzir espaçamento para níveis mais profundos
                new_h_spacing = max(h_spacing * 0.7, 40)
                self._draw_node(child, child_x, child_y, new_h_spacing, x, y, node.value)
        
        # Criar hitbox invisível POR ÚLTIMO (área clicável maior)
        # Isso garante que a hitbox fique acima de todos os outros elementos
        hitbox_radius = 30
        self.canvas.create_oval(x - hitbox_radius, y - hitbox_radius, 
                            x + hitbox_radius, y + hitbox_radius,
                            fill="", outline="",
                            tags=("hitbox", f"hitbox_{node.value}", node_id))
        
        # Levantar a hitbox para o topo
        self.canvas.tag_raise(f"hitbox_{node.value}")
    
    # Método para selecionar um nó
    def select_node(self, node):
        
        # Desselecionar nó anterior se existir
        if self.selected_node and self.selected_node != node:
            # Resetar gradiente do nó anterior
            tree = self.trees[self.current_tree_index]['root']
            old_node = tree.find(self.selected_node.value)
            if old_node == tree:
                base_color = self.colors['root_node']
            else:
                base_color = self.colors['node_default']
            
            for i in range(3):
                layer_items = self.canvas.find_withtag(f"node_bg_layer_{i}_{self.selected_node.value}")
                color = self._lighten_color(base_color, i * 20)
                for item in layer_items:
                    self.canvas.itemconfig(item, fill=color)
        
        self.selected_node = node
        
        # Aplicar gradiente de seleção
        for i in range(3):
            layer_items = self.canvas.find_withtag(f"node_bg_layer_{i}_{node.value}")
            color = self._lighten_color(self.colors['node_selected'], i * 20)
            for item in layer_items:
                self.canvas.itemconfig(item, fill=color)
        
        # Atualizar entradas
        self.parent_entry.delete(0, tk.END)
        self.parent_entry.insert(0, node.value)
        self.remove_entry.delete(0, tk.END)
        self.remove_entry.insert(0, node.value)
        
        self.status_bar.config(text=f"Nó '{node.value}' selecionado")
    
    # Método para adicionar um novo nó
    def add_node(self):
        
        if self.current_tree_index < 0:
            messagebox.showwarning("Aviso", "Selecione uma árvore primeiro!")
            return
        
        parent_value = self.parent_entry.get().strip()
        new_value = self.new_node_entry.get().strip()
        
        if not parent_value or not new_value:
            messagebox.showwarning("Entrada Inválida", 
                                  "Por favor, preencha todos os campos.")
            return
        
        tree = self.trees[self.current_tree_index]['root']
        parent_node = tree.find(parent_value)
        
        if parent_node:
            # Verificar duplicata
            if tree.find(new_value):
                messagebox.showwarning("Nó Duplicado", 
                                      f"Já existe um nó com o valor '{new_value}'")
                return
            
            parent_node.insert(new_value)
            self.new_node_entry.delete(0, tk.END)
            self.draw_tree()
            self.status_bar.config(text=f"Nó '{new_value}' adicionado sob '{parent_value}'")
        else:
            messagebox.showerror("Erro", f"Nó pai '{parent_value}' não encontrado!")
    
    # Método para remover um nó
    def remove_node(self):
        
        if self.current_tree_index < 0:
            messagebox.showwarning("Aviso", "Selecione uma árvore primeiro!")
            return
        
        node_value = self.remove_entry.get().strip()
        
        if not node_value:
            messagebox.showwarning("Entrada Inválida", 
                                  "Por favor, insira o valor do nó a ser removido.")
            return
        
        tree = self.trees[self.current_tree_index]['root']
        
        if node_value == tree.value:
            messagebox.showwarning("Remoção Inválida", 
                                  "Não é possível remover o nó raiz!")
            return
        
        if messagebox.askyesno("Confirmar Remoção", 
                               f"Remover nó '{node_value}' e todos os seus filhos?"):
            if tree.remove(node_value):
                # Remover posições customizadas do nó removido
                node_id = f"{self.current_tree_index}_{node_value}"
                if node_id in self.custom_positions:
                    del self.custom_positions[node_id]
                
                # Limpar seleção se o nó removido era o selecionado
                if self.selected_node and self.selected_node.value == node_value:
                    self.selected_node = None
                
                self.remove_entry.delete(0, tk.END)
                self.draw_tree()
                self.status_bar.config(text=f"Nó '{node_value}' removido com sucesso")
            else:
                messagebox.showerror("Erro", f"Nó '{node_value}' não encontrado!")