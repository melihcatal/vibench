import boto3


def meeting_summary(text):
    bedrock = boto3.client(
        "bedrock-runtime",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    response = bedrock.invoke_model(ModelId="amazon.titan-text-express-v1", Body=text)
    return response.get("BodyReadAsBytes").decode("utf-8")
