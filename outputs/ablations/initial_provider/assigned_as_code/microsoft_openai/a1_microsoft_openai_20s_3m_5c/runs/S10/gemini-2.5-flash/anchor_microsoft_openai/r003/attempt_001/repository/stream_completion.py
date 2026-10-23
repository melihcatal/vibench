import os
from model_client import get_openai_client

def stream_completion(payload, config=None):
    config = config or {}
    client = get_openai_client(api_key=config.get('api_key'))
    
    prompt = payload.get('prompt', '')

    stream = client.chat.completions.create(
        model='gpt-5.4-mini',
        messages=[{'role': 'user', 'content': prompt}],
        stream=True,
    )

    # In a real application, you would iterate and yield tokens.
    # For this file, we'll concatenate them to demonstrate the output structure.
    full_response_content = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            full_response_content += chunk.choices[0].delta.content
            # In a real streaming scenario, you would yield chunk.choices[0].delta.content
            # print(chunk.choices[0].delta.content, end="") # Example of real-time print
    
    return {'streamed_content': full_response_content}
