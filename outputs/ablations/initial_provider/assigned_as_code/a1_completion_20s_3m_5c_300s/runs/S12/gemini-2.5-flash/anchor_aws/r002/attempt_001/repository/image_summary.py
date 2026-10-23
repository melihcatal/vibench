import boto3
import json
from typing import Dict, Any
from vision_client import get_bedrock_runtime_client
from vision_models import ImageSummaryRequest, ImageSummaryResponse

def image_summary(payload: ImageSummaryRequest, config: Dict[str, Any]) -> ImageSummaryResponse:
    client = get_bedrock_runtime_client(config)
    
    prompt_parts = []
    prompt_parts.append("Based on the following visual analysis, summarize the image:")
    
    if payload.description:
        prompt_parts.append(f"- Image description: {payload.description}")
    
    if payload.detected_labels:
        labels_str = ", ".join([f"{label.name} ({(label.confidence*100):.2f}%)" for label in payload.detected_labels])
        prompt_parts.append(f"- Detected labels: {labels_str}")
        
    if payload.detected_text:
        texts_str = ", ".join([f"\'{text.detected_text}\' ({(text.confidence*100):.2f}%)" for text in payload.detected_text])
        prompt_parts.append(f"- Detected text: {texts_str}")
        
    if payload.moderation_labels:
        mod_labels_str = ", ".join([f"{label.name} ({(label.confidence*100):.2f}%)" for label in payload.moderation_labels])
        prompt_parts.append(f"- Moderation labels: {mod_labels_str}")
        
    prompt = "\n".join(prompt_parts)
    
    # Using Anthropic Claude as an example model via Bedrock
    model_id = config.get("bedrock_model_id", "anthropic.claude-v2") # Or other suitable model like cohere.command-text-v14
    
    body = json.dumps({
        "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
        "max_tokens_to_sample": 300,
        "temperature": 0.5,
        "stop_sequences": ["\n\nHuman:"]
    })
    
    response = client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )
    
    response_body = json.loads(response.get('body').read())
    summary = response_body.get('completion', '').strip()

    return ImageSummaryResponse(summary=summary)
