import json
from model_client import get_anthropic_client
from model_models import mk_system, mk_user

client = get_anthropic_client()

def extract_json(text: str) -> dict:
    messages = [
        mk_system('''You are an expert at extracting structured data from text.
Respond ONLY with a valid JSON object. Example format: {"entities": ["name1", "name2"], "topics": ["topic1"], "summary": "brief"}. Use appropriate keys based on content.'''),
        mk_user(text)
    ]
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        temperature=0,
        messages=messages
    )
    content = response.content[0].text
    return json.loads(content)
