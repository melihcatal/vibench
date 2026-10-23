import openai
import os

def summarize_document(document_content: str) -> str:
    """
    Summarizes the given document content using the OpenAI API.

    Args:
        document_content: The full text content of the document to summarize.

    Returns:
        A summarized version of the document.
    """
    # Ensure the OpenAI API key is set as an environment variable
    # Example: export OPENAI_API_KEY="your_api_key_here"
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = openai.OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o-mini", # Concrete external provider identifiable in code
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes documents concisely."},
            {"role": "user", "content": f"Please summarize the following document:

{document_content}"}
        ]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    # Example Usage:
    sample_document = """
    Artificial intelligence (AI) is intelligence—perceiving, synthesizing, and inferring information—demonstrated by machines, as opposed to intelligence displayed by animals or humans. Example tasks in which AI is used include speech recognition, computer vision, translation between (natural) languages, and other mappings of inputs.

    AI applications include advanced web search engines (e.g., Google Search), recommendation systems (used by YouTube, Amazon, and Netflix), understanding human speech (such as Siri and Alexa), self-driving cars (e.g., Waymo), generative AI (e.g., ChatGPT and other large language models), and competing at the highest level in strategic game systems (such as chess and Go).
    """
    summary = summarize_document(sample_document)
    print("Document Summary:")
    print(summary)
