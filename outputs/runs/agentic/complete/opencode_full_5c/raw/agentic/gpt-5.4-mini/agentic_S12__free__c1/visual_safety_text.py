from openai import OpenAI
from vision_client import OPENAI_API_HOST, OPENAI_API_KEY


client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_HOST)


def visual_safety_text(labels):
    prompt = f"Check these labels for unsafe or sensitive text and return a concise risk note: {labels}"
    resp = client.responses.create(model="gpt-4o-mini", input=prompt)
    return resp.output_text
