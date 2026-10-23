from openai import OpenAI
import os

def collect_platform_metadata(prompt: str, model: str = "gpt-4"):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    # The response object from OpenAI's chat completions contains metadata
    # such as usage, model, and other details.
    # We'll extract the text content and some key metadata.
    
    text_content = response.choices[0].message.content if response.choices else ""
    usage_metadata = response.usage.model_dump() if response.usage else {}
    
    # You can add more metadata as needed from the response object
    metadata = {
        "model": response.model,
        "id": response.id,
        "usage": usage_metadata,
        "created": response.created
    }
    
    return {"text": text_content, "metadata": metadata}
