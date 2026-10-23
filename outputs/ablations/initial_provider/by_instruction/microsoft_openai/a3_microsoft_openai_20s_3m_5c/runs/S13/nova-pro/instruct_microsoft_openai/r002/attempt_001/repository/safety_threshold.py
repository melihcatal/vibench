import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-05-15'
)

def safety_threshold(text, threshold):
    response = client.moderations.create(
        input=text,
        model='text-moderation-stable'
    )
    flagged_categories = response.results[0].categories
    return sum(flagged_categories.values()) >= threshold