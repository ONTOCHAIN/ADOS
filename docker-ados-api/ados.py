#!/usr/bin/python
import subprocess
from flask import Flask, request, jsonify
import json
import sys
import time
import random, string
import threading
from pathlib import Path
import os
import datetime as dt

app = Flask(__name__)

def generateUniqueAlphaNumeric():

    x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
    return x

def call_iexec(weightsFile, data_in, list_in, outputFile, alphanumeric):
    input_buffer = sys.stdin
    output_buffer = sys.stdout
    os.chdir('/app/iexec_conf')
    command = 'iexec app run --watch --chain viviani --input-files ' + weightsFile + ',' + data_in + ',' + list_in + ' --skip-request-check --params {\"iexec_developer_logger\":true}'
    arrayProc = command.split()

    password = os.environ['WALLET_PASS']
    print("Wallet password: ", password)

    with open(outputFile, "w") as output:
        proc = subprocess.Popen(arrayProc, stdin=subprocess.PIPE, stdout=output, stderr=output, universal_newlines=True)#output_buffer'''

        time.sleep(5)
        print(password, file=proc.stdin, flush=True) #proc.stdin

        time.sleep(5)
        print("Y", file=proc.stdin, flush=True) #proc.stdin
        time.sleep(1)

        found = False
        while not found:
            with open(outputFile, 'r') as file:
                readFile = file.read()

                if "successful" in readFile:
                    print("Transaction Successful")
                    # Now we need to unzip
                    char1 = '('
                    char2 = ')'
                    completeString = readFile.split("successful",1)[1]
                    task_id = completeString[completeString.find(char1) + 1: completeString.find(char2)]
                    print(task_id)

                    command2 = 'iexec task show ' + task_id + ' --download ' + alphanumeric + ' --chain viviani'

                    print(command2)
                    arrayProc2 = command2.split()
                    proc2 = subprocess.Popen(arrayProc2, stdin=subprocess.PIPE, stdout=output, stderr=output,
                                            universal_newlines=True)

                    time.sleep(5)
                    print(password, file=proc2.stdin, flush=True)  # proc.stdin
                    found = True
                    time.sleep(5)

                    notFound = True
                    while notFound:
                        path = Path('/app/iexec_conf/' + alphanumeric + '.zip')
                        if path.is_file():
                            notFound = False
                            print('File ready!')
                            command3 = 'unzip ' + alphanumeric + '.zip -d ' + alphanumeric
                            arrayProc3 = command3.split()
                            proc3 = subprocess.Popen(arrayProc3, stdin=subprocess.PIPE, stdout=output, stderr=output,
                                                    universal_newlines=True)

                            time.sleep(3)
                            command4 = 'mv /app/iexec_conf/' + alphanumeric + ' /app/computations/' + alphanumeric
                            arrayProc4 = command4.split()
                            proc4 = subprocess.Popen(arrayProc4, stdin=subprocess.PIPE, stdout=output, stderr=output,
                                                    universal_newlines=True)
                        
                            command5 = 'rm -rf /app/iexec_conf/' + alphanumeric + '.zip'
                            arrayProc5 = command5.split()
                            proc5 = subprocess.Popen(arrayProc5, stdin=subprocess.PIPE, stdout=output, stderr=output)

                        else:
                            time.sleep(5)
                            print('Waiting...')

                    print("Unzipped")
                    break
                time.sleep(5)

@app.route("/", methods=['POST'])
def ados():

    data_json = request.get_json()
    if not data_json.keys() >= {"weightsFile", "data_in", "list_in"}:
        return jsonify({'message': 'Bad request'}), 400
    weightsFile = data_json['weightsFile']
    data_in = data_json['data_in']
    list_in = data_json['list_in']

    extension = generateUniqueAlphaNumeric()
    logfile_name = "/app/logs/" + extension
    thread = threading.Thread(target=call_iexec, args=(weightsFile, data_in, list_in, logfile_name, extension))

    thread.start()

    #return json.dumps({'source': extension, 'task_id': 'unassigned', 'status': 'INITIATING'}), 201
    return jsonify({'source': extension, 'task_id': 'unassigned', 'status': 'INITIATING'}), 201

