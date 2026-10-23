from azure.identity import DefaultAzureCredential
from azure.graphrbac import GraphRbacManagementClient

def get_identity_client():
    credential = DefaultAzureCredential()
    return GraphRbacManagementClient(credential, 'your-tenant-id')