import numpy as np
import networkx as nx
import random
import pandas as pd

df_instaglam_1 = pd.read_csv("instaglam_1.csv")
df_instaglam0 = pd.read_csv("instaglam0.csv")
df_spotifly = pd.read_csv("spotifly.csv")

G_1 = nx.from_pandas_edgelist(df_instaglam_1, "userID", "friendID")
G0 = nx.from_pandas_edgelist(df_instaglam0, "userID", "friendID")

artists = [989, 16326, 144882, 194647]

nx.set_node_attributes(G0, "no", name="bought")
nx.set_node_attributes(G0, 0, name="probability")
nx.set_node_attributes(G0, 0, name="Nt")
nx.set_node_attributes(G0, 0, name="Bt")
nx.set_node_attributes(G0, 0, name="h1")
nx.set_node_attributes(G0, 0, name="h2")
nx.set_node_attributes(G0, 0, name="h3")
nx.set_node_attributes(G0, 0, name="h4")


# print(G.nodes[145]["bought"])
# print(G.nodes[145]["probability"])

edges_1 = []
for i in G_1.nodes:
    edges_1.append(len(G_1.adj[i]))


edges0 = []
for i in G0.nodes:
    edges0.append(len(G0.adj[i]))

edges_1_np = np.array(edges_1)
edges0_np = np.array(edges0)

result = (sum(edges0_np - edges_1_np))/2
p_new_edge = result/12717       #TODO: We need to find another p

G0.nodes[145]['bought'] = 'yes'
G0.nodes[31383]['bought'] = 'yes'
G0.nodes[32813]['bought'] = 'yes'
G0.nodes[84149]['bought'] = 'yes'
G0.nodes[105294]['bought'] = 'yes'

G0.nodes[117383]['bought'] = 'yes'
G0.nodes[160817]['bought'] = 'yes'
G0.nodes[175764]['bought'] = 'yes'
G0.nodes[338687]['bought'] = 'yes'
G0.nodes[351902]['bought'] = 'yes'

G0.nodes[418840]['bought'] = 'yes'
G0.nodes[466173]['bought'] = 'yes'
G0.nodes[563940]['bought'] = 'yes'
G0.nodes[572310]['bought'] = 'yes'
G0.nodes[607020]['bought'] = 'yes'

G0.nodes[613750]['bought'] = 'yes'
G0.nodes[617317]['bought'] = 'yes'
G0.nodes[620114]['bought'] = 'yes'
G0.nodes[628474]['bought'] = 'yes'
G0.nodes[748485]['bought'] = 'yes'

print(df_spotifly)
print(df_spotifly.loc[(df_spotifly['userID'] == "145") & (df_spotifly['artistID'] == artists[0])])

# for i in range(6):
#     for node in G0.nodes:
#         G0.nodes[node]['Nt'] = len(G0[node])
#         for neighboor in G0.adj[node]:
#             if G0.nodes[neighboor]['bought'] == 'yes':
#                 G0.nodes[node]['Bt'] += 1
#         G0.nodes[node]['h'] = df_spotifly[2][node]
#     break