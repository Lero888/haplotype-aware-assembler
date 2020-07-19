class Graph:
    
    
    def __init__(self):
        
        self.node_set = set()
        self.next = {}
        self.num_node = 0
        self.edges = 0
                
    
    def num_of_node(self):
        
        """ return total number of nodes in the graph """
        
        try:
            return self.num_node
        except:
            print("ERROR: No graph exists")
            
    def num_of_edge(self):
        
        """ return total number od edges in the graph """
        try:
            return self.edges
        except:
            print("ERROR: No graph exists")
            
            
    def add_node(self, node):
        """ add nodes to the graph """
        
        if node in self.node_set:
            return 
        
        self.num_node = self.num_node + 1
        self.node_set.add(node)
        self.next[node] = []
        
    def add_edge(self, u, v):
        """ add edges between the nodes """
        
        self.add_node(u)
        self.add_node(v)
        
        if v not in self.next[u]:
            self.next[u].append(v)
            self.next[v].append(u)
            self.edges += 2
            
        else:
            print("ERROR: Edges between ", u, " and ", v, " exists")
            
    def clear(self):
        """ Remove all nodes and edges from the graph """
       
        self.node_set.clear()
        self.next.clear()
        self.num_node = 0
        self.edges = 0
        
    def subgraph_helper(self, node, visited):
        
        visited.add(node)
        
        for i in self.next[node]:
            if i not in visited:
                self.subgraph_helper(i, visited)
            
        
    def num_subgraph(self):
        
        """ return the number of disconnected components in the graph """
        
        visited = set()
        count = 0
        
        for node in self.node_set:
            
            if node not in visited:
                self.subgraph_helper(node, visited)
                count += 1
        
        return count
            
        
        
        
        
        