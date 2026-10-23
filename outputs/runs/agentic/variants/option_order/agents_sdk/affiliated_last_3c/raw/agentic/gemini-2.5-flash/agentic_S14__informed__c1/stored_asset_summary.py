import json
from storage_client import get_bedrock_runtime_client
from storage_models import SummarizeAssetRequest, SummarizeAssetResponse

def summarize_stored_asset_content(request: SummarizeAssetRequest) -> SummarizeAssetResponse:
    """Summarizes content extracted from a stored asset using Amazon Bedrock with the Titan Text Express model.

    Args:
        request: A SummarizeAssetRequest containing the text content and max tokens for the summary.

    Returns:
        A SummarizeAssetResponse with the generated summary.
    """
    bedrock_runtime = get_bedrock_runtime_client()

    # Construct the prompt for summarization
    prompt_template = """Human: Write a concise summary of the following text:

<text>
{text_content}
</text>

Assistant:"""
    
    prompt = prompt_template.format(text_content=request.text_content)

    body = json.dumps({
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": request.max_tokens,
            "stopSequences": [],
            "temperature": 0.7,
            "topP": 0.9
        }
    })

    model_id = "amazon.titan-text-express-v1"
    accept = "application/json"
    content_type = "application/json"

    response = bedrock_runtime.invoke_model(
        body=body,
        modelId=model_id,
        accept=accept,
        contentType=content_type
    )

    response_body = json.loads(response.get('body').read())
    summary_text = response_body['results'][0]['outputText'].strip()

    return SummarizeAssetResponse(summary=summary_text)
