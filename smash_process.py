import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import scipy

# csv to read in and write to. Will be changed depending on smash output file
UNPROCESSED = "WEIRDNAME_1"
PROCESSED = "WEIRDNAME_2"

# read in csv as dataframe
df = pd.read_csv(UNPROCESSED)

# convert column headers to integers
df.columns = range(len(df.columns))

# create empty list to store new data
new_data = []

# iterate through each column and value
for col_idx, col in df.iteritems():
    for idx, val in col.iteritems():
        # only add the value if the index is less than or equal to the column header
        if idx <= col_idx:
            new_data.append({"Genome1": col_idx, "Genome2": idx, "Value": val})

# create a new dataframe from the new data
new_df = pd.DataFrame(new_data)
for_final_df = new_df.copy()

# make dictionary to change integers later
UNPROCESSED_DICT_CSV = pd.read_csv(UNPROCESSED)
genome_IDs = list(UNPROCESSED_DICT_CSV.columns)
genome_IDs_dict = {idx: val for idx, val in enumerate(genome_IDs)}

# replace the integers with genome_IDs
for_final_df["Genome1"] = for_final_df["Genome1"].map(genome_IDs_dict)
for_final_df["Genome2"] = for_final_df["Genome2"].map(genome_IDs_dict)

# convert the df to a csv
for_final_df.to_csv(PROCESSED, index=False, header=True)

# read in new csv to make network graph
network_df = pd.read_csv(PROCESSED)

# create first graph showing all connections
G1 = nx.Graph()
G1 = nx.from_pandas_edgelist(network_df, 'Genome1', 'Genome2', edge_attr='Value')
#nx.draw(G1, with_labels=True)
#plt.savefig("WEIRDNAME_3.pdf", format="pdf")

# create second graph without self-loops
#BEEPG2 = nx.Graph()
#BEEPG2 = nx.Graph(G1)
#BEEPG2_selfloops = [(u,v) for u, v in G2.edges() if u == v]
#BEEPG2.remove_edges_from(G2_selfloops)
#BEEPnx.draw(G2, with_labels=True)
#BEEPplt.savefig("noselfloops_WEIRDNAME_3.pdf", format="pdf")

# create third graph with edges of certain value removed
G3 = nx.Graph()
G3 = nx.Graph(LOOPED)
edges_to_remove = [(u, v, d) for u, v, d in G3.edges(data=True) if d['Value']<OMGEDGES]
G3.remove_edges_from(edges_to_remove)
#nx.draw(G3, with_labels=True)
#plt.savefig("edged_WEIRDNAME_3.pdf", format="pdf")

# create final graph of spring layout
G4 = nx.Graph()
G4 = nx.Graph(G3)
pos = nx.spring_layout(G4, k=1)
nx.draw(G4, pos, with_labels=True)
plt.savefig("network_WEIRDNAME_3.pdf", format="pdf")

# finding the largest clique
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

top5_cliques.to_csv('top5cliques_WEIRDNAME_3.csv', index=False)
