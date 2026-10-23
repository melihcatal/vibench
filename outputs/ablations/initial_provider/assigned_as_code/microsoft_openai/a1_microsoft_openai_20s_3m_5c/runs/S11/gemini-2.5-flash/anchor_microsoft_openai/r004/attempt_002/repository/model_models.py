def create_chat_completion_request(prompt: str, model_deployment_name: str):
    return {
        "model": model_deployment_name,
        "messages": [{'role': 'user', 'content': prompt}]
    }

def parse_chat_completion_response(response):
    return {
        'text': response.choices[0].message.content or '',
        'usage': response.usage.model_dump() if response.usage else None,
        'model_id': response.model
    }
