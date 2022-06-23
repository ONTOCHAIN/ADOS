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
  
  POST
  
*  **URL Params**

   No URL params are expected in this endpoint

* **Data Params**

   The body must include the following dictionary with the following three fields:
   - **weightsFile**: URL pointing to the pt file holding the training model weights (e.g. URL in S3)
   - **data_in**: URL pointing to a CSV-type file holding the IoT network data structured in timestamps to be processed by iExec
   - **list_in**: URL pointing to a txt file holding additional settings configuration for the process

   ```
   {
       "weightsFile": "<URL>",
       "data_in": "<URL>",
       "list_in": "<URL>"
   }
   ```

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

**ADOS Transaction status check**
----
  This API endpoint is used to check the current status of a transaction generated via [POST] / endpoint (check above)

* **URL**

  /transactions/<id_transaction>

* **Method:**
  
  GET
  
*  **URL Params**

   - **id_transaction**: alphanumeric string that was returned by [POST] / endpoint when submitting the transaction

* **Data Params**

   No data params are necessary

* **Success Response:**
  
  The current status of the transaction, returning a dictionary with:
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
  * **Code:** 200 <br />
    **Content:** `{
    "source": "0DL2ucrkE2QeYJhi",
    "status": "REVEALING",
    "task_id": "0xd0987b0654160f0c1d47e5d5f1518893023373146fe5a978bd1ac300cc05f20d"
    }`
 
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ error : "Log in" }`

* **Sample Call:**

   ```
   curl --location --request GET 'ados.airtrace.io:5000/transactions/tlogjQqZDyenJvcm' \
   --data-raw ''```

* **Notes:**

  Please, refer to the scenarios folder to check examples on trained models by ADOS short project in ONTOCHAIN's OC2.

**ADOS all transactions so far**
----
  This API endpoint is intended to retrieve all transactions made so far

* **URL**

  /transactions

* **Method:**
  
  GET
  
*  **URL Params**

   No URL params are expected in this endpoint

* **Data Params**

   No data params are necessary

* **Success Response:**

  Now we show next the respone code and an example:
  * **Code:** 200 <br />
    **Content:** `[
    {
        "last_update": "2022-06-23 13:58:43.033961",
        "task_id": "0xb69ccba1f59e81452543024b14d94fdd4f6d44be687a374d8652b68ee41db89c",
        "transaction_id": "FYaE6UTOLr8Y2mpB"
    },
    {
        "last_update": "2022-06-23 14:34:11.938198",
        "task_id": "0xd0987b0654160f0c1d47e5d5f1518893023373146fe5a978bd1ac300cc05f20d",
        "transaction_id": "tlogjQqZDyenJvcm"
    },
    {
        "last_update": "2022-06-23 13:50:11.148763",
        "task_id": "0x7487e2fe4981c24fc303b0175825964fa1e390832e374829c8530c0be75df02b",
        "transaction_id": "uXBAjIgyvhdFIerI"
    },
    {
        "last_update": "2022-06-23 14:07:48.386991",
        "task_id": "0x70378c85f2deac2fb00989f7bb15b32ff0509623377c78b9ce9ac80cc14a1c24",
        "transaction_id": "qyk5D0vMwzNPgGVs"
    },
    {
        "last_update": "2022-06-23 14:16:44.351961",
        "task_id": "0xbd24f968e903e0bb3a84e33e9b563c100f77dade8c4b9de8fe3d45ae3d3ff5f7",
        "transaction_id": "iTbcfG8whDIdz2aD"
    }
]`
 
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ error : "Log in" }`

* **Sample Call:**

   ```
   curl --location --request GET 'ados.airtrace.io:5000/transactions' \
   --data-raw ''```

* **Notes:**

  Please, refer to the scenarios folder to check examples on trained models by ADOS short project in ONTOCHAIN's OC2.

**ADOS marketplace retrieval**
----
  (Still at an alpha state) This API endpoint is intended to be used to retrieve all models currently available in current instance along with the ontologies defining their intricacies

* **URL**

  /marketplace

* **Method:**
  
  GET
  
*  **URL Params**

   No URL params are expected in this endpoint

* **Data Params**

   No data params are necessary

* **Success Response:**
  
  Now we show next the respone code and an example:
  * **Code:** 200 <br />
    **Content:** `[
    {
        "model_name": "scenario1",
        "ontology": ":ados-0 a aom:configuration;aom : model : ados-gnn ;aom : modelVersion : 0.1 ;aom : location : ipfs://bafybeiemxf5abjwjbikoz4mc3a3dla6ual3jsgpdr4cjr3oz3evfyavhwq/aom : idNodes [M-6,M-1,M-2,S-2,P-10,T-4,T-5,F-7,M-3,M-4,M-5,P-15,C-1,C-2,T-12,T-13,F-4,F-5,D-14,T-9,P-14,T-8,P-11,D-15,D-16,M-7,F-8] .aom : iExecMaxNumWorkers : 10 ."
    },
    {
        "model_name": "scenario2",
        "ontology": ":ados-0 a aom:configuration;aom : model : ados-gnn ;aom : modelVersion : 0.1 ;aom : location : ipfs://bafybeiemxf5abjwjbikoz4mc3a3dla6ual3jsgpdr4cjr3oz3evfyavhwq/aom : idNodes [M-6,M-1,M-2,S-2,P-10,T-4,T-5,F-7,M-3,M-4,M-5,P-15,C-1,C-2,T-12,T-13,F-4,F-5,D-14,T-9,P-14,T-8,P-11,D-15,D-16,M-7,F-8] .aom : iExecMaxNumWorkers : 10 ."
    },
    {
        "model_name": "scenario3",
        "ontology": ":ados-0 a aom:configuration;aom : model : ados-gnn ;aom : modelVersion : 0.1 ;aom : location : ipfs://bafybeiemxf5abjwjbikoz4mc3a3dla6ual3jsgpdr4cjr3oz3evfyavhwq/aom : idNodes [M-6,M-1,M-2,S-2,P-10,T-4,T-5,F-7,M-3,M-4,M-5,P-15,C-1,C-2,T-12,T-13,F-4,F-5,D-14,T-9,P-14,T-8,P-11,D-15,D-16,M-7,F-8] .aom : iExecMaxNumWorkers : 10 ."
    }
]`
 
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ error : "Log in" }`

* **Sample Call:**

   ```
   curl --location --request GET 'ados.airtrace.io:5000/marketplace' \
   --data-raw ''```

* **Notes:**

  Please, refer to the scenarios folder to check examples on trained models by ADOS short project in ONTOCHAIN's OC2.
