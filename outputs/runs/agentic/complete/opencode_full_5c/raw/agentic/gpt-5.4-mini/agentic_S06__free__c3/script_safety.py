from openai import OpenAI


def check_script_safety(script: str) -> dict:
    client = OpenAI()
    response = client.moderations.create(model="omni-moderation-latest", input=script)
    result = response.results[0]
    return {"flagged": result.flagged, "categories": result.categories.model_dump()}
