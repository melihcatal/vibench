
import os
import openai
from messaging_models import ProcessingResult

def summarize_message_text(text: str, event_id: str) -> ProcessingResult:
    """
    Summarizes the text content of a message using OpenAI's GPT model.

    Args:
        text: The text content from the message payload.
        event_id: The ID of the event being processed.

    Returns:
        A ProcessingResult object with the summary.
    """
    try:
        # The provider is identified by the openai SDK and the model name
        openai.api_key = os.environ["OPENAI_API_KEY"]
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                {"role": "user", "content": f"Please summarize the following text in one sentence: {text}"}
            ],
            max_tokens=60,
            temperature=0.5,
        )
        
        summary = response.choices[0].message.content.strip()
        return ProcessingResult(original_event_id=event_id, status="SUCCESS", summary=summary)

    except openai.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return ProcessingResult(original_event_id=event_id, status="FAILURE", error_message=str(e))
    except Exception as e:
        print(f"An unexpected error occurred during summarization: {e}")
        return ProcessingResult(original_event_id=event_id, status="FAILURE", error_message=str(e))

if __name__ == '__main__':
    # Example Usage:
    # Set the following environment variable before running:
    # export OPENAI_API_KEY="your-openai-api-key"
    
    # message_content = (
    #     "The new system update will be deployed next Tuesday. "
    #     "It includes several security patches and performance improvements. "
    #     "All users should expect a brief period of downtime around 3 AM."
    # )
    # result = summarize_message_text(message_content, "event-456")
    # print(result.to_dict())
    pass
