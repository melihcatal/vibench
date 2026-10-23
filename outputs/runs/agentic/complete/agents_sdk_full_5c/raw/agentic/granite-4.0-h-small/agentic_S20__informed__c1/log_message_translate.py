import os
import json
from ibm_watsonx_ai import WatsonxApi

# Initialize Watsonx client (uses WATSONX_API_KEY and WATSONX_PROJECT_ID env vars)
watsonx = WatsonxApi()

def translate_log_message(log_entry: dict, target_locale: str = 'fr') -> str:
    """Translates the 'message' field of a log entry to the specified locale using watsonx.ai.

    Args:
        log_entry (dict): Log payload containing a 'message' key.
        target_locale (str): Locale code (e.g., 'fr', 'es').
    Returns:
        Translated message string.
    """
    payload = {
        'messages': [
            {
                'role': 'user',
                'content': [
                    {'language': 'en', 'text': log_entry.get('message', '')}
                ]
            }
        ],
        'model': 'ibm/granite-7b-v2',
        'max_tokens': 256
    }
    # Send to watsonx for translation (simple prompt-based pattern)
    response = watsonx.chat.completions.create(
        system=f"Translate the text from English to {target_locale}.",
        messages=[{'role': 'user', 'content': log_entry.get('message', '')}],
        model='ibm/granite-7b-v2'
    )
    # The response structure varies; extract first assistant message text
    translated = response.choices[0].message.content
    return str(translated)

# Demo (remove in production)
if __name__ == '__main__':
    entry = {'message': 'Error connecting to database'}
    print('Translated:', translate_log_message(entry, 'fr'))
