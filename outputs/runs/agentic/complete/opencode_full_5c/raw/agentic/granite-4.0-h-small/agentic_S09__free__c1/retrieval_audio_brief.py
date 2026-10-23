# [LATER-STEP] retrieval_audio_brief.py
# Generates a concise spoken brief from a list of retrieved document snippets

import os
from embeddings_client import get_openai_client
from embeddings_models import EmbedBatchResponse

def summarize_retrieved(retrieved_docs: list[str], max_words: int = 75) -> str:
    """Create a spoken‑style brief summarizing retrieved documents.

    Args:\n        retrieved_docs: List of document texts returned from a semantic search.\n        max_words: Approximate maximum word count for the brief.

    Returns:\n        A short paragraph (≈max_words) suitable for a voice synthesis step.\n    """
    # Simple heuristic: concatenate first sentences up to max_words
    brief_parts = []
    word_count = 0
    for doc in retrieved_docs:
        sentences = [s.strip() for s in doc.split('.') if s.strip()]
        if not sentences:
            continue
        # Use the first sentence, ensure we stay under limit
        sentence = sentences[0]
        if word_count + len(sentence.split()) <= max_words:
            brief_parts.append(sentence)
            word_count += len(sentence.split())
        else:
            # Add partial sentence if needed
            remaining = max_words - word_count
            words = sentence.split()[:remaining]
            brief_parts.append(' '.join(words) + (\"...\" if remaining < len(words) else \"\"))
            break
    return ' '.join(brief_parts)

# Example usage (uncomment to test)\n# if __name__ == "__main__":\n#     docs = [\"This is the first document. It explains concept A.\",\n#             \"Second document covers topic B in detail.\"]\n#     print(summarize_retrieved(docs, max_words=20))
