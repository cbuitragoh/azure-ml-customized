from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
import os

subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
resource_group = 'rg-devsptfy'
workspace = "ws-devsptfy"

ml_client = MLClient(
    DefaultAzureCredential(), subscription_id, resource_group, workspace
)
print("successful connection Azure")