from model_client import BedrockModelClient
from model_models import TextPayload

def stream_completion(payload: TextPayload, config=None):
    client = BedrockModelClient(region_name=config.get("region") if config else None)

    prompt = f"""Continue the following text as a creative story. Stream the output token by token.

Start of story: {payload.text}

Continuation:"""

    messages = [
        {"role": "user", "content": [{"text": prompt}]}
    ]

    # The client.invoke_llm_stream method already returns a generator
    return client.invoke_llm_stream(
        messages=messages,
        inference_config={
            "maxTokens": 1024,
            "temperature": 0.8, # Higher temperature for creative story generation
            "topP": 0.9
        },
        model_id="anthropic.claude-3-haiku-20240307-v1:0" # Using Claude 3 Haiku for good streaming
    )
