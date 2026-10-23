from identity_client import IdentityClient


def profile_moderation(profile_text: str):
    client = IdentityClient.from_env()
    return client.post("/moderations", {"model": "omni-moderation-latest", "input": profile_text})
