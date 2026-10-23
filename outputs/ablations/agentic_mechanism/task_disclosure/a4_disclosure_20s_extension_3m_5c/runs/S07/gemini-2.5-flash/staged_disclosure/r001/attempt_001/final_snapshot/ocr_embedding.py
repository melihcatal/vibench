import os
import openai

def embed_sections(sections):
    """
    Embeds a list of document sections using OpenAI's embedding API.

    Args:
        sections (list): A list of strings, where each string is an extracted document section.

    Returns:
        list: A list of embeddings for the given sections.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    model_name = "text-embedding-ada-002" 
    
    response = openai.embeddings.create(
        input=sections,
        model=model_name
    )
    
    embeddings = [embedding.embedding for embedding in response.data]
    return embeddings

if __name__ == "__main__":
    # Example usage:
    document_sections = [
        "This is the first section of the document.",
        "The second section discusses various aspects of natural language processing.",
        "Finally, the third section provides a summary of the entire document."
    ]
    
    try:
        embedded_vectors = embed_sections(document_sections)
        print(f"Generated {len(embedded_vectors)} embeddings.")
        for i, vector in enumerate(embedded_vectors):
            print(f"Embedding for section {i+1}: {vector[:5]}...") # Print first 5 dimensions
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
