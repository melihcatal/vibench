# SAME-SCENARIO: Score user text for unsafe or policy-violating content

from safety_client import get_client


def moderate_text(user_text: str, threshold: float = 0.5) -> bool:
    """Return True if the text is flagged as unsafe.

    Uses OpenAI Moderation endpoint as the concrete safety provider.
    """
    client = get_client()
    response = client.moderations.create(input=user_text)
    # response['results'][0]['flagged'] indicates unsafe content
    return response["results"][0]["flagged"]
