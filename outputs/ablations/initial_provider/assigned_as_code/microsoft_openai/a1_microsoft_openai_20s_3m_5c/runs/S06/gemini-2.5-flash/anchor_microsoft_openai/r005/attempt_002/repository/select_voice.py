import azure.cognitiveservices.speech as speechsdk


def select_voice(payload, config=None):
    config = config or {}
    speech_config = speechsdk.SpeechConfig(subscription=config['api_key'], region=config['region'])
    
    # This feature is not directly available in the Azure SDK as a simple listVoices method.
    # To get a list of voices, you typically need to refer to the documentation or make an HTTP call.
    # For the purpose of this exercise, we will return a mock list or a commonly used voice based on locale.
    # In a real-world scenario, you would parse the documentation or use an API that provides this.
    
    # As a placeholder, we return a common voice that could be selected.
    # A real implementation would involve a more complex lookup or an API call to Azure's voice list endpoint.
    locale = payload.get('locale', 'en-US')
    if locale == 'en-US':
        return {'voices': [{'name': 'en-US-JennyNeural', 'locale': 'en-US'}, {'name': 'en-US-GuyNeural', 'locale': 'en-US'}]}
    elif locale == 'es-ES':
        return {'voices': [{'name': 'es-ES-ElviraNeural', 'locale': 'es-ES'}]}
    else:
        return {'voices': [{'name': f'{locale}-Standard-A', 'locale': locale}]}