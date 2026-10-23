import os
from model_client import ManagedModelClient
from model_models import ModelInvocationRequest, InvocationResponse
from google.cloud.translate_v2 import Translator  # concrete Google Cloud Translation client

def localized_platform_output(output: InvocationResponse, target_locale: str = 'es') -> str:
    """
    Translates the model's generated text into the requested locale using Google Cloud Translation.
    """
    translator = Translator()
    src_text = output.generated_text
    # Translation API returns a list; we take the first translation
    translated = translator.translate(src_text, target_language=target_locale)['translatedText']
    return translated

if __name__ == '__main__':
    client = ManagedModelClient()
    req = ModelInvocationRequest(
        model='projects/{}/locations/{}/publishers/google/models/gemma'.format(
            os.getenv('GOOGLE_CLOUD_PROJECT'), os.getenv('GCLOUD_LOCATION', 'us-central1')
        ),
        parameters={'temperature': 0.7},
        messages=[{'role': 'user', 'content': 'Describe the sunset in poetic terms.'}],
    )
    resp = client.invoke(req)
    es_text = localized_platform_output(resp, target_locale='es')
    print('Original:', resp.generated_text)
    print('Spanish translation:', es_text)
