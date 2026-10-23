from identity_client import openai_headers, post_json


def profile_moderation(profile_text: str):
    payload = {"model": "omni-moderation-latest", "input": profile_text}
    return post_json("https://api.openai.com/v1/moderations", payload, headers=openai_headers())
