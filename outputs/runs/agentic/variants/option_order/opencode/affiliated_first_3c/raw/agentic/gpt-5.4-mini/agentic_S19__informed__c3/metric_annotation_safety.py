from openai import OpenAI


def metric_annotation_safety(text: str, model: str = 'omni-moderation-latest') -> bool:
    client = OpenAI()
    response = client.moderations.create(model=model, input=text)
    return not any(result.flagged for result in response.results)
