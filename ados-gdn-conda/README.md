# ADOS GDN IMPLEMENTATION FOR IEXEC

Code implementation for ADOS: AirTrace Decentralized Oracle System an advanced AI-based oracle system for securing off-chain IoT data integrity when injecting in the blockchain

Second Non TEE version for Conda Environment in order to implement a TEE version.

# Usage
We use part of msl dataset for the first use case (Water quality scenario) 
(refer to [telemanom](https://github.com/khundman/telemanom)) as demo example. 

## Data Preparation

### put your dataset under iexec_in/ directory with the same structure shown below
```
iexec_in
 |-list.txt      # the feature names, one feature per line
 |-data_in.csv   # dataset
 |-best_mls.pt   # trained model
``` 
## Notices:

* The first column in .csv will be regarded as index column. 
* The column sequence in .csv don't need to match the sequence in list.txt, we will rearrange the data columns according to the sequence in list.txt.


# Build and run locally

## non tee
```
docker build . --tag ados-gdn-nontee:v2
docker run --rm -v /home/ados/iexec_out:/iexec_out -e IEXEC_OUT=/iexec_out -v /home/ados/iexec_in:/iexec_in -e IEXEC_IN=/iexec_in ados-gdn-nontee:v2
```

# Run on iExec

## non tee
Deploy your app on iExec
```
iexec app deploy --chain viviani
```
Verify the deployed app (name, multiaddr, checksum, owner)
```
iexec app show --chain viviani
```
Before requesting an execution make sure your account stake is charged with Viviani RLC
```
iexec account show --chain viviani
```
Run your application on iExec
```
iexec app run --watch --chain viviani
```
Once the run is completed copy the taskid from iexec app run output to download and check the result
```
iexec task show <taskid> --download my-app-result --chain viviani  \
    && unzip my-app-result.zip -d my-app-result
```

# Others DataSet and Scenarios in preparation
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
