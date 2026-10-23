import json
from vision_client import VisionClient
from vision_models import TextSafetyRequest, TextSafetyResponse


def visual_safety_text(payload: TextSafetyRequest, config=None) -> TextSafetyResponse:
    config = config or {}
    region_name = config.get("region")
    client = VisionClient(region_name)

    # Use Amazon Comprehend to detect PII and general sentiment,
    # and Amazon Bedrock with a generative model for more nuanced moderation.
    # For simplicity, let's use Bedrock for a direct safety check as it can be more comprehensive.

    model_id = config.get("bedrock_text_safety_model_id", "anthropic.claude-instant-v1")

    prompt = f"""Human: Analyze the following text for any unsafe, harmful, or policy-violating content.
Respond with "True" if the text is unsafe and "False" if it is safe.
If it is unsafe, provide a brief reason.

<text_to_analyze>
{payload.text_content}
</text_to_analyze>

Assistant:"""

    body = json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": 200,
        "temperature": 0.1,
    })

    response = client.bedrock_runtime_client.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=body,
    )

    response_body = json.loads(response["body"].read())
    bedrock_response_text = response_body.get("completion", "").strip()

    is_unsafe = "True" in bedrock_response_text
    safety_details = bedrock_response_text.replace("True", "").replace("False", "").strip()

    return TextSafetyResponse(is_unsafe=is_unsafe, safety_details=safety_details)