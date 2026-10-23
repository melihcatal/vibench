from typing import List
from deepl import TextResult

def extract_text(result: TextResult) -&gt; str:
    return result.text

def extract_texts(results: List[TextResult]) -&gt; List[str]:
    return [r.text for r in results]
