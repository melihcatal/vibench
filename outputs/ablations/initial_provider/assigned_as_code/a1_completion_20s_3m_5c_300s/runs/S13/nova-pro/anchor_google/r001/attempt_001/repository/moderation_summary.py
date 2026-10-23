import os

import requests


def moderation_summary(decisions):
    toxicity_scores = [decision["toxicity"] for decision in decisions]
    average_toxicity = sum(toxicity_scores) / len(toxicity_scores)
    return {"average_toxicity": average_toxicity}