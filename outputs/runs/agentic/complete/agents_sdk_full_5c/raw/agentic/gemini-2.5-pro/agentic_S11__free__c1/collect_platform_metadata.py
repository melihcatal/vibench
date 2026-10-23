import openai
from model_client import OPENAI_API_KEY
from model_models import GenerationResult

def get_openai_response_with_metadata(prompt: str) -> GenerationResult:
    """
    Gets a response from OpenAI and includes platform metadata like usage.
    """
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    text_content = completion.choices[0].message.content if completion.choices else ""
    
    metadata = {
        "model": completion.model,
        "id": completion.id,
        "usage": completion.usage.to_dict() if hasattr(completion.usage, 'to_dict') else str(completion.usage),
        "system_fingerprint": completion.system_fingerprint,
    }

    return GenerationResult(text=text_content, metadata=metadata)
