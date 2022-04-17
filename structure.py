class Structure:
    """Implements graph representation of sql dependencies."""
    def __init__(self):
        """Initialize empty graph and vertices."""
        self.graph = {}
        self.vertices = 0

    def add_vertex(self, v: int):
        """Add vertex to a graph."""
        if v in self.graph:
            print("Vertex ", v, " already exists.")
        else:
            self.vertices = self.vertices + 1
            self.graph[v] = []

    def add_edge(self, v1, v2):
        """Add edge to a graph."""
        if v1 not in self.graph:
            print("Vertex ", v1, " does not exist.")
        elif v2 not in self.graph:
            print("Vertex ", v2, " does not exist.")
        else:
            self.graph[v1].append(v2)
