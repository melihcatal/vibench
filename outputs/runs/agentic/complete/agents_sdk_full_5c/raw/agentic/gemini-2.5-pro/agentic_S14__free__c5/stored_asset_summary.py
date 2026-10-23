import os
import cohere

def summarize_asset_text(text: str) -> str | None:
    """
    Summarizes text content using the Cohere Summarize API.

    This function requires the COHERE_API_KEY environment variable to be set.

    Args:
        text: The text content extracted from a stored asset.

    Returns:
        A string containing the summary, or None if an error occurred.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        print("Error: COHERE_API_KEY environment variable not set.")
        return None

    try:
        co = cohere.Client(api_key)
        
        # Using the command-r-plus model for summarization
        response = co.summarize(
            text=text,
            model='command-r-plus',
            length='medium',
            format='paragraph',
        )
        
        return response.summary

    except cohere.core.api_error.ApiError as e:
        print(f"Cohere API error: {e}")
        return None

# Example Usage
# if __name__ == '__main__':
#     # Text presumably extracted from a stored document
#     document_text = (
#         "The solar system is a gravitationally bound system of the Sun and the "
#         "objects that orbit it. Of the bodies that orbit the Sun directly, the "
#         "largest are the four gas giants and four terrestrial planets, followed "
#         "by an unknown number of dwarf planets and innumerable small Solar System "
#         "bodies. The solar system formed 4.6 billion years ago from the gravitational "
#         "collapse of a giant interstellar molecular cloud."
#     )
    
#     summary = summarize_asset_text(document_text)
#     if summary:
#         print("--- Original Text ---")
#         print(document_text)
#         print("\n--- Cohere Summary ---")
#         print(summary)
