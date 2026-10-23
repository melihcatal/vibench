import boto3


def image_summary(image_path):
    client = boto3.client("bedrock-runtime")
    response = client.invoke_model(
        ModelId="amazon.titan-text-express-v1",
        Body={"inputText": f"Summarize the following image: {image_path}"},
    )
    return response["Body"].read().decode("utf-8")
