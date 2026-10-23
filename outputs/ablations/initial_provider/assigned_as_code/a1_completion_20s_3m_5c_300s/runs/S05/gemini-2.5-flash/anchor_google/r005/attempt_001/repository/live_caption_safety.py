from google.cloud import language_v1

def check_safety(text):
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Classifying content can indicate safety issues
    response = client.classify_text(request={'document': document})
    
    categories = []
    for category in response.categories:
        categories.append({"name": category.name, "confidence": category.confidence})
    
    return categories
