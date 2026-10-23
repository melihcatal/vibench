import boto3
import json
from storage_client import get_bedrock_runtime_client
from storage_models import SummarizeRequest

def summarize_stored_asset(request: SummarizeRequest) -> str:
    bedrock_runtime = get_bedrock_runtime_client()
    model_id = "amazon.titan-text-express-v1"

    prompt = f"Summarize the following text:\n\n{request.text}"

    body = json.dumps({
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": request.max_tokens,
            "temperature": 0.7,
            "topP": 0.9,
        }
    })

    try:
        response = bedrock_runtime.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json"
        )

        response_body = json.loads(response.get('body').read())
        return response_body['results'][0]['outputText']

    except bedrock_runtime.exceptions.ClientError as e:
        raise RuntimeError(f"Amazon Bedrock failed to summarize content: {e}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred during summarization: {e}")
