from.safety_client import get_client

def create_moderation_request(text):
    client = get_client()
    return client.moderations.create(
        input=text,
        model='text-moderation-stable'
    )

def parse_moderation_response(response):
    return response.results[0].categories