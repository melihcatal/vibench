from google.cloud import language_v2

def check_platform_output_safety(text_content: str, project_id: str):
    client = language_v2.LanguageServiceClient()
    document = language_v2.Document(content=text_content, type_=language_v2.Document.Type.PLAIN_TEXT)
    
    # Sending a moderation request to the Google Cloud Natural Language API
    # Note: As of my last update, direct 'safety' classification for generative AI
    # models is often handled within the genai SDK or Vertex AI itself. 
    # This example uses the general Natural Language API for text moderation.
    response = client.moderate_text(document=document)
    
    safety_attributes = {}
    for category in response.moderation_categories:
        safety_attributes[category.name] = category.score

    # Determine overall safety based on scores (this is a simplified example)
    is_safe = all(score < 0.7 for score in safety_attributes.values()) # Example threshold
    
    return {"is_safe": is_safe, "safety_attributes": safety_attributes}
