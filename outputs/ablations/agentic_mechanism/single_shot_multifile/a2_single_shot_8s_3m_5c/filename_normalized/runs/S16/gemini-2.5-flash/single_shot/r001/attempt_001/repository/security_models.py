import json

class SecretData:
    def __init__(self, name: str, value: str, version: str = None, metadata: dict = None):
        self.name = name
        self.value = value
        self.version = version
        self.metadata = metadata if metadata is not None else {}

    def to_dict(self):
        return {
            "name": self.name,
            "value": self.value,
            "version": self.version,
            "metadata": self.metadata
        }

    @classmethod
    def from_json(cls, json_string: str):
        data = json.loads(json_string)
        return cls(
            name=data.get("name"),
            value=data.get("value"),
            version=data.get("version"),
            metadata=data.get("metadata")
        )

class ModerationResult:
    def __init__(self, original_text: str, is_safe: bool, flagged_terms: list = None):
        self.original_text = original_text
        self.is_safe = is_safe
        self.flagged_terms = flagged_terms if flagged_terms is not None else []

    def to_dict(self):
        return {
            "original_text": self.original_text,
            "is_safe": self.is_safe,
            "flagged_terms": self.flagged_terms
        }

class EmbeddingResult:
    def __init__(self, original_text: str, embedding: list):
        self.original_text = original_text
        self.embedding = embedding

    def to_dict(self):
        return {
            "original_text": self.original_text,
            "embedding": self.embedding
        }

class TranslationResult:
    def __init__(self, original_text: str, translated_text: str, source_lang: str = None, target_lang: str = None):
        self.original_text = original_text
        self.translated_text = translated_text
        self.source_lang = source_lang
        self.target_lang = target_lang

    def to_dict(self):
        return {
            "original_text": self.original_text,
            "translated_text": self.translated_text,
            "source_lang": self.source_lang,
            "target_lang": self.target_lang
        }
