import os
import cohere

def stream_completion(prompt: str):
    """
    Streams partial output tokens from Cohere's hosted LLM.
    """
    co = cohere.Client(os.environ.get("COHERE_API_KEY"))

    response = co.chat(
        model='command', # Or 'command-light', etc.
        message=prompt,
        stream=True,
        temperature=0.7
    )

    for event in response:
        if event.event_type == 'text-generation':
            yield event.text
