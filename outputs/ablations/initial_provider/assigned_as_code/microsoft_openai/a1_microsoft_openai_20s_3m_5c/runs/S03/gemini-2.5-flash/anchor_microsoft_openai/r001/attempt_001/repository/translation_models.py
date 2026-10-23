from typing import List, Dict, Any

class TranslationRequest:
    def __init__(self, text: str, source_language: str, target_language: str):
        self.text = text
        self.source_language = source_language
        self.target_language = target_language

    def to_azure_input(self) -> List[Dict[str, str]]:
        return [{'Text': self.text}]

class BatchTranslationRequest:
    def __init__(self, texts: List[str], source_language: str, target_language: str):
        self.texts = texts
        self.source_language = source_language
        self.target_language = target_language

    def to_azure_input(self) -> List[Dict[str, str]]:
        return [{'Text': text} for text in self.texts]

class TranslationResponse:
    def __init__(self, azure_response: List[Dict[str, Any]], source_language: str, target_language: str):
        self.translated_text = azure_response[0]['translations'][0]['text'] if azure_response and azure_response[0].get('translations') else ""
        self.source_language = source_language
        self.target_language = target_language

class BatchTranslationResponse:
    def __init__(self, azure_response: List[Dict[str, Any]], source_language: str, target_language: str):
        self.translated_texts = [
            item['translations'][0]['text'] 
            for item in azure_response 
            if item.get('translations')
        ]
        self.source_language = source_language
        self.target_language = target_language

class MarkupTranslationRequest:
    def __init__(self, html_content: str, source_language: str, target_language: str):
        self.html_content = html_content
        self.source_language = source_language
        self.target_language = target_language

    def to_azure_input(self) -> List[Dict[str, str]]:
        return [{'Text': self.html_content}]

class DictionaryTranslationRequest:
    def __init__(self, dictionary: Dict[str, str], source_language: str, target_language: str):
        self.dictionary = dictionary
        self.source_language = source_language
        self.target_language = target_language
    
    def to_azure_input(self) -> List[Dict[str, str]]:
        return [{'Text': value} for value in self.dictionary.values()]


