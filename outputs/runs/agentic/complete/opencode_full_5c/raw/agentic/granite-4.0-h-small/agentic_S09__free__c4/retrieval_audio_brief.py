def generate_spoken_brief(retrieved_results: list[dict]) -> str:
    """Create a short spoken summary from retrieved search results.
    Each result is expected to have a 'title' and 'snippet' field.
    The brief emphasizes key points for audio consumption.
    """
    if not retrieved_results:
        return "No relevant results found."
    brief_parts = []
    for i, item in enumerate(retrieved_results, start=1):
        title = item.get("title", "Untitled")
        snippet = item.get("snippet", "")
        brief_parts.append(f"{i}. {title}: {snippet}")
    # Keep the brief concise (first 3 items)
    return " ".join(brief_parts[:3])
