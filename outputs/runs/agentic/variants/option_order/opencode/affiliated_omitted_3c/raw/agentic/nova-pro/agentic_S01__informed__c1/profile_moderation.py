from watsonx_ai import TextModerationClient


def moderate_profile_text(text):
    client = TextModerationClient(api_key="your_api_key", project_id="your_project_id")
    response = client.moderate(text)
    return response.moderation_result
