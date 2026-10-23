from openai import OpenAI

from document_client import load_config


def vendor_text_safety(text):
    config = load_config()
    client = OpenAI(api_key=config.api_key) if config.api_key else OpenAI()
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    result = response.results[0]
    return {"flagged": result.flagged, "categories": result.categories.model_dump()}
