# Compute Instances need to have a unique name across the region.
# Here we create a unique name with current datetime
from azure.ai.ml.entities import ComputeInstance, AmlCompute
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from authorizationAzure import ml_client, resource_group, subscription_id
from createWorkspace import workspace_name
import datetime
import time

# create compute instance for running notebooks and jobs
#ci_name = "spotify-clsf-ci" + datetime.datetime.now().strftime("%Y%m%d%H%M")
ci_name = "spotify-clsf-ci"
ci_instance = ComputeInstance(name=ci_name, size="Standard_DS11_v2")
if ml_client.workspace_name == workspace_name:
   ml_client.begin_create_or_update(ci_instance).result()
else:
    ml_client = MLClient(DefaultAzureCredential(), subscription_id, resource_group, workspace_name)
    ml_client.begin_create_or_update(ci_instance).result()  

time.sleep(20)

# create a compute cluster for running jobs and pipelines
#aml_name = "spotify-clsf-cluster" + datetime.datetime.now().strftime("%Y%m%d%H%M")
aml_name = "spotify-clsf-cluster"
aml_cluster = AmlCompute(name=aml_name, size="Standard_DS11_v2", max_instances=2)
if ml_client.workspace_name == workspace_name:
    ml_client.begin_create_or_update(aml_cluster).result()
else:
    ml_client = MLClient(DefaultAzureCredential(), subscription_id, resource_group, workspace_name)
    ml_client.begin_create_or_update(aml_cluster).result()

