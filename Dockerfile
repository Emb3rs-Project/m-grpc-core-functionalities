FROM condaforge/mambaforge-pypy3

WORKDIR /app
COPY . .


# Update conda if a newer version is available
RUN --mount=type=cache,target=/opt/conda/pkgs mamba update mamba

# Create Environment
RUN --mount=type=cache,target=/opt/conda/pkgs mamba env create --file environment-py39.yml --force

RUN mamba init bash
RUN mamba activate cf-grpc-module
ENTRYPOINT PYTHONPATH=ms_grpc/plibs python -u server.py

EXPOSE 50051