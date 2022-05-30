FROM continuumio/miniconda3

WORKDIR /app
COPY . .


# Update conda if a newer version is available
RUN conda update --name base --channel defaults conda --yes;

# Create Environment
RUN conda env create --file environment-py39.yml --force;

# Add grpc to PythonPath
RUN export PYTHONPATH=ms_grpc/plibs

ENTRYPOINT ["conda", "run", "--no-capture-output", "--name", "cf-grpc-module", "python", "-u", "server.py"]