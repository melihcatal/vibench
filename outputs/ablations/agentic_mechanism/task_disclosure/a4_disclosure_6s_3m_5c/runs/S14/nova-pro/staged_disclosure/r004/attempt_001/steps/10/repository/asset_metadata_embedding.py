import boto3

bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

def embed_text(text):
    response = bedrock.invoke_model(
        model_id="amazon.titan-embed-text-v1",
        body={
            "inputText": text
        }
    )
    result = json.loads(response["body"].read())
    return result["embedding"]

# Example usage
metadata = {
    "object_id": "12345",
    "object_type": "document",
    "text": "This is an example document."
}

embedding = embed_text(metadata["text"])
print(f"Embedding for object {metadata['object_id']}: {embedding}")