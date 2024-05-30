import matplotlib.pyplot as plt
import networkx as nx

# Create a directed graph
G = nx.DiGraph()

# Add nodes
G.add_node('C')
G.add_node('D1')
G.add_node('D2')
G.add_node('D3')
G.add_node('a1')
G.add_node('a2')
G.add_node('a3')

# Add edges

G.add_edge('C', 'D1')
G.add_edge('C', 'D2')
G.add_edge('C', 'D3')
G.add_edge('a1', 'D1')
#G.add_edge('D1', 'a2')
G.add_edge('a2', 'D2')
#G.add_edge('D2', 'a3')
G.add_edge('a3', 'D3')

# Draw the graph

pos = {'C': (1, 0), 'D1': (0, -1), 'D2': (1, -1), 'D3': (2, -1), 'a1': (0, -2), 'a2': (1, -2), 'a3': (2, -2)}
'''
G.add_edge('C', 'D1')
G.add_edge('D1', 'D2')
G.add_edge('D2', 'D3')
G.add_edge('a1', 'D1')
G.add_edge('a2', 'D2')
G.add_edge('a3', 'D3')
pos = {'C': (0, -1), 'D1': (1, -1), 'D2': (2, -1), 'D3': (3, -1), 'a1': (1, 0), 'a2': (2, 0), 'a3': (3, 0)}
'''
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1500, arrows=True)

# Show the plot
plt.show()