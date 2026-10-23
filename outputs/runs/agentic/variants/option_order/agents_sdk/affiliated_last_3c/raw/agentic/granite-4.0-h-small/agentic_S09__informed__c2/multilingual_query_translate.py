from googletrans import Translator
from embeddings_client import embeddings_client
from embeddings_models import normalize_embedding

def translate_query(query: str, target_lang: str = "en"):
    """Translate a query string before multilingual embedding search."""
    translator = Translator()
    translated = translator.translate(query, dest=target_lang).text
    return translated

# Example: embed multilingual query after translation
# translated_query = translate_query("查询中文文档")
# query_embedding, _ = embed_for_search(translated_query, documents)
