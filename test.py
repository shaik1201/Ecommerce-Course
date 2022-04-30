import matplotlib.pyplot as plt
import networkx as nx
from matplotlib import pylab
import numpy as np
import random
import pandas as pd


df_instaglam_1 = pd.read_csv("instaglam_1.csv")
df_instaglam0 = pd.read_csv("instaglam0.csv")
df_spotifly = pd.read_csv("spotifly.csv")

G_1 = nx.from_pandas_edgelist(df_instaglam_1, "userID", "friendID")
G0 = nx.from_pandas_edgelist(df_instaglam0, "userID", "friendID")

def save_graph(graph,file_name):
    #initialze Figure
    plt.figure(num=None, figsize=(200, 200), dpi=80)
    plt.axis('off')
    fig = plt.figure(1)
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph,pos)
    nx.draw_networkx_edges(graph,pos)
    nx.draw_networkx_labels(graph,pos)

    cut = 1.00
    xmax = cut * max(xx for xx, yy in pos.values())
    ymax = cut * max(yy for xx, yy in pos.values())
    plt.xlim(0, xmax)
    plt.ylim(0, ymax)

    plt.savefig(file_name,bbox_inches="tight")
    pylab.close()
    del fig

#Assuming that the graph g has nodes and edges entered
save_graph(G0,"my_graph_1.png")

#it can also be saved in .svg, .png. or .ps formats


