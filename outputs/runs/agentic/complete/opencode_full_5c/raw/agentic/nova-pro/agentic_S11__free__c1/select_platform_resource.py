import boto3

bedrock = boto3.client("bedrock", region_name="us-west-2")


def list_models():
    response = bedrock.list_foundation_models()
    return response


if __name__ == "__main__":
    models = list_models()
    print(models)
