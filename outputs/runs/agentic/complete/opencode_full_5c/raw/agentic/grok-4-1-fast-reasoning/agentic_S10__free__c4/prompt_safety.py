from model_client import get_llm_client


def check_for_unsafe_content(text: str) -> bool:
    client = get_llm_client()
    response = client.moderations.create(input=text, model="text-moderation-latest")
    return not response.results[0].flagged
