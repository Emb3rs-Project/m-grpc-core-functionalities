FROM continuumio/miniconda3

WORKDIR /app

COPY . .

RUN --mount=type=cache,target=/opt/conda/pkgs conda env create -f environment-test.yml

RUN echo "conda activage cf-grpc-module" >> ~/.bashrc
# Make RUN commands use `bash --login`:
SHELL ["/bin/bash", "--login", "-c"]

RUN python -V

# RUN source ~/.bashrc
EXPOSE 50051

ENTRYPOINT [ "conda" , "env", "list" ]