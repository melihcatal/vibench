import os
from openai import OpenAI
from select_platform_resource import select_platform_resource

def check_output_safety(text: str):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        organization=os.environ.get("OPENAI_ORGANIZATION_ID"),
    )
    moderation_model = select_platform_resource(model_type="moderation")
    response = client.moderations.create(input=text, model=moderation_model)
    result = response.results[0]
    return result.flagged, result.categories.model_dump()
