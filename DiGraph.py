import Graph
import Function as ft
import copy

class DiGraph:
    
    def __init__(self):
        self.node_set = set()
        self.prefix = {}
        self.suffix = {}
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
        
        """ check if the node is already added in the graph. If not, add the node and declare dict for storing prefix/suffix and 
        weight """
        
        if node in self.node_set:
            return 
        
        self.num_node = self.num_node + 1
        self.node_set.add(node)
        self.prefix[node] = {}
        self.suffix[node] = {}
        
        
    def add_edge(self, u, v, weight, pre_start, pre_end, suff_start, suff_end):
        
        """ add the nodes into graph if it has not been done and record prefix and suffix of the nodes 
            directed edge: u -> v
            Multi-edge is not allowed
        """
        
        self.add_node(u)
        self.add_node(v)
        
        if u not in self.prefix[v] and v not in self.suffix[u]:
            self.edges = self.edges + 1
        
        if u not in self.prefix[v]:
            self.prefix[v][u] = [weight, pre_start, pre_end]
            
        if v not in self.suffix[u]:
            self.suffix[u][v] = [weight, suff_start, suff_end]
            
    def remove_node(self, node):
        
        """ remove node from the graph """
        
        try:
            num_of_edge = len(self.prefix[node]) + len(self.suffix[node])
            self.node_set.remove(node)
            
            # remove edge associated with the node
            for key in self.prefix[node]:
                
                self.suffix[key].pop(node)
                
            for key in self.suffix[node]:
                
                self.prefix[key].pop(node)
                
            self.prefix.pop(node)
            self.suffix.pop(node)
            
            self.num_node -= 1
            self.edges -= num_of_edge
            
        except:
            print("ERROR: No node found.")
            
            
    def remove_edge(self, u, v):
        
        """ remove edges between two nodes
            u is the prefix of v
        """
        
        try:
            del self.prefix[v][u]
            del self.suffix[u][v]
        except:
            print("ERROR: The edges not in graph")
            
    def get_weight(self, u, v):
        
        """ return the weight between two edges """
        
        if self.node_set:
            if u in self.node_set and v in self.node_set:
                if v in self.suffix[u]:
                    return self.suffix[u][v][0];
                else:
                    print("ERROR: There is no edge between the nodes.")
            else:
                print("ERROR: Either or both of the node does not exists in the graph.")
        else:
            print("ERROR: The graph is empty.")
            
            
    def get_num_edge(self, node, direction):
        
        """ return number of edge by prefix or suffix of the node """
        
        if direction == 'prefix':
            return len(self.prefix[node])

        elif direction == 'suffix':
            return len(self.suffix[node])        

        else:

            print("""
            Make sure you have key in the correct parameters.
            get_num_edge(node, direction)
            direction: 'prefix' OR 'suffix'
            """)          

            
            
    def next_(self, node):
        
        """ return the next node with directed edge node -> nextnode """
        
        try:
            return list(self.suffix[node].keys())[0]
        except:
            print("ERROR: There is no outdegree edge")
            
    
    def in_degree(self, node):
        
        """ return the number of directed edges towards the node """
        
        try:
            return len(self.prefix[node])
        
        except:
            print("ERROR: The node does not exist.")
        
            
    def num_of_subgraphs(self):
        
        """ return the number of subgraphs in the graph """
        
        G = self.to_undirected_graph()
        
        count = G.num_subgraph()
        
        print('The number of disconnected components in the graph is ', count)       
        
     
    
    def to_undirected_graph(self):
        
        """ Return the undirected copy of the graph """
        visited = set()     
        G = Graph.Graph()
        
        for node in self.node_set:
            
            if node not in visited:
                visited.add(node)
                for i in self.suffix[node]:
                    G.add_edge(node, i)
        
        return G
        
                  
    def copy(self):
        """ Return the deep copy of the graph """
        
        
        G = DiGraph()
        G.node_set = copy.deepcopy(self.node_set)
        G.prefix = copy.deepcopy(self.prefix)
        G.suffix = copy.deepcopy(self.suffix)
        G.num_node = copy.deepcopy(self.num_node)
        G.edges = copy.deepcopy(self.edges)
        
        return G
    
    def clear(self):
        """ Remove all nodes and edges from the graph """
       
        self.node_set.clear()
        self.prefix.clear()
        self.suffix.clear()
        self.num_node = 0
        self.edges = 0
        

    def find_min_weight(self, path, node):
        
        """ return the edge that has minimum weight from a series of node """
        
        min_edge = []
                
        # assign edge weight first pair of node as min_weight
        min_weight = self.get_weight(path[-1], node)
        min_edge.append(path[-1])
        min_edge.append(node)
        
        # start from last node in path
        index = -1 
        i = path[index]
        
        
        # while node in path not equal to the node passed in, find min_weight
        while i != node:
            
            weight = self.get_weight(path[index-1], path[index])
            
            if weight < min_weight:
                
                min_weight = weight
                min_edge.clear()
                min_edge.append(path[index-1])
                min_edge.append(path[index])
            
            index -= 1
            i = path[index]
            
       
        return min_edge  
    
    def is_cyclic_helper(self, node, visited, path):
        
        """ helper function to determine whether the graph has cycle """
        
        visited.add(node)
        path.append(node)
        
        for i in self.suffix[node]:
            if i not in visited:
                if self.is_cyclic_helper(i, visited, path) is True: 
                    return True
                
            elif i in path:
                return True
        
        path.remove(node)
        return False

    
    def is_cyclic(self):
        
        """ return whether the graph has cycle """
        
        visited = set()
        path = []
        
        for node in self.node_set:
            if node not in visited:
                if self.is_cyclic_helper(node, visited, path) is True:
                    return True                
        
        visited.clear()
        path.clear()
        return False
    
    def remove_cycle_helper(self, node, visited, path):
        
        """ helper function to find the edge with minimum weight within the cycle """
        
        visited.add(node)
        path.append(node)
        
        for i in self.suffix[node]:
            if i not in visited:
                min_edge = self.remove_cycle_helper(i, visited, path)
                if min_edge is not None:
                    if len(min_edge) == 2:
                        return min_edge
            # cycle detected
            elif i in path:
                # find min weight of edges from the cycle
                min_edge = self.find_min_weight(path, i)
                return min_edge
        

        path.remove(node)
                          
        
    def remove_cycle_recur(self):
        
        """ find cycle in graph (repeated read), choose the edge with min weight """
        
        visited = set()
        path = []
        
        for node in self.node_set:
            if node not in visited:
                min_edge = self.remove_cycle_helper(node, visited, path)
                visited.clear()
                path.clear()
                if min_edge is not None:
                    # if there is a cycle and the min weight is found
                    if len(min_edge) == 2:
                        return min_edge
        
        visited.clear()
        path.clear()
        return []
    
    def remove_cycle(self):
        
        """ remove cycle from the graph """
        if self.is_cyclic() is True:

            while self.is_cyclic():
                min_edge = self.remove_cycle_recur()
                self.remove_edge(min_edge[0], min_edge[1])

            print("All the cycles are removed from the graph.")
        else:
            print("The graph has no cycle.")                
            
    

    def topological_sort_helper(self, node, visited, sorted_node): 
        
        """ helper function to help recursively visit and add nodes to list """
        
        # add the current node as visited. 
        visited.add(node)

        # repeat for all suffixes of the node
        for i in self.suffix[node]: 
            if i not in visited: 
                self.topological_sort_helper(i, visited, sorted_node) 

        # push current node as the first value in list 
        sorted_node.insert(0,node) 
        return visited

    
    def topological_sort(self): 
        
        """ return the topological sorted nodes """
        
        visited = set()
        sorted_node = [] 

        # sort all the node in the graph
        for i in self.node_set: 
            if i not in visited: 
                visited = self.topological_sort_helper(i, visited, sorted_node) 
        
        visited.clear()
        return sorted_node
        
    
    def transitive_reduction_helper(self, node, visited, path):
        
        """ helper function to recursively visit and remove edges """

        visited.add(node)
        path.append(node)
                    
        for i in self.suffix[node].copy():             
            self.transitive_reduction_helper(i, visited, path)

        # determine if the prefix can be reduced
        for i in self.prefix[path[-1]].copy():
            # if j is in the path and not the previous node
            if i in path and i is not path[-2]:
                self.remove_edge(i, path[-1])                    
                    
        
        path.remove(node)
        return visited
    
    def transitive_reduction(self, sorted_node):
        
        """ perform transitive reduction on the graph """
        
        if self.is_cyclic() is False:
        
            visited = set()
            path = []

            for i in sorted_node:
                if i not in visited:
                    visited = self.transitive_reduction_helper(i, visited, path)
                    
            print("Transitive reduction is completed.")
            
        else:
            print("Transitive reduction can only be performed on directed acyclic graph.")
            
    def filter_graph(self, sorted_node, ploidy):
        
        """ return the graph that has been reduced to best overlap graph 
            proceed from removing the edge with the min weight
        """
        
        for node in sorted_node:
            
            # while number of prefix edge > ploidy level
            while len(self.prefix[node]) > ploidy:
                min_weight_node = min(self.prefix[node], key=self.prefix[node].get)
                self.remove_edge(min_weight_node, node)
            
            # while number of suffix edge > ploidy level
            while len(self.suffix[node]) > ploidy:
                min_weight_node = min(self.suffix[node], key=self.suffix[node].get)
                self.remove_edge(node, min_weight_node)
        
        print("Graph is reduced to best overlap graph.")
            
    def longest_path(self, sorted_node):
        
        """ return the path travel in the graph 
            { sequence: [weight, previous sequence] }
        """
                
        dist = {}
        
        # Initialise dict with weight ('0') and previous seq ('null')
        for node in sorted_node:                      
            
            dist[node] = [0, ""]            
        
        # Finding longest path
        for node in sorted_node:
                            
            for prefix in self.prefix[node]:                
                
                temp_weight = self.get_weight(prefix, node) + dist[prefix][0]
                # update each weight with greatest path
                if temp_weight > dist[node][0]:
                    dist[node][0] = temp_weight
                    dist[node][1] = prefix  
                    
         
        return dist
    


    def bubble_detection(self, sorted_node):
        
        """ return the smallest bubbles in the graph
        """
        
        source = sorted_node[0]
        bubble = {} # for storing result
        potential = {}  # for storing path of potential entrance

        # transverse topologically sorted node
        for i in sorted_node:
                        
            if len(self.prefix[i]) > 1:
                temp = next(iter(self.prefix[i]))

                # if the entrance is stored in potential entrance
                if len([k for k, v in potential.items() if temp in v]) > 0:
                    print([k for k, v in potential.items() if temp in v])
                    source = [k for k, v in potential.items() if temp in v][0]
                    del potential[source]

                # add source and target to dictionary  
                if source != i:
                    bubble[source] = i
                    source = i

            for j in self.suffix[i]:

                # if the previous node is a potential entrance
                if i in potential:
                    potential[i].append(j)

                # if it is the successor of the potential entrance
                temp = next(iter(self.prefix[j]))
                if len([k for k, v in potential.items() if temp in v]) > 0:
                    potential_entrance = [k for k, v in potential.items() if temp in v][0]
                    potential[potential_entrance].append(j)

                if len(self.suffix[source]) == 1:
                    source = j

                if j != source:
                    if len(self.suffix[j]) > 1 and len(self.suffix[source]) > 1:
                        potential[j] = []

        return bubble
    
    def superbubble_detection(self, sorted_node):
        
        """ return the superbubbles in graph """

        source = sorted_node[0]
        path = []
        bubble = {}

        # transverse topologically sorted node
        for i in sorted_node:                    
                
            count_prefix = 0
            # check if it is the exit of bubble
            for node in self.prefix[i]:
                if node in path:
                    count_prefix += 1

                     # if it the potential exit of the bubble
                    if count_prefix == 2:
                        # if it the last node
                        if len(self.suffix[i]) == 0:
                            bubble[source] = i
                            break
                        # if it is the real exit
                        for temp in self.suffix[i]:
                            if len(self.prefix[temp]) == 1:
                                # add source and target to dictionary            
                                bubble[source] = i
                                source = i
                                path.clear()
                                break

            for j in self.suffix[i]:
                if len(self.suffix[i]) == 1 and len(path) == 0:
                        source = j

                if j != source:
                    path.append(j)

        return bubble 
    
    def reduce_graph(self, longest_path, sorted_node):
        
        """ reduce the graph for next haplotype formation """
        
        bubble = self.bubble_detection(sorted_node)
        
        # for every bubble
        for i in bubble:
            
            # if the bubble in longest path
            if i in longest_path and bubble[i] in longest_path:
                entrance_position = longest_path.index(i)
                exit_position = longest_path.index(bubble[i])
                
                # remove the edges 
                pos = entrance_position                
                while pos < exit_position:
                    self.remove_edge(longest_path[pos], longest_path[pos+1])
                    pos += 1
        
        # if there are no bubble exists
        if not bubble:
            return False
        
        return True
        
        
        
    def haplotype(self, ploidy):
        
        """ return ploidy level of haplotype (if got)
            if not, return as many haplotype as possible
        """
    
        i = 0 # counter for ploidy
        final = [] #to store seq
        got_bubble = True
        
        while i < ploidy:
            
            frag = []
            longest_path = []

            sorted_node = self.topological_sort()
            # find greatest weight path
            path = self.longest_path(sorted_node)
            # last node in the graph
            curr_max = max(path, key=path.get)
            next_node = ''
            str_temp = ''

            # while it is not the source node
            while len(self.prefix[curr_max]) != 0:
                # prev max node
                prev = path[curr_max][1]

                # if current node longer than prev and next node
                if len(curr_max) >= len(prev) and len(curr_max) >= len(next_node):
                    str_temp = curr_max                             

                # if current node shorter than prev and next node                
                elif len(curr_max) < len(prev) and len(curr_max) < len(next_node):
                    start = self.suffix[prev][curr_max][2]
                    end = self.prefix[next_node][curr_max][1]
                    str_temp = curr_max[start:end]

                # if current node shorter than prev but longer than the next node   
                elif len(curr_max) < len(prev) and len(curr_max) >= len(next_node):
                    start = self.suffix[prev][curr_max][2]
                    str_temp = curr_max[start:]

                # if current node longer than prev but shorter than the next node                
                else:
                    end = self.prefix[next_node][curr_max][1]
                    str_temp = curr_max[:end]

                frag.insert(0, str_temp)
                longest_path.insert(0, curr_max)
                next_node = curr_max
                curr_max = prev


            # if this is the first node
            if len(self.prefix[curr_max]) == 0:

                # if current longer than next node
                if len(curr_max) > len(next_node):
                    frag.insert(0, curr_max)
                    next_node = curr_max

                else:                    
                    end = self.prefix[next_node][curr_max][1]
                    str_temp = curr_max[:end]
                    frag.insert(0, str_temp)
                    next_node = curr_max
                
                longest_path.insert(0, curr_max)                


            # combine all string
            seq = ''.join(frag)
            final.append(seq)
            
            got_bubble = self.reduce_graph(longest_path, sorted_node)
            if got_bubble is False:
                break
            i += 1
        
        
        return final
            
        
        
        
        
                
                
            

    
        
        

        
    
        