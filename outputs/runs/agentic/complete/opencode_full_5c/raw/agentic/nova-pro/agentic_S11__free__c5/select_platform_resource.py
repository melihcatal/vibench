import boto3

bedrock_client = boto3.client("bedrock-runtime")


def select_model(model_id):
    return model_id
