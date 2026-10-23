import boto3


def summarize_invoice_fields(extracted_data):
    client = boto3.client("bedrock-runtime")
    response = client.invoke_model(
        model_id="amazon.titan-text-lite",
        body={"inputText": f"Summarize the following invoice fields: {extracted_data}"},
    )
    return response["outputText"]
