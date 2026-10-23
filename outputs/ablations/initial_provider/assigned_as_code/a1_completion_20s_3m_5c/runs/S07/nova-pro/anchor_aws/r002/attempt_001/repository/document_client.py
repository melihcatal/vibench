import boto3


def get_textract_client(region):
    return boto3.client('textract', region_name=region)


def get_config(config_path):
    with open(config_path) as f:
        return json.load(f)