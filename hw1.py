import numpy as np
import networkx as nx
import random
import pandas as pd

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

counter = 0

########

mask = ((df_instaglam0.userID == 145) | (df_instaglam0.userID == 31383) |
 (df_instaglam0.userID == 26577))
new_instaglam0 = df_instaglam0[mask]

mask2 = ((df_spotifly.userID == 145) | (df_spotifly.userID == 31383) |
 (df_spotifly.userID == 26577))
new_spotifly = df_spotifly[mask2]

new_G = nx.from_pandas_edgelist(new_instaglam0, "userID", "friendID")

nx.set_node_attributes(new_G, 0, name="bought")
nx.set_node_attributes(new_G, 0, name="probability")
nx.set_node_attributes(new_G, 0, name="Nt")
nx.set_node_attributes(new_G, 0, name="Bt")
nx.set_node_attributes(new_G, 0, name="h")

new_G.nodes[145]['bought'] = 1
new_G.nodes[31383]['bought'] = 1
new_G.nodes[26577]['bought'] = 1


########


# edges_1 = []
# for i in G_1.nodes:
#     edges_1.append(len(G_1.adj[i]))


# edges0 = []
# for i in G0.nodes:
#     edges0.append(len(G0.adj[i]))

# edges_1_np = np.array(edges_1)
# edges0_np = np.array(edges0)

# result = (edges0_np - edges_1_np)
# print(result)




def prob_for_edge(G, node1, node2):
    node1_num_neighboors = G.degree[node1]
    node2_num_neighboors = G.degree[node2]
    common_neighboors = len(list(nx.common_neighbors(G, node1, node2)))
    if common_neighboors <= 1:
        return 0
    p = common_neighboors / (node1_num_neighboors + node2_num_neighboors)
    return p



def updated_graph(G):
    random_number = random.random()
    graph_nodes_list = list(G.nodes)
    graph_nodes_np_list = np.array(graph_nodes_list)
    unique_graph_nodes_np_list = np.unique(graph_nodes_np_list)
    n = len(unique_graph_nodes_np_list)
    for i in range(n):
        if i % 100 == 0:
            print(i)
        for j in range(i + 1, n):
            p = prob_for_edge(G, unique_graph_nodes_np_list[i], unique_graph_nodes_np_list[j])
            if random_number <= p:
                G.add_edge(unique_graph_nodes_np_list[i], unique_graph_nodes_np_list[j])



def h_update(G, artist):
    for node in G.nodes:
        plays_as_np_array = ((df_spotifly[(df_spotifly.userID == node) &
                                          (df_spotifly[' artistID'] == artist)]['#plays'])).to_numpy()
        if plays_as_np_array.size == 0:
            G.nodes[node]['h'] = 0
        else:
            G.nodes[node]['h'] = plays_as_np_array[0]


def parameters_update(G):
    for node in G.nodes:
        if G.nodes[node]['bought'] == 1:
            continue
        G.nodes[node]['Nt'] = len(G[node])
        for neighboor in G.adj[node]:
            if G.nodes[neighboor]['bought'] == 1:
                G.nodes[node]['Bt'] += 1
        if G.nodes[node]['h'] == 0:
            G.nodes[node]['probability'] = G.nodes[node]['Bt'] / G.nodes[node]['Nt']

        else:
            G.nodes[node]['probability'] = (G.nodes[node]['Bt'] * G.nodes[node]['h'])\
                                           / (1000 * G.nodes[node]['Nt'])


def buying_probability(G):
    global counter
    random_number = random.random()
    for node in G.nodes:
        if G.nodes[node]["bought"] == 1:
            continue
        x = G.nodes[node]['probability']
        if random_number <= x:
            G.nodes[node]['bought'] = 1
            counter += 1


def simulation(G):
    global counter
    for i in range(1, 7):
        updated_graph(G)
        parameters_update(G)
        buying_probability(G)
    return counter



def main():
    artists = [989, 16326, 144882, 194647]
    print(len(G0.nodes))
    for i in range(4):
        h_update(G0, artists[i])
        print(simulation(G0))
        break


if __name__ == '__main__':
    main()


# mask = df_spotifly.userID == 145
# mask2 = df_spotifly.artistID == 20317
# print((df_spotifly[mask][mask2]['#plays'])[0])


