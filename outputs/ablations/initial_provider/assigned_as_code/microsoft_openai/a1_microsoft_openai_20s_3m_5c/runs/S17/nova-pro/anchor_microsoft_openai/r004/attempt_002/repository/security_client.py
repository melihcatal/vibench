from azure.identity import DefaultAzureCredential

def get_client(config):
    with DefaultAzureCredential() as credential:
        return credential

def get_config(config):
    return config or {}