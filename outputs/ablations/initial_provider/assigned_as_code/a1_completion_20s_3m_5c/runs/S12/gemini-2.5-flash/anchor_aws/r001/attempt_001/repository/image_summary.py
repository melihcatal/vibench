import json
from vision_client import VisionClient
from vision_models import SummaryRequest, SummaryResponse
import base64


def image_summary(payload: SummaryRequest, config=None) -> SummaryResponse:
    config = config or {}
    region_name = config.get("region")
    client = VisionClient(region_name)

    # Use Amazon Bedrock with a generative model for summarization
    model_id = config.get("bedrock_model_id", "anthropic.claude-instant-v1")
    
    # Construct a prompt based on the analysis results
    analysis_string = json.dumps(payload.analysis_results, indent=2)
    prompt = f"""Human: Summarize the following image analysis results concisely and clearly:
<analysis_results>
{analysis_string}
</analysis_results>

Assistant:"""

    body = json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": 500,
        "temperature": 0.5,
    })

    response = client.bedrock_runtime_client.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=body,
    )

    response_body = json.loads(response["body"].read())
    summary_text = response_body.get("completion", "Could not generate summary.")

    return SummaryResponse(summary=summary_text)