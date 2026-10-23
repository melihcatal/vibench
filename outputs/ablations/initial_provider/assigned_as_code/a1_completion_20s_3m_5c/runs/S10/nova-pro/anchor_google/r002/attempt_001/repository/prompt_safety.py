import openai


def check_prompt_safety(payload):
    response = openai.Moderation.create(input=payload["text"])
    return {"safe": response["results"][0]["flagged"] == False}