import boto3

def multilingual_query_translate(query_text, target_language_code, source_language_code="auto", config=None):
    config = config or {}
    client = boto3.client("translate", region_name=config.get("region", "us-east-1"))
    
    if source_language_code == "auto":
        response = client.translate_text(
            Text=query_text,
            TargetLanguageCode=target_language_code,
        )
    else:
        response = client.translate_text(
            Text=query_text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code,
        )
        
    translated_text = response["TranslatedText"]
    return {"translated_query": translated_text, "source_language": response.get("SourceLanguageCode", source_language_code)}
