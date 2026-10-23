import json


def summarize_onboarding_state(state):
    return json.dumps(state, indent=2)