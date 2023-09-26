# Import the needed credential and management objects from the libraries.
import os

#from azure.identity import AzureCliCredential
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from authorizationAzure import resource_group

# Acquire a credential object using CLI-based authentication.
credential = DefaultAzureCredential()

# Retrieve subscription ID from environment variable.
subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]

# Obtain the management object for resources.
resource_client = ResourceManagementClient(credential, subscription_id)

# Provision the resource group.
rg_result = resource_client.resource_groups.create_or_update(
    resource_group, {"location": "eastus"}
)

print(
    f"Provisioned resource group {rg_result.name} in \
        the {rg_result.location} region"
)

