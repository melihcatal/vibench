class ExtractedText:
    def __init__(self, text_content: str):
        self.text_content = text_content

class ExtractedLayout:
    def __init__(self, pages: list):
        self.pages = pages

class ExtractedTable:
    def __init__(self, num_rows: int, num_columns: int, header_rows: list, body_rows: list):
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.header_rows = header_rows
        self.body_rows = body_rows

class TableCell:
    def __init__(self_obj, text_content: str, row_span: int = 1, col_span: int = 1):
        self_obj.text_content = text_content
        self_obj.row_span = row_span
        self_obj.col_span = col_span

class KeyValuePair:
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value

class ExtractedKeyValues:
    def __init__(self, key_value_pairs: list[KeyValuePair]):
        self.key_value_pairs = key_value_pairs

class TranslatedText:
    def __init__(self, translated_content: str, detected_language_code: str = None):
        self.translated_content = translated_content
        self.detected_language_code = detected_language_code

class SafetyScore:
    def __init__(self, category: str, score: float):
        self.category = category
        self.score = score

class DocumentSafety:
    def __init__(self, safety_scores: list[SafetyScore]):
        self.safety_scores = safety_scores

class ExtractedField:
    def __init__(self, name: str, value: str, entity_type: str = None):
        self.name = name
        self.value = value
        self.entity_type = entity_type

class DocumentFields:
    def __init__(self, fields: list[ExtractedField]):
        self.fields = fields

class TextEmbedding:
    def __init__(self, embedding_vector: list[float]):
        self.embedding_vector = embedding_vector

class DocumentEmbeddings:
    def __init__(self, embeddings: list[TextEmbedding]):
        self.embeddings = embeddings
