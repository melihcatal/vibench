import os


class PlatformRequest:
    def __init__(self, messages, resource_id=None, temperature=0.2, max_tokens=256):
        self.messages = messages
        self.resource_id = resource_id
        self.temperature = temperature
        self.max_tokens = max_tokens

    @classmethod
    def from_env(cls):
        prompt = os.getenv("PLATFORM_PROMPT", "Summarize the latest platform update.")
        return cls([
            {"role": "system", "content": "You are a concise managed platform assistant."},
            {"role": "user", "content": prompt},
        ], os.getenv("AZURE_OPENAI_DEPLOYMENT"))


def normalize_text_response(response):
    return response.choices[0].message.content


def stream_text_chunks(response):
    for event in response:
        delta = event.choices[0].delta
        if getattr(delta, "content", None):
            yield delta.content


def collect_response_payload(response):
    return {
        "text": response.choices[0].message.content,
        "usage": response.usage.model_dump() if response.usage else None,
        "model": response.model,
        "id": response.id,
    }
