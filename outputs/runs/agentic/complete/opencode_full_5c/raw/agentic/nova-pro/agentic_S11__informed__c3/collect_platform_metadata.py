import boto3

AWS_REGION = "us-west-2"
MODEL_ID = "amazon.titan-text-express-v1"

bedrock_client = boto3.client("bedrock-runtime", region_name=AWS_REGION)


def collect_metadata(response):
    metadata = {
        "modelId": MODEL_ID,
        "usage": response["usage"],
        "output": response["outputText"],
    }
    return metadata
