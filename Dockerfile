FROM condaforge/mambaforge-pypy3

WORKDIR /app
COPY . .


# Update conda if a newer version is available
RUN --mount=type=cache,target=/opt/conda/pkgs mamba update mamba;

# Create Environment
RUN --mount=type=cache,target=/opt/conda/pkgs mamba env create --file environment-py39.yml --force;

# Add grpc to PythonPath
ENV PYTHONPATH=ms_grpc/plibs

ENTRYPOINT ["conda", "run", "-n","cf-grpc-module", "python","server.py"]