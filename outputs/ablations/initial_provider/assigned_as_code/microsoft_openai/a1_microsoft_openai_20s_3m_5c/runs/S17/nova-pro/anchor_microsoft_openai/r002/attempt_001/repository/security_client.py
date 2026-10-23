from azure.identity import DefaultAzureCredential


def get_security_client(config):
    credential = DefaultAzureCredential()
    return credential, config