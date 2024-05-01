import pandas as pd
import torch
import pickle
import numpy as np
import os 

#Parameters
DATAPATH = "./dataset/"

#Read in Node ID
n2id = {}
with open('n2id.pkl', 'rb') as handle:
    n2id = pickle.load(handle)

#Read in Subgraph ID
cc2id = {}
cc = pd.read_csv(DATAPATH+"/connected_components.csv")
for row in cc.itertuples(index=True):
    cc2id[int(row[1])] =int(row[0])

#Read in Nodes in Subgraph
sub = {}
node = pd.read_csv(DATAPATH+"/nodes.csv")
for row in node.itertuples(index=False):
    if cc2id[int(row[1])] in sub.keys():
        sub[cc2id[int(row[1])]].append(n2id[int(row[0])])
    else:
        sub[cc2id[int(row[1])]] = [n2id[int(row[0])]]

#Read in edge list (undirected as reference to paper)    
adj = {}
file = open("./edge_list.txt","r")
Lines = file.readlines()
print(len(Lines))
for line in Lines:
    c1,c2 = line.split(" ")
    c1 = int(c1)
    c2 = int(c2)
    if c1 < c2:
        if c1 in adj.keys():
            adj[c1].append(c2)
        else:
            adj[c1] = [c2]
    else:
        if c2 in adj.keys():
            adj[c2].append(c1)
        else:
            adj[c2] = [c1]

#Generate Subgraph Files
count = 0
isolate = 0
# y = np.zeros(shape = (1,1))
label = {}
if not os.path.exists("./sub2vec/sub2vec_input"):
    os.mkdir("./sub2vec/sub2vec_input")
for c in sub.keys():
    file = open("./sub2vec/sub2vec_input/subGraph"+str(c),"w")
    for i in range(len(sub[c])):
        seen = False
        for j in range(i,len(sub[c])):
            if sub[c][i] in adj.keys() and sub[c][j] in adj[sub[c][i]]:
                file.write(str(sub[c][i])+"\t"+str(sub[c][j])+"\n")
                seen = True
            elif sub[c][j] in adj.keys() and sub[c][i] in adj[sub[c][j]]:
                file.write(str(sub[c][j])+"\t"+str(sub[c][i])+"\n")
                seen = True
        if not seen:
            #print("Spotted isolated node in subgraph",c,sub[c],sub[c][i])
            file.write(str(sub[c][i])+"\t"+str(sub[c][i])+"\n")
            isolate+=1
    label[c] =  cc.loc[c,"ccLabel"]
    count+=1
    # if label == "licit":
    #     y = np.vstack([y,[0]])
    # else:
    #     y = np.vstack([y,[1]])
    file.close()

with open('label.pkl', 'wb') as fp:
    pickle.dump(label, fp)
#torch.save(torch.from_numpy(y),"label.pt")
print("Generated "+str(count)+" subgraphs in which "+str(isolate)+" are isolated")
    
