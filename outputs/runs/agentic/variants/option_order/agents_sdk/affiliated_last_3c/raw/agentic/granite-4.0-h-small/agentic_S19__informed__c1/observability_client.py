# [HELPER] observability_client.py

import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.monitor import MonitorManagementClient

def get_azure_monitor_client() -> MonitorManagementClient:
    """Create an authenticated Azure Monitor Management Client using DefaultAzureCredential.
    The credential chain handles environment variables (AZURE_TENANT_ID, AZURE_CLIENT_ID, etc.)
    and managed identity where applicable.
    Returns:
        Instance of MonitorManagementClient ready for metric queries.
    """
    credential = DefaultAzureCredential()
    # Azure Monitor ManagementClient requires Azure AD token, not subscription ID alone.
    return MonitorManagementClient(credential=credential, subscription_id=os.getenv('AZURE_SUBSCRIPTION_ID'))