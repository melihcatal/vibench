import os

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def get_client():
    return {
        "api_key": PERSPECTIVE_API_KEY,
    }


def normalize_response(response):
    return response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
