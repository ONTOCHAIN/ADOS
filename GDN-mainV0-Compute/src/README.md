# ADOS GDN IMPLEMENTATION FOR IEXEC




# Installation
### Requirements
* Python >= 3.6
* cuda == 10.2
* [Pytorch==1.5.1](https://pytorch.org/)
* [PyG: torch-geometric==1.5.0](https://pytorch-geometric.readthedocs.io/en/latest/notes/installation.html)

# Usage
We use part of msl dataset(refer to [telemanom](https://github.com/khundman/telemanom)) as demo example. 

## Data Preparation
```
# put your dataset under iexec_in/ directory with the same structure shown below

iexec_in
 |-list.txt    # the feature names, one feature per line
 |-data_in.csv   # dataset
 |-best_mls.pt    # trained model


### Notices:
* The first column in .csv will be regarded as index column. 
* The column sequence in .csv don't need to match the sequence in list.txt, we will rearrange the data columns according to the sequence in list.txt.

## Run
```
    # using gpu
    TODO

    # or using cpu
    TODO
```
TODO: You can change running parameters....

# Others DataSet and Scenarios
TODO
SWaT and WADI datasets can be requested from [iTrust](https://itrust.sutd.edu.sg/)


# Citation
Adaptation of the code implementation for : [Graph Neural Network-Based Anomaly Detection in Multivariate Time Series(AAAI'21)](https://arxiv.org/pdf/2106.06947.pdf)

If you find this repo or our work useful for your research, please consider citing the paper
```
@inproceedings{deng2021graph,
  title={Graph neural network-based anomaly detection in multivariate time series},
  author={Deng, Ailin and Hooi, Bryan},
  booktitle={Proceedings of the AAAI Conference on Artificial Intelligence},
  volume={35},
  number={5},
  pages={4027--4035},
  year={2021}
}
```