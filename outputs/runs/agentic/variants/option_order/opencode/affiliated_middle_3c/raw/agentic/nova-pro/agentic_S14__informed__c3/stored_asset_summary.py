from mistralai.client import Client


def stored_asset_summary(text):
    client = Client(api_key="your-mistral-api-key")
    response = client.complete(text, model="mistral-large-latest")
    return response.choices[0].text
