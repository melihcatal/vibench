from google.cloud import translate_v2 as translate

import os


def invoice_summary(extracted_fields):
    client = translate.Client()
    result = client.translate(extracted_fields["total"], target_language="en")
    return result["translatedText"]
