import os
from openai import OpenAI
from model_client import get_openai_client
from model_models import ChatResponse


def stream_platform_generation(prompt: str, model_id: str = "gpt-4o"):
    """
    Stream output from OpenAI's managed model platform while preserving provider response objects.
    """
    client = get_openai_client()

    try:
        stream = client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000,
            stream=True,
        )

        full_response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                full_response += content

                # Yield both the content chunk and the raw chunk object
                yield {
                    "content": content,
                    "raw_chunk": chunk,
                    "model": chunk.model if hasattr(chunk, "model") else model_id,
                    "finish_reason": chunk.choices[0].finish_reason
                    if chunk.choices[0].finish_reason
                    else None,
                }

        # After streaming completes, create a summary response
        final_response = ChatResponse(
            content=full_response,
            model=model_id,
            usage=None,  # Usage not available in streaming mode
            raw_response={"streamed": True, "model": model_id},
        )

        yield {"final": True, "response": final_response, "full_content": full_response}

    except Exception as e:
        raise Exception(f"Failed to stream from OpenAI model {model_id}: {str(e)}")
