import json

from identity_client import comprehend_client


def onboarding_summary(state: str):
    client = comprehend_client()
    return client.detect_syntax(Text=state, LanguageCode="en")
