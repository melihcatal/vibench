import openai
from storage_client import get_s3_client

def summarize_stored_asset(bucket_name: str, object_key: str, prompt: str = "Provide a concise summary of the content:") -> str:
    """Summarize the content of a stored asset using OpenAI GPT model.

    The function retrieves the object (assumed to be textual), then calls the language model.
    """
    client = get_s3_client()
    obj = client.get_object(Bucket=bucket_name, Key=object_key)
    content = obj['Body'].read().decode('utf-8')
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"{prompt}\n\n{content}"}]
    )
    return response.choices[0].message.content.strip()