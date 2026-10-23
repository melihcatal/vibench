import json

from openai import OpenAI


client = OpenAI()


def check_safety(text):
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    return response.results[0].flagged


def handler(event, context=None):
    text = event.get("text", "") if isinstance(event, dict) else str(event)
    return {"statusCode": 200, "body": json.dumps({"ok": True, "flagged": check_safety(text)})}
