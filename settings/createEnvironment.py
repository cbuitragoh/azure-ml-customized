from azure.ai.ml.entities import Environment
from authorizationAzure import ml_client

custom_env_name = "sklearn-clf-env"
env = Environment(
    image="mcr.microsoft.com/azureml/openmpi3.1.2-ubuntu18.04",
    conda_file="./settings/conda.yml",
    name=custom_env_name,
    description="customized environment created for spotify classification",
)
ml_client.environments.create_or_update(env)