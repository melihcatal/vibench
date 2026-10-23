class OCRResponse:
    def __init__(self, blocks):
        self.blocks = blocks


class TranslatedText:
    def __init__(self, text):
        self.text = text


class SafetyCheckResult:
    def __init__(self, is_safe):
        self.is_safe = is_safe


class ExtractedFields:
    def __init__(self, fields):
        self.fields = fields


class DocumentEmbedding:
    def __init__(self, embedding):
        self.embedding = embedding
