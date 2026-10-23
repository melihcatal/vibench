import json
from typing import Dict, Any
from model_client import create_chat_completion
from model_models import ChatMessage, ChatCompletionRequest

def extract_json(text: str) -> Dict[str, Any]:
    messages = [
        ChatMessage(
            role="system",
            content="""You are a JSON extractor. Analyze the text and extract structured information as a valid JSON object. 
            Include relevant keys like entities, topics, sentiment based on the content."""
        ),
        ChatMessage(role="user", content=text),
    ]
    request = ChatCompletionRequest(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.0,
        response_format={"type": "json_object"},
    )
    response = create_chat_completion(request)
    content = response.choices[0].message.content.strip()
    return json.loads(content)