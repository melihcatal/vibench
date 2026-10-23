from google.cloud import language_v1


def vendor_text_safety(payload, config=None):
    client = language_v1.ModerationServiceClient()
    response = client.moderate_text(
        request={"parent": f"projects/{(config or {}).get('project_id', '')}/locations/global", "text": payload["text"]}
    )
    return {"categories": [item.category for item in response.moderation_categories]}
