import boto3

AWS_ACCESS_KEY_ID = "your_access_key_id"
AWS_SECRET_ACCESS_KEY = "your_secret_access_key"


def summarize_invoice_fields(extracted_data):
    bedrock = boto3.client(
        "bedrock-runtime",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    prompt = f"Summarize the following invoice fields: {extracted_data}"
    response = bedrock.invoke_model(modelId="amazon.titan-text-express-v1", body=prompt)
    return response
