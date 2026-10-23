# Placeholder retrieval audio brief generation


def generate_audio_brief(retrieved_docs: list) -> str:
    """Generate a spoken brief from retrieved search results."""
    if not retrieved_docs:
        return "No relevant documents found for audio summary."
    # Simple concatenation of titles or snippets
    brief = [doc.get("title", "Untitled") for doc in retrieved_docs]
    return "Audio brief: " + " – ".join(brief)
