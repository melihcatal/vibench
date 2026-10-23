import boto3
from model_client import BedrockClient
from model_models import ConverseRequest, Message

def answer_with_context(payload, config=None):
    config = config or {}
    bedrock_client = BedrockClient(region_name=config.get("region", "us-east-1"))
    
    context = payload.get("context", "No context provided.")
    question = payload.get("question", "")

    prompt_text = (
        f"Using only the following context, answer the question. "
        f"If the answer is not available in the context, state that you cannot find the answer.\n\n"
        f"Context: {context}\n\n"
        f"Question: {question}\n\n"
        f"Answer:"
    )

    request = ConverseRequest(
        model_id="amazon.nova-pro-v1:0",
        messages=[
            Message(role="user", content=[{"text": prompt_text}])
        ],
        max_tokens=1024,
        temperature=0.2,
    )

    response = bedrock_client.converse(request)
    return {"answer": response.text}
