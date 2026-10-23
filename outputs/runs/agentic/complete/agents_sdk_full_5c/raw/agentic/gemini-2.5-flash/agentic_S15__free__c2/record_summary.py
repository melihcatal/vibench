import os
import google.generativeai as genai

def summarize_document_content(document_content: str, model_name: str = "gemini-pro") -> str:
    """
    Summarizes retrieved document records using Google Cloud Generative AI.
    Requires GOOGLE_API_KEY environment variable to be set.
    """
    try:
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
        model = genai.GenerativeModel(model_name)

        prompt = f"Please provide a concise summary of the following document content:

{document_content}

Summary:"

        response = model.generate_content(prompt)
        summary = response.text.strip()
        print(f"Document summarized successfully. Summary: {summary}")
        return summary
    except KeyError:
        print("Error: GOOGLE_API_KEY environment variable not set.")
        raise
    except Exception as e:
        print(f"Error summarizing document content: {e}")
        raise

if __name__ == '__main__':
    # Example usage
    # os.environ['GOOGLE_API_KEY'] = 'YOUR_GEMINI_API_KEY' # Replace with your actual API key
    # sample_content = (
    #     "The quick brown fox jumps over the lazy dog. "
    #     "This is a classic pangram used to display all the letters of the alphabet. "
    #     "It is often used for testing typefaces and computing equipment."
    # )
    # try:
    #     summary = summarize_document_content(sample_content)
    #     print(f"\nGenerated Summary: {summary}")
    # except Exception as e:
    #     print(f"Could not summarize: {e}")
