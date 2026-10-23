import os
import requests
from messaging_client import get_azure_content_moderator_config
from messaging_models import EventMessage

def check_message_safety(message: EventMessage) -> dict:
    endpoint, subscription_key = get_azure_content_moderator_config()
    text_to_check = str(message.payload)

    text_moderation_url = f"{endpoint}/contentmoderator/moderate/v1.0/ProcessText/FullText?classify=true"
    
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-Type': 'text/plain'
    }

    try:
        response = requests.post(text_moderation_url, headers=headers, data=text_to_check.encode('utf-8'))
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "message": "Failed to connect to Azure Content Moderator."}
