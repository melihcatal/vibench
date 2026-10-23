import json
from storage_client import get_bedrock_runtime_client
from storage_models import SummarizeContentRequest, SummarizeContentResponse


def summarize_content(request: SummarizeContentRequest) -> SummarizeContentResponse:
    bedrock_runtime_client = get_bedrock_runtime_client()
    try:
        # Using Amazon Titan Text G1 - Express for summarization
        # Model ID might vary, confirm the exact model ID for Titan or other supported models
        model_id = "amazon.titan-text-express-v1"

        body = json.dumps(
            {
                "inputText": request.content,
                "textGenerationConfig": {
                    "maxTokenCount": request.max_tokens,
                    "temperature": request.temperature,
                    "topP": 0.9,
                },
            }
        )

        response = bedrock_runtime_client.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json",
        )

        response_body = json.loads(response.get("body").read())
        summary_text = response_body.get("results")[0].get("outputText")

        return SummarizeContentResponse(summary=summary_text.strip())
    except Exception as e:
        raise RuntimeError(f"Failed to summarize content using Bedrock: {e}")
