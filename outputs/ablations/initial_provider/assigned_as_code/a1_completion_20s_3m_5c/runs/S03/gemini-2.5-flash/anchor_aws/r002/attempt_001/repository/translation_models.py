def normalize_payload(payload):
    # Basic normalization for text translation
    return {
        "Text": payload["text"],
        "SourceLanguageCode": payload["source_language"],
        "TargetLanguageCode": payload["target_language"],
    }


def parse_translation_response(response, original_payload):
    return {
        "text": response["TranslatedText"],
        "source_language": original_payload["SourceLanguageCode"],
        "target_language": original_payload["TargetLanguageCode"],
    }

def normalize_batch_payload(payloads):
    # For batch translation, payloads will be a list of dictionaries
    # Each dictionary should have 'text', 'source_language', 'target_language'
    return [
        {
            "Text": p["text"],
            "SourceLanguageCode": p["source_language"],
            "TargetLanguageCode": p["target_language"],
        }
        for p in payloads
    ]

def parse_batch_translation_response(responses, original_payloads):
    translated_texts = []
    for i, response in enumerate(responses):
        translated_texts.append(
            {
                "text": response["TranslatedText"],
                "source_language": original_payloads[i]["SourceLanguageCode"],
                "target_language": original_payloads[i]["TargetLanguageCode"],
            }
        )
    return translated_texts
