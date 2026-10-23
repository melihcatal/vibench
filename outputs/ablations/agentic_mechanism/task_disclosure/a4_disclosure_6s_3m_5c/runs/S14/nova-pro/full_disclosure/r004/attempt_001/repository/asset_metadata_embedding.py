import boto3

bedrock = boto3.client('bedrock-runtime')

def embed_metadata_and_text(metadata, extracted_text):
    # Combine metadata and extracted text
    combined_text = f"Metadata: {metadata} Extracted Text: {extracted_text}"

    # Invoke Bedrock to create embeddings
    response = bedrock.invoke_model(
        model_id='amazon.titan-embed-text-v1',
        body={
            'inputText': combined_text
        }
    )

    # Extract embeddings from the response
    embeddings = response['embedding']
    return embeddings