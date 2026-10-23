from azure.identity import DefaultAzureCredential


def get_client(config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        return LogsIngestionClient(endpoint=config['endpoint'], credential=credential)


def get_query_client(config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        return LogsQueryClient(credential=credential)
