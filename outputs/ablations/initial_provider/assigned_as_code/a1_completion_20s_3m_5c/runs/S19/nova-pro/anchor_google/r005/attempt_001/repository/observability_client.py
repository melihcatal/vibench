import os


def get_config():
    return {
        'project_id': os.getenv('GOOGLE_CLOUD_PROJECT_ID'),
        'region': os.getenv('AWS_REGION', 'us-east-1'),
        'subscription_id': os.getenv('AZURE_SUBSCRIPTION_ID'),
        'resource_group': os.getenv('AZURE_RESOURCE_GROUP'),
        'vm_name': os.getenv('AZURE_VM_NAME'),
        'access_token': os.getenv('AZURE_ACCESS_TOKEN')
    }


def normalize_payload(payload):
    return {
        'metric': payload.get('metric', ''),
        'start_time': payload.get('start_time', ''),
        'end_time': payload.get('end_time', ''),
        'namespace': payload.get('namespace', ''),
        'metric_name': payload.get('metric_name', ''),
        'metric_names': payload.get('metric_names', [])
    }