import json
from speech_client import get_bedrock_runtime_client
from speech_models import EmbeddingResult

def embed_text_segment(text_segment: str) -> EmbeddingResult:
    bedrock_runtime_client = get_bedrock_runtime_client()
    model_id = "amazon.titan-embed-text-v1"
    try:
        body = json.dumps({"inputText": text_segment})
        response = bedrock_runtime_client.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json"
        )
        response_body = json.loads(response.get('body').read())
        embedding = response_body.get("embedding")

        print(f"Text segment embedded using {model_id}.")
        return EmbeddingResult(
            segment_text=text_segment,
            embedding=embedding
        )
    except Exception as e:
        print(f"Error embedding text segment with AWS Bedrock: {e}")
        raise
