# Ensure all packages have been installed
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import scipy


# change this to the .csv output file from sourmash (NOT the numpy binary matrix)
SMASH_CSV = "<sourmash_output.csv"


# Convert sourmash output to usable format
df = pd.read_csv(SMASH_CSV)
df.columns = range(len(df.columns))

new_data = []
for col_idx, col in df.iteritems():
    for idx, val in col.iteritems():
        if idx <= col_idx:
            new_data.append({"Genome1": col_idx, "Genome2": idx, "Value": val})

new_df = pd.DataFrame(new_data)
for_final_df = new_df.copy()

SMASH_DICT_CSV = pd.read_csv(SMASH_CSV)
genome_IDs = list(SMASH_DICT_CSV.columns)
genome_IDs_dict = {idx: val for idx, val in enumerate(genome_IDs)}

for_final_df["Genome1"] = for_final_df["Genome1"].map(genome_IDs_dict)
for_final_df["Genome2"] = for_final_df["Genome2"].map(genome_IDs_dict)

for_final_df.to_csv("processed_sourmash.csv", index=False, header=True)
network_df = pd.read_csv("processed_sourmash.csv")

#
#
# EDIT FOLLOWING CODE BLOCKS TO EDIT NETWORK GRAPH
#
#

# Creating base graph
G1 = nx.Graph()
G1 = nx.from_pandas_edgelist(network_df, 'Genome1', 'Genome2', edge_attr='Value')

# Removes edges of a certain value (essential for clique formation)
G2 = nx.Graph()
G2 = nx.Graph(G1)
edges_to_remove = [(u, v, d) for u, v, d in G2.edges(data=True) if d['Value']<#ADD_EDGE_VALUE_HERE]
G2.remove_edges_from(edges_to_remove)

# Change graph to spring layout (nicer spread of nodes)
# Nodes are treated as a 'repelling force' and edges treated as 'springs' pulling nodes together
G3 = nx.Graph()
G3 = nx.Graph(G2)
pos = nx.spring_layout(G3, k=1)

# Removes self-loops (reccomended for large datasets)
G4 = nx.Graph()
G4 = nx.Graph(G3)
G4_selfloops = [(u,v) for u, v in G4.edges() if u == v]
G4.remove_edges_from(G4_selfloops)

# Plotting the graph
# Leave out pos argument for normal graph layout
# Will need to edit node/edge size for large datasets to prevent overlapping
nx.draw(G4, pos, with_labels=True, ndoe_size=5, width=0.005)
plt.savefig("network_graph_sourmash.pdf", format="pdf")


#
#
# This code will find the top 5 largest cliques in your network
#
#

cliques = list(nx.find_cliques(G4))
cliques.sort(key=len, reverse=True)
clique_1 = cliques[0]
clique_2 = cliques[1]
clique_3 = cliques[2]
clique_4 = cliques[3]
clique_5 = cliques[4]

while len(clique_2) < len(clique_1):
	clique_2.append('NA')

while len(clique_3) < len(clique_1):
    clique_3.append('NA')

while len(clique_4) < len(clique_1):
    clique_4.append('NA')

while len(clique_5) < len(clique_1):
    clique_5.append('NA')

top5_cliques = pd.DataFrame(
    {'clique_1': clique_1,
    'clique_2': clique_2,
    'clique_3': clique_3,
    'clique_4': clique_4,
    'clique_5': clique_5}
)

top5_cliques.to_csv('top5cliques_sourmash.csv', index=False)