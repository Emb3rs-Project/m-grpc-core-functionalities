# Module gRPC - Core Functionalities 
Platform gRPC Integration Module to communicate with CF Module.

## Git
Clone this repository:
```shell
git clone https://github.com/Emb3rs-Project/m-grpc-core-functionalities.git
```

Load submodules:
```shell
git submodule init
git submodule update
```

## Setup Local Environment
Create Conda environment and install packages:
```shell
conda env create -n cf-grpc-module -f environment-py39.yml
conda activate  cf-grpc-module
```

Create environment variables config file:
```shell
cp .env.example .env
```

Run grpc server:
```shell
PYTHONPATH=$PYTHONPATH:ms_grpc/plibs:module python server.py
```

## Setup Docker Environment
Create environment variables config file:
```shell
cp .env.example .env
```

Build docker image:
```shell
DOCKER_BUILDKIT=1 docker build -t m-grpc-cf .
```

Run docker image:
```shell
docker run -p 50051:50051 --name m-grpc-cf --rm m-grpc-cf
```

**NOTE**: *If you've run docker-dev from the Emb3rs-project repository before, I advise use the embers network 
in docker run to access PGSQL and change the database settings inside .env to Platform DB.*  

Run docker image with embers network:
```shell
docker run -p 50051:50051 --network dev_embers|platform_embers --name m-grpc-cf --rm m-grpc-cf
```