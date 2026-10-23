import os
from openai import OpenAI

def summarize_record(record_content: dict) -> str:
    # Initialize OpenAI client
    # It expects OPENAI_API_KEY environment variable to be set.
    client = OpenAI()

    # Convert the record content to a string for summarization
    text_to_summarize = str(record_content)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # You can choose a different GPT model
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes document records."},  # System prompt for context
                {"role": "user", "content": f"Please summarize the following document record: {text_to_summarize}"}
            ],
            max_tokens=150  # Adjust as needed for desired summary length
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        return f"Error summarizing record: {e}"

if __name__ == "__main__":
    # Example usage
    sample_record = {
        "id": "doc123",
        "title": "Quarterly Financial Report Q3 2026",
        "author": "Jane Doe",
        "date": "2026-09-30",
        "content": "This report details the financial performance of the company for the third quarter of 2026. Key highlights include a 15% increase in revenue compared to the previous quarter, driven by strong sales in the EMEA region. Net profit also saw a significant boost due to cost optimization strategies. The outlook for Q4 remains positive with new product launches planned."
    }

    # Ensure OPENAI_API_KEY environment variable is set.
    if "OPENAI_API_KEY" not in os.environ:
        print("Please set the OPENAI_API_KEY environment variable to run this example.")
    else:
        summary = summarize_record(sample_record)
        print(f"Original Record: {sample_record}\n")
        print(f"Summary: {summary}")
