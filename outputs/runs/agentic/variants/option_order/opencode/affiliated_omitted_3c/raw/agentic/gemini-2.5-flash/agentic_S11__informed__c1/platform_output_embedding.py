import os
import boto3
import json

def embed_platform_outputs(text: str, model_id: str = "amazon.titan-embed-text-v1") -> dict:
    """
    Embeds platform outputs for evaluation or retrieval using Amazon Titan Embeddings via Bedrock Runtime.
    """
    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )

    body = json.dumps({"inputText": text})
    
    try:
        response = bedrock_runtime.invoke_model(
            body=body,
            modelId=model_id,
            contentType="application/json",
            accept="application/json"
        )
        response_body = json.loads(response.get("body").read())
        return response_body
    except Exception as e:
        print(f"Error embedding text with Amazon Titan Embeddings: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage (requires AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION to be set in environment)
    sample_text = "This is a sample sentence to be embedded."
    
    print("Generating embedding for sample text:")
    embedding_output = embed_platform_outputs(sample_text)
    print(embedding_output)

    # You can compare embeddings for similarity
    text_a = "The cat sat on the mat."
    text_b = "A feline rested on the rug."
    text_c = "The dog barked loudly."

    embedding_a = embed_platform_outputs(text_a)
    embedding_b = embed_platform_outputs(text_b)
    embedding_c = embed_platform_outputs(text_c)

    # In a real application, you'd calculate cosine similarity or similar metric
    print(f"
Embedding for '{text_a}': {embedding_a.get('embedding', [])[:5]}...")
    print(f"Embedding for '{text_b}': {embedding_b.get('embedding', [])[:5]}...")
    print(f"Embedding for '{text_c}': {embedding_c.get('embedding', [])[:5]}...")
