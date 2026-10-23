from openai import OpenAI
import os

def select_model_resource():
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    models = client.models.list()
    # For this example, we'll just return the ID of the first available model that is a chat completion model
    for model in models.data:
        if "gpt" in model.id:
            return model.id
    return None
