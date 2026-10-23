from vision_client import get_openai_client
from vision_models import parse_openai_moderation_result

def check_text_for_safety(text_content: str):
    client = get_openai_client()
    response = client.moderations.create(input=text_content)
    return parse_openai_moderation_result(response)
