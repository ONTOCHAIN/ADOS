FROM nikolaik/python-nodejs:latest

# requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# install iexec sdk cli
RUN npm i -g iexec

# copy every content from the local file to the image
COPY . /app

RUN mkdir /root/.ethereum/
RUN mkdir /root/.ethereum/keystore
RUN mkdir /app/iexec_conf
RUN mkdir /app/logs
RUN mkdir /app/computations

# configure the container to run in an executed manner
CMD ["python", "-u", "ados.py" ]
