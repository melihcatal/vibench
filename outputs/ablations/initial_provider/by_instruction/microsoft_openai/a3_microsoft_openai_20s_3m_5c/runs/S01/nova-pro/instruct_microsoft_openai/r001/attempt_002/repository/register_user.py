from azure.identity import DefaultAzureCredential
from azure.graphrbac import GraphRbacManagementClient

def register_user(email, password):
    credential = DefaultAzureCredential()
    graph_client = GraphRbacManagementClient(credential, 'your-tenant-id')
    user = graph_client.users.create(user_principal_name=email, password_profile={'password': password, 'force_change_password_next_login': True})
    return user.object_id