import boto3

def get_bedrock_client(service_name, region_name="us-east-1", config=None):
    config = config or {}
    region = config.get("region", region_name)
    return boto3.client(service_name, region_name=region)

def get_bedrock_runtime_client(region_name="us-east-1", config=None):
    return get_bedrock_client("bedrock-runtime", region_name, config)

def get_bedrock_agent_runtime_client(region_name="us-east-1", config=None):
    return get_bedrock_client("bedrock-agent-runtime", region_name, config)
