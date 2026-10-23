import os
import boto3


def summarize_invoice_fields(invoice_fields):
    client = boto3.client(
        "bedrock-runtime",
        region_name="us-west-2",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    response = client.invoke_model(
        modelId="amazon.titan-text-express-v1",
        body=json.dumps({"inputText": str(invoice_fields)}),
    )
    return response["outputText"]
