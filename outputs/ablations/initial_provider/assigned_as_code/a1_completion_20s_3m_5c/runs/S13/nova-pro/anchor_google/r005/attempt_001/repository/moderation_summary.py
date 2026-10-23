import os

import requests

from safety_client import get_perspective_client


def summarize_moderation_decisions(decisions):
    summary = {
        'allowed': 0,
        'redacted': 0
    }
    for decision in decisions:
        if decision['toxicity'] > 0.5:
            summary['redacted'] += 1
        else:
            summary['allowed'] += 1
    return summary