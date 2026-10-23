import os
import openai

def embed_text(text_sections):
    """
    Embeds extracted document sections using OpenAI's embedding API.

    Args:
        text_sections (list): A list of strings, where each string is an
                              extracted document section.

    Returns:
        list: A list of embeddings, where each embedding is a list of floats.
    """
    # Make sure to set your OpenAI API key as an environment variable
    # For example: export OPENAI_API_KEY="your_api_key_here"
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    response = openai.embeddings.create(
        input=text_sections,
        model="text-embedding-ada-002" # Concrete model identifier
    )

    embeddings = [data.embedding for data in response.data]
    return embeddings

if __name__ == "__main__":
    # Example Usage:
    sections = [
        "This is the first section of the document.",
        "Here is some information about semantic retrieval.",
        "The quick brown fox jumps over the lazy dog."
    ]

    try:
        document_embeddings = embed_text(sections)
        for i, embedding in enumerate(document_embeddings):
            print(f"Embedding for section {i+1}: {embedding[:5]}...") # Print first 5 dimensions
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
