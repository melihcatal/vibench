from model_client import get_openai_client


def check_safety(prompt: str, generation: str = "") -> bool:
    client = get_openai_client()
    texts = [prompt]
    if generation:
        texts.append(generation)
    response = client.moderations.create(
        model="text-moderation-3.5-2024",
        input=texts,
    )
    return all(not result.flagged for result in response.results)
