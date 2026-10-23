from deep import DeepLClient
from security_models import TranslationRequest, normalize_text

client = DeepLClient()
request = TranslationRequest(text='Rotate the secret, wait for propagation, then validate downstream connections.', target_language='DE')
print(client.translate_text(normalize_text(request.text), target_lang=request.target_language))
