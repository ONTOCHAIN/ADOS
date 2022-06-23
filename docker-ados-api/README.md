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

**ADOS Transaction submission**
----
  This API endpoint is intended to submit data for processing via ADOS models in iExec. It will return a set of values corresponding to the probability of attacks for the set of measurements by the IoT network in each particular timestamp.

* **URL**

  /

* **Method:**
  
  `POST
  
*  **URL Params**

   No URL params are expected in this endpoint

* **Data Params**

   The body must include the following dictionary with the following three fields:
   - **weightsFile**: URL pointing to the pt file holding the training model weights (e.g. URL in S3)
   - **data_in**: URL pointing to a CSV-type file holding the IoT network data structured in timestamps to be processed by iExec
   - **list_in**: URL pointing to a txt file holding additional settings configuration for the process

   {
       "weightsFile": "<URL>",
       "data_in": "<URL>",
       "list_in": "<URL>"
   }

   NOTE: in each of the scenarios folders located in this repo you can find the metadata files you can use for testing the API.

* **Success Response:**
  
  A new transaction process is generated, returning a dictionary with:
  - **transaction_id**: unique alphanumeric value used to identify the transaction in ADOS
  - **status**: current status of the ongoing transaction
    1. INITIATING: transaction initiating
    2. UNSET: transaction initiated, tasks still not set up with the workerpool
    3. ACTIVE: tasks assigned to workerpool, now processing data in iExec model
    4. REVEALING: data processed, now finishing transaction
    5. COMPLETE: data processed, transaction over, waiting for receiving response
    6. DELIVERED: response received, now showing
  - **task_id**: associated task_id in iExec

  Now we show next the respone code and an example:
  * **Code:** 201 <br />
    **Content:** `{
    "source": "0DL2ucrkE2QeYJhi",
    "status": "INITIATING",
    "task_id": "unassigned"
    }`
 
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ error : "Log in" }`

* **Sample Call:**

   ```
   curl --location --request POST 'ados.airtrace.io:5000' \
   --header 'Content-Type: application/json' \
   --data-raw '{
    "weightsFile": "https://airchain.s3.eu-west-1.amazonaws.com/ados/inferences/best_mls.pt",
    "data_in": "https://airchain.s3.eu-west-1.amazonaws.com/ados/inferences/data_in.csv",
    "list_in": "https://airchain.s3.eu-west-1.amazonaws.com/ados/inferences/list.txt"```

* **Notes:**

  Please, refer to the scenarios folder to check examples on trained models by ADOS short project in ONTOCHAIN's OC2.
