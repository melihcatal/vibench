from google.cloud import language_v1


def check_record_safety(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_toxicity(request={"document": document})
    return {"toxicity": response.attribute_scores.get("TOXICITY")}
