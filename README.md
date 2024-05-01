# Elliptic2

This repository is the official guide of using the Elliptic2 dataset introduced by the paper [The Shape of Money Laundering: Subgraph Representation Learning on the Blockchain with the Elliptic2 Dataset](https://arxiv.org/abs/2404.19109).

#### Requirements
To install the required python packages to run this repo, first create a python environment `elliptic` using the commend below

```
conda create --name elliptic --file requirements.txt
```

and then install [PyTorch](https://pytorch.org/get-started/previous-versions/) and [PyTorch_Geometric](https://pytorch-geometric.readthedocs.io/en/latest/notes/installation.html) based on the specific GPU setup of your own system, following the official guides. Also install the additional libraries torch_scatter, torch_sparse, torch_cluster, and torch_spline_conv while installing pytorch geometric.


#### Download Data

Download the Elliptic2 dataset [here](http://elliptic.co/elliptic2). Please download, unzip, and put them in a folder `dataset`. The downloaded files should include

```
dataset
├── background_edges.csv
├── background_nodes.csv
├── connected_components.csv
├── edges.csv
└── nodes.csv
```

#### Clone Repository

To run the three models in the paper on Elliptic2, clone the [GLASS](https://github.com/Xi-yuanWang/GLASS/tree/main) repository for GLASS and GNNSeg. For Sub2vec, we provide a version adapted from the original [Sub2Vec](https://github.com/bijayaVT/sub2vec/tree/master) respository. The overall folder structure should look like

```
CODE
├── dataset
├── GLASS
└── sub2vec
```

### Preprocess Data

Now, you need to preprocess Elliptic2 to obtain the specific input format for each model.

#### GLASS and GNNSeg

To preprocess for GLASS and GNNSeg, edit `DATAPATH` in `preprocess_glass.py` and run
```
python preprocess_glass.py
```
which will produce three files: `edge_list.txt`, `subgraph.pth`, `n2id.pkl`. 

The first two files are the required inputs for GLASS, which should be move into `GLASS/dataset/elliptic`. The file `n2id.pkl` will store a dictionary that converts node id in Ellptic2 to node id in GLASS for reference. Note that the train/val split is fixed given the random seeds, but you can change the split size at the top of the python script.


#### Sub2vec

To preprocess for Sub2Vec, edit `DATAPATH` in `preprocess_sub2vec.py` and run
```
python preprocess_sub2vec.py
```
which will produce a directory `sub2vec/sub2vec_input` that contains all the subgraphs for input to Sub2Vec, and a file `label.pkl` which contains the subgraph labels as a dictionary.

### Run Experiments

#### GLASS
To run GLASS, you need to provide a config file for Elliptic2. An example is `elliptic.yml`, which should be moved to `GLASS/config/`. Then, follow the original instructions of GLASS and run

```
cd GLASS
python GLASSTest.py --use_deg --use_maxzeroone --repeat 1 --device $gpu_id --dataset elliptic
```

#### GNNSeg
To run GNNSeg, you need to add the configuration directly under the `best_hyperparams` dictionary at the bottom of `GLASS/GNNSeg.py`. An example configuration is 

```python 
'elliptic': {
        'conv_layer': 2,
        'dropout': 0.2,
        'hidden_dim': 256
}
```

Then, run 
```
cd GLASS
python GNNSeg.py --repeat 1 --device $gpu_id --dataset elliptic
```

#### Sub2vec
Follow the original instructions of Sub2Vec and run 
```
cd sub2vec
python src/main.py --input sub2vec_input  --output $output_file --property n
```
which will produce the subgraph embeddings in `$output_file`, which can be used with `label.pkl` to run any futhur downstream model (i.e. a simple FeedForward model). This command may take a long time to run.


### Cite Elliptic2

```{bibtex}
@MISC{random.walk,
  AUTHOR = {Claudio Bellei and Muhua Xu and Ross Phillips and Tom Robinson and Mark Weber and Tim Kaler and Charles E. Leiserson and Arvind and Jie Chen},
  TITLE = {The Shape of Money Laundering: Subgraph Representation Learning on the Blockchain with the {Elliptic2} Dataset},
  HOWPUBLISHED = {Preprint arXiv:2404.19109},
  YEAR = {2024},
}
```

