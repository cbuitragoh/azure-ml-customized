from azure.ai.ml.entities import Workspace
from authorizationAzure import ml_client, resource_group, subscription_id
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

workspace_name = "ws-devsptfy"

ws_basic = Workspace(
    name=workspace_name,
    location="eastus",
    display_name="Spotify_classification_workspace",
    description="workspace for dev spotify classification project",
    resource_group= resource_group
)
if ml_client.workspace_name == workspace_name:
    ml_client.workspaces.begin_create(ws_basic)
else:
    ml_client = MLClient(DefaultAzureCredential(), subscription_id, resource_group, workspace_name)
    ml_client.workspaces.begin_create(ws_basic)