import boto3

def translate_payload(payload, target_language='es'):
    client = boto3.client('translate')
    try:
        response = client.translate_text(Text=payload, SourceLanguageCode='auto', TargetLanguageCode=target_language)
        return response['TranslatedText']
    except client.exceptions.InternalServerException as e:
        print(f"Service error: {e}")
        return None
    except client.exceptions.ServiceError as e:
        print(f"Service error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None