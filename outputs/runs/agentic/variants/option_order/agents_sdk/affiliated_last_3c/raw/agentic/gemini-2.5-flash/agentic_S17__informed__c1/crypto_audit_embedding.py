import boto3
import os
from security_client import get_bedrock_runtime_client

def embed_audit_note(audit_note: str) -> list:
    """
    Embeds a cryptographic audit note using Amazon Titan Embeddings via Bedrock.
    """
    bedrock_client = get_bedrock_runtime_client()
    
    try:
        model_id = "amazon.titan-embed-text-v1"
        
        response = bedrock_client.invoke_model(
            body=f'{{"inputText": "{audit_note}"}}',
            modelId=model_id,
            accept="application/json",
            contentType="application/json"
        )
        
        response_body = response['body'].read().decode('utf-8')
        embedding_data = json.loads(response_body)
        
        return embedding_data['embedding']
    except Exception as e:
        print(f"Error creating embedding with Amazon Titan: {e}")
        raise

if __name__ == '__main__':
    # Example Usage
    # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION_NAME must be set.
    # Ensure the AWS account has access to Amazon Bedrock and the Titan Embeddings model.
    
    audit_note_1 = "KMS key rotation successfully completed for encryption key 'arn:aws:kms:us-east-1:123456789012:key/abcde123-4567-8901-2345-67890abcdef'."
    audit_note_2 = "Decryption request failed due to invalid ciphertext format for application 'data-processor'."
    audit_note_3 = "New asymmetric signing key 'arn:aws:kms:us-east-1:123456789012:key/fedcba98-7654-3210-fedc-ba9876543210' created and enabled."
    
    print("Embedding Audit Note 1:")
    try:
        embedding_1 = embed_audit_note(audit_note_1)
        print(f"Embedding vector (first 5 elements): {embedding_1[:5]}...")
        print(f"Embedding dimension: {len(embedding_1)}")
    except Exception as e:
        print(f"Embedding failed for note 1: {e}")

    print("\nEmbedding Audit Note 2:")
    try:
        embedding_2 = embed_audit_note(audit_note_2)
        print(f"Embedding vector (first 5 elements): {embedding_2[:5]}...")
    except Exception as e:
        print(f"Embedding failed for note 2: {e}")
