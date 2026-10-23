from identity_client import post_json


def profile_moderation(text: str) -> dict:
    return post_json("/moderations", {"model": "omni-moderation-latest", "input": text})
