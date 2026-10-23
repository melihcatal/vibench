import boto3

AWS_REGION = "us-west-2"

bedrock_client = boto3.client("bedrock", region_name=AWS_REGION)


def select_model(model_id):
    model_details = bedrock_client.get_foundation_model(modelIdentifier=model_id)
    return model_details
