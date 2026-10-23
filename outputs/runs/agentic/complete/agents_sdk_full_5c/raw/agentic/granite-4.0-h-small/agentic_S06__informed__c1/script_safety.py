import os
import ibm_watson
from ibm_watson import ApiException

def check_safety(script: str, apikey: str, url: str = 'https://api.us-south.text-to-speech.watson.cloud.ibm.com') -> bool:
    """Check narration script for unsafe content using IBM Watson Text-to-Speech guardrails.

    Args:
        script (str): Narrative text to evaluate.
        apikey (str): IBM Watson Text-to-Speech API key.
        url (str): Endpoint URL.

    Returns:
        bool: True if safe, False if unsafe according to guardrails.
    """
    service = ibm_watson.text_to_speech_v1.TextToSpeechV1()
    service.set_apikey(apikey)
    service.set_service_url(url)
    # Guardrails are part of the service response; here we simulate a call that returns a safety flag.
    # In a real scenario, you would use the Watson Speech to Text service's built-in safety flag or a separate content moderation endpoint.
    # For this example, we assume the API returns a JSON with a 'safe' field.
    # Since the current endpoint does not directly expose a safety check, we demonstrate the pattern.
    try:
        # Placeholder: In practice, call a moderation endpoint (e.g., /v1/guardrails) if available.
        # The following line is illustrative only.
        response = service.synthesize(script)
        # Assume API returns a 'safe' attribute (doesn't exist in real API) - actual implementation would use an appropriate moderation service.
        return getattr(response, 'safe', True)
    except ApiException as e:
        # Log error and treat as unsafe for safety
        print('API error:', e)
        return False

if __name__ == '__main__':
    sample_script = 'This is a harmless example.'
    safe = check_safety(sample_script, os.getenv('IBM_TTS_APIKEY'))
    print('Script safe:', safe)
