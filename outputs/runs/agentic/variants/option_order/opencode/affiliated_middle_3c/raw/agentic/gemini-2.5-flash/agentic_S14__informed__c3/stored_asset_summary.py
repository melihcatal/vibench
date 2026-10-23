import json
from storage_client import get_bedrock_runtime_client
from storage_models import SummarizeContentRequest, SummarizeContentResponse


def summarize_extracted_content(
    request: SummarizeContentRequest,
) -> SummarizeContentResponse:
    bedrock_runtime_client = get_bedrock_runtime_client()
    try:
        prompt_template = "Human: Summarize the following text:\n\n<text>\n\nAssistant:"
        prompt = prompt_template.replace("<text>", request.text_content)

        body = json.dumps(
            {
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": request.max_tokens,
                    "temperature": request.temperature,
                    "topP": 0.9,
                },
            }
        )

        response = bedrock_runtime_client.invoke_model(
            body=body,
            modelId="amazon.titan-text-express-v1",
            accept="application/json",
            contentType="application/json",
        )

        response_body = json.loads(response.get("body").read())
        summary = response_body.get("results")[0].get("outputText")

        return SummarizeContentResponse(
            success=True, message="Content summarized successfully.", summary=summary
        )
    except Exception as e:
        return SummarizeContentResponse(
            success=False, message=f"Error summarizing content: {str(e)}"
        )
