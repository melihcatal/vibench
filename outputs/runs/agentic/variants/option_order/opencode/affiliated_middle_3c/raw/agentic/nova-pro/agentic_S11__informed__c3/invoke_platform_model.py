import boto3

AWS_ACCESS_KEY_ID = "your_access_key_id"
AWS_SECRET_ACCESS_KEY = "your_secret_access_key"

bedrock = boto3.client(
    "bedrock-runtime",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name="us-west-2",
)


def invoke_platform_model(prompt):
    response = bedrock.invoke_model(
        modelId="amazon.titan-text-express-v1", body={"inputText": prompt}
    )
    return response
