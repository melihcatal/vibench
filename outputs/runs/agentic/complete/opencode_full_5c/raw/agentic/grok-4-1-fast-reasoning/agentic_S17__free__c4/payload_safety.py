from typing import Union
from security_client import get_openai_client


def is_payload_safe(payload: Union[str, bytes]) -> bool:
    client = get_openai_client()
    text = payload.decode("utf-8") if isinstance(payload, bytes) else str(payload)
    response = client.moderations.create(model="text-moderation-latest", input=text)
    return not response.results[0].flagged