@app.route("/transactions")
def adostransactions():
    
    dictReturn = []

    for roota, dirsa, filesa in os.walk('/app/logs'):
        for file in filesa:
            outputFile = "/app/logs/" + file
            with open(outputFile, 'r') as file_read:
                readFile = file_read.read()
                char1 = '('
                char2 = ')'
                st = os.stat(outputFile)
                mtime = dt.datetime.fromtimestamp(st.st_mtime)
                try:
                    completeString = readFile.split("tasks running", 1)[1]
                    task_id = completeString[completeString.find(char1) + 1: completeString.find(char2)]
                except:
                    task_id = "unassigned"

                dictReturn.append({"transaction_id":file, "last_update":str(mtime), "task_id": task_id})
    
    #return json.dumps(dictReturn), 200
    return jsonify(dictReturn), 200

@app.route("/marketplace")
def marketplace():

    dictModels = [{"model_name":"scenario1", "ontology": ":ados-0 a aom:configuration;aom : model : ados-gnn ;aom : modelVersion : 0.1 ;aom : location : ipfs://bafybeiemxf5abjwjbikoz4mc3a3dla6ual3jsgpdr4cjr3oz3evfyavhwq/aom : idNodes [M-6,M-1,M-2,S-2,P-10,T-4,T-5,F-7,M-3,M-4,M-5,P-15,C-1,C-2,T-12,T-13,F-4,F-5,D-14,T-9,P-14,T-8,P-11,D-15,D-16,M-7,F-8] .aom : iExecMaxNumWorkers : 10 ."},
    {"model_name":"scenario2", "ontology": ":ados-0 a aom:configuration;aom : model : ados-gnn ;aom : modelVersion : 0.1 ;aom : location : ipfs://bafybeiemxf5abjwjbikoz4mc3a3dla6ual3jsgpdr4cjr3oz3evfyavhwq/aom : idNodes [M-6,M-1,M-2,S-2,P-10,T-4,T-5,F-7,M-3,M-4,M-5,P-15,C-1,C-2,T-12,T-13,F-4,F-5,D-14,T-9,P-14,T-8,P-11,D-15,D-16,M-7,F-8] .aom : iExecMaxNumWorkers : 10 ."},
    {"model_name":"scenario3", "ontology": ":ados-0 a aom:configuration;aom : model : ados-gnn ;aom : modelVersion : 0.1 ;aom : location : ipfs://bafybeiemxf5abjwjbikoz4mc3a3dla6ual3jsgpdr4cjr3oz3evfyavhwq/aom : idNodes [M-6,M-1,M-2,S-2,P-10,T-4,T-5,F-7,M-3,M-4,M-5,P-15,C-1,C-2,T-12,T-13,F-4,F-5,D-14,T-9,P-14,T-8,P-11,D-15,D-16,M-7,F-8] .aom : iExecMaxNumWorkers : 10 ."}]
    return jsonify(dictModels)

@app.route("/transactions/<ados_transaction_id>")
def adostransid(ados_transaction_id):

    outputFile = "/app/logs/" + ados_transaction_id
    with open(outputFile, 'r') as file:
        readFile = file.read()
        char1 = '('
        char2 = ')'
        try:
            completeString = readFile.split("tasks running", 1)[1]
            task_id = completeString[completeString.find(char1) + 1: completeString.find(char2)]
        except:
            task_id='unassigned'
        #TODO controlar cuando se está descomprimiendo el archivo
        if "Downloaded task result" in readFile:
            finalFile = '/app/computations/' + ados_transaction_id + '/result.json'
            notFound = True
            while notFound:
                path = Path(finalFile)
                if path.is_file():
                    with open(finalFile, 'r') as file2:
                        readFile2 = file2.read()
                        notFound = False
                        #return json.dumps({'source': ados_transaction_id, 'task_id': task_id, 'status': 'DELIVERED', 'data': readFile2}), 200
                        return jsonify({'source': ados_transaction_id, 'task_id': task_id, 'status': 'DELIVERED', 'data': readFile2}), 200
                else:
                    time.sleep(5)
        elif "successful" in readFile:
            return jsonify({'source': ados_transaction_id, 'task_id': task_id, 'status': 'COMPLETE'}), 200
        elif "REVEALING" in readFile:
            return jsonify({'source': ados_transaction_id, 'task_id': task_id, 'status': 'REVEALING'}), 200
        elif "ACTIVE" in readFile:
            return jsonify({'source': ados_transaction_id, 'task_id': task_id, 'status': 'ACTIVE'}), 200
        elif "UNSET" in readFile:
            return jsonify({'source': ados_transaction_id, 'task_id': task_id, 'status': 'UNSET'}), 200
        else:
            return jsonify({'source': ados_transaction_id, 'task_id': task_id, 'status': 'INITIATING'}), 200

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

