import os
from azure.monitor.query import MetricsQueryClient, MetricsQueryOptions
from azure.core.credentials import AzureKeyCredential

# Load configuration from environment variables
subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
resource_group = os.getenv('AZURE_RESOURCE_GROUP')
workspace_id = os.getenv('AZURE_WORKSPACE_ID')
api_key = os.getenv('AZURE_API_KEY')

# Create a client
credential = AzureKeyCredential(api_key)
client = MetricsQueryClient(credential)