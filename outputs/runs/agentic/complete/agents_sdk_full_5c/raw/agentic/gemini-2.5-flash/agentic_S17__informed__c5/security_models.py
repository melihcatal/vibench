from typing import Optional, Dict, Any

class EncryptionRequest:
    """Represents a request for encryption."""
    def __init__(self, plaintext: str, key_id: str, encryption_context: Optional[Dict[str, str]] = None):
        self.plaintext = plaintext
        self.key_id = key_id
        self.encryption_context = encryption_context

class EncryptionResponse:
    """Represents a response from an encryption operation."""
    def __init__(self, ciphertext_blob: bytes, key_id: str, arn: Optional[str] = None):
        self.ciphertext_blob = ciphertext_blob
        self.key_id = key_id
        self.arn = arn

class DecryptionRequest:
    """Represents a request for decryption."""
    def __init__(self, ciphertext_blob: bytes, key_id: Optional[str] = None, encryption_context: Optional[Dict[str, str]] = None):
        self.ciphertext_blob = ciphertext_blob
        self.key_id = key_id
        self.encryption_context = encryption_context

class DecryptionResponse:
    """Represents a response from a decryption operation."""
    def __init__(self, plaintext: str, key_id: str, arn: Optional[str] = None):
        self.plaintext = plaintext
        self.key_id = key_id
        self.arn = arn

class KeyInfo:
    """Represents summary information about a KMS key."""
    def __init__(self, key_id: str, arn: str, enabled: bool, description: Optional[str] = None):
        self.key_id = key_id
        self.arn = arn
        self.enabled = enabled
        self.description = description

class ContentSafetyResult:
    """Represents the result of a content safety check."""
    def __init__(self, text: str, categories_analysis: Dict[str, Any], block_detected: bool, review_recommended: bool):
        self.text = text
        self.categories_analysis = categories_analysis
        self.block_detected = block_detected
        self.review_recommended = review_recommended

class EmbeddingResult:
    """Represents the result of an embedding operation."""
    def __init__(self, text: str, embedding: list[float]):
        self.text = text
        self.embedding = embedding

class TranslationResult:
    """Represents the result of a translation operation."""
    def __init__(self, original_text: str, translated_text: str, source_language: str, target_language: str):
        self.original_text = original_text
        self.translated_text = translated_text
        self.source_language = source_language
        self.target_language = target_language
