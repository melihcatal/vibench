import os
import requests

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")


def summarize_audit_events(events):
    return " ".join(events)
