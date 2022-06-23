# DOCKER-based image API client for ADOS

Docker image source code implementing API for ADOS: AirTrace Decentralized Oracle System an advanced AI-based oracle system for securing off-chain IoT data integrity when injecting in the blockchain

# Usage
We consider deployment of the API in a virtual machine hosted in the clode (e.g. AWS EC2). Please, note that ports shall be open for proper functionality of the service.

# Build and run

```
docker image build -t ados_docker .
docker run -p 5000:5000 -e WALLET_PASS=<password> -v </route/to/local/keystore>:/root/.ethereum/keystore -v </route/to/iexec/configuration/files>:/app/iexec_conf -d ados_docker
```
Please, note the following (these parameters have to be introduced by the user):
- **password** refers to the password used for your wallet in iExec
- **/route/to/local/keystore** refers to the route that holds your wallet data (more information at https://docs.iex.ec/for-developers/quick-start-for-developers)
- **/route/to/iexec/configuration/files** refers to the directory that holds the app data to be executed in iExec (e.g. chain.json, deployment.json, iexec.json). More information at https://docs.iex.ec/for-developers/quick-start-for-developers

# API endpoints


