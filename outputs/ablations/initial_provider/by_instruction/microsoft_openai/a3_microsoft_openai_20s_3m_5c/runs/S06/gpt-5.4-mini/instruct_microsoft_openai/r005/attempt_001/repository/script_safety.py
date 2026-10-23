from speech_client import safety_client


def check_script_safety(text):
    response = safety_client().moderations.create(model="omni-moderation-latest", input=text)
    return response.results[0]
