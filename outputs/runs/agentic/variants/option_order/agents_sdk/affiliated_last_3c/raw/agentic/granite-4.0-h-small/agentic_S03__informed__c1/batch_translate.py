import os
import concurrent.futures
from google.cloud import translate_v2 as translate

def translate_text(text, target_language='es'):
    client = translate.Client()
    return client.translate(text, target_language=target_language)['translatedText']

def batch_translate(texts, target_language='es'):
    # Preserve order of input list
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(translate_text, t, target_language) for t in texts]
        return [f.result() for f in futures]

if __name__ == '__main__':
    sample_texts = ["Hello", "World", "How are you?"]
    print(batch_translate(sample_texts, 'fr'))