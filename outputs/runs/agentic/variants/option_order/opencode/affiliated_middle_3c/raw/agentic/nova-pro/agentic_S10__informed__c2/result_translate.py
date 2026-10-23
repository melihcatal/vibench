from .prompt_safety import client


def check_prompt(text):
    response = client.detect_toxic_content(Text=text, LanguageCode="en")
    return response["ToxicContent"]
