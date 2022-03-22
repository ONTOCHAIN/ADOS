FROM ubuntu:20.04

RUN apt update
RUN apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
#RUN apt install -y python3.6
RUN apt install -y python3-pip
RUN pip3 install numpy==1.21


# CPU only
RUN pip3 install torch==1.5.1+cpu torchvision==0.6.1+cpu -f https://download.pytorch.org/whl/torch_stable.html

### CPU installations

RUN pip install torch-geometric==1.5.0 -f https://data.pyg.org/whl/torch-1.5.0+cpu.html
RUN pip install --no-index torch-scatter -f https://data.pyg.org/whl/torch-1.5.0+cpu.html
RUN pip install --no-index torch-sparse -f https://data.pyg.org/whl/torch-1.5.0+cpu.html
RUN pip install --no-index torch-cluster -f https://data.pyg.org/whl/torch-1.5.0+cpu.html
RUN pip install --no-index torch-spline-conv -f https://data.pyg.org/whl/torch-1.5.0+cpu.html


### CUDA installations
#RUN pip3 install torch==1.5.1 torchvision==0.6.1 -f https://download.pytorch.org/whl/torch_stable.html
#RUN pip3 install torch-geometric==1.5.0
#RUN pip3 install --no-index torch-scatter -f https://data.pyg.org/whl/torch-1.5.0+cu102.html
#RUN pip3 install --no-index torch-sparse -f https://data.pyg.org/whl/torch-1.5.0+cu102.html
#RUN pip3 install --no-index torch-cluster -f https://data.pyg.org/whl/torch-1.5.0+cu102.html
#RUN pip3 install --no-index torch-spline-conv -f https://data.pyg.org/whl/torch-1.5.0+cu102.html


COPY ./src /app


ENTRYPOINT ["python3", "/app/main.py"]