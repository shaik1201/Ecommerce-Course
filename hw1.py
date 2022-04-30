from itertools import count
import numpy as np
import networkx as nx
import random
import pandas as pd
import matplotlib.pyplot as plt


df_instaglam_1 = pd.read_csv("instaglam_1.csv")
df_instaglam0 = pd.read_csv("instaglam0.csv")
df_spotifly = pd.read_csv("spotifly.csv")

G_1 = nx.from_pandas_edgelist(df_instaglam_1, "userID", "friendID")
G0 = nx.from_pandas_edgelist(df_instaglam0, "userID", "friendID")
nx.set_node_attributes(G0, 0, name="bought")
nx.set_node_attributes(G0, 0, name="probability")
nx.set_node_attributes(G0, 0, name="Nt")
nx.set_node_attributes(G0, 0, name="Bt")
nx.set_node_attributes(G0, 0, name="h")


G0.nodes[145]['bought'] = 1
G0.nodes[31383]['bought'] = 1
G0.nodes[32813]['bought'] = 1
G0.nodes[84149]['bought'] = 1
G0.nodes[105294]['bought'] = 1


# edges_1 = []
# for i in G_1.nodes:
#     edges_1.append(len(G_1.adj[i]))


# edges0 = []
# for i in G0.nodes:
#     edges0.append(len(G0.adj[i]))

# edges_1_np = np.array(edges_1)
# edges0_np = np.array(edges0)

# result = (edges0_np - edges_1_np)
#print(result)



# print(df_spotifly)
# print(df_spotifly.loc[(df_spotifly['userID'] == "145") & (df_spotifly['artistID'] == artists[0])])



def prob_for_edge(G, node1, node2):
    node1_num_neighboors = G.degree[node1]
    node2_num_neighboors = G.degree[node2]
    common_neighboors = len(list(nx.common_neighbors(G, node1, node2)))
    if common_neighboors <= 1:
        return 0

    p = common_neighboors / (node1_num_neighboors + node2_num_neighboors)

    return p


def update_edge(G, node1, node2, p, random_number):
    
    if random_number <= p:
        G.add_edge(node1, node2)
    
    return G

def updated_graph(G):
    random_number = random.random()
    graph_nodes_list = list(G.nodes)
    graph_nodes_np_list = np.array(graph_nodes_list)
    unique_graph_nodes_np_list = np.unique(graph_nodes_np_list)
    n = len(unique_graph_nodes_np_list)

    for i in range(n):
        for j in range(i+1, n):
            p = prob_for_edge(G, unique_graph_nodes_np_list[i], unique_graph_nodes_np_list[j])
            G = update_edge(G, unique_graph_nodes_np_list[i], unique_graph_nodes_np_list[j],
            p, random_number)
    
    return G
            

def parameters_update(G, artist):
    for node in G.nodes:
        G.nodes[node]['Nt'] = len(G[node])
        for neighboor in G.adj[node]:
            if G.nodes[neighboor]['bought'] == 'yes':
                G.nodes[node]['Bt'] += 1

        mask = df_spotifly.userID == node
        mask2 = df_spotifly.artistID == artist
        G.nodes[node]['h'] = df_spotifly[mask][mask2]['#plays'][0]
        if G.nodes[node]['h'] == 0:
            G.nodes[node]['probability'] = G.nodes[node]['Bt'] / G.nodes[node]['Nt']
        else:
            G.nodes[node]['probability'] = (G.nodes[node]['Bt']
             * G.nodes[node]['h']) / (1000 * G.nodes[node]['Nt'])

def buying_probability(G, counter):
    random_number = random.random()
    for node in G.nodes:
        if random_number <= G.nodes[node]['probability']:
            G.nodes[node]['bought'] = 1
            counter += 1
    return counter

def simulation(artist, G):
    counter = 0
    for i in range(1,7):
        updated_G = updated_graph(G)
        parameters_update(G, artist)
        counter += buying_probability(updated_G, counter)
        
    return counter

def main():
    artists = [989, 16326, 144882, 194647]
    for i in range(4):
        print(simulation(artists[i], G0))
        break

if __name__ == '__main__':
    main()



lst = list(G_1.nodes)
np_list = np.array(lst)
unique_lst = np.unique(np_list)



# filt = df_spotifly['userID'] == 145 & df_spotifly[' artistID'] == 20317
# print(df_spotifly.loc[filt])

# print(df_spotifly[df_spotifly['userID'] == 145][' artistID']['#plays'])

mask = df_spotifly.userID == 145
mask2 = df_spotifly.artistID == 20317
# print((df_spotifly[mask][mask2]['#plays'])[0])
    

