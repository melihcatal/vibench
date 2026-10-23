from google.cloud import language_v1
from typing import List, Dict

def check_unsafe_text(project_id: str, texts_to_check: List[str]) -> Dict[str, List[str]]:
    client = language_v1.LanguageServiceClient()
    
    unsafe_annotations = {}

    for text in texts_to_check:
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = client.moderate_text(request={"document": document})
        
        categories = []
        for category in response.moderation_categories:
            categories.append(f"{category.name}: {category.score}")
        
        if categories:
            unsafe_annotations[text] = categories
            
    return unsafe_annotations