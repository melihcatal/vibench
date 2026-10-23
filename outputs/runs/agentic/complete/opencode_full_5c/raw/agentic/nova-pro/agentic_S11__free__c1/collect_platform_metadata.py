import boto3

bedrock = boto3.client("bedrock-runtime", region_name="us-west-2")


def invoke_model(model_id, payload):
    response = bedrock.invoke_model(modelId=model_id, body=payload)
    return response


if __name__ == "__main__":
    model_id = "amazon.titan-text-express-v1"
    payload = {"inputText": "Hello, world!"}
    response = invoke_model(model_id, payload)
    print(response)
