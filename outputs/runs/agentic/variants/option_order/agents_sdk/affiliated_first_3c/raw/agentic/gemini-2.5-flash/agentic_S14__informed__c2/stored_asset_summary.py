
import json
from storage_client import get_bedrock_runtime_client
from storage_models import SummarizeContentRequest, SummarizeContentResponse

def summarize_stored_asset_content(request: SummarizeContentRequest) -> SummarizeContentResponse:
    bedrock_runtime_client = get_bedrock_runtime_client()

    # Using Amazon Titan Text Express v1 model for summarization
    model_id = 'amazon.titan-text-express-v1'

    prompt = f"Summarize the following text:

{request.text_content}

Summary:"

    body = json.dumps({
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": request.max_tokens,
            "temperature": 0.5,
            "topP": 0.9
        }
    })

    response = bedrock_runtime_client.invoke_model(
        body=body,
        modelId=model_id,
        accept='application/json',
        contentType='application/json'
    )

    response_body = json.loads(response.get('body').read())
    summary_text = response_body.get('results')[0].get('outputText', '').strip()

    return SummarizeContentResponse(summary_text=summary_text)
