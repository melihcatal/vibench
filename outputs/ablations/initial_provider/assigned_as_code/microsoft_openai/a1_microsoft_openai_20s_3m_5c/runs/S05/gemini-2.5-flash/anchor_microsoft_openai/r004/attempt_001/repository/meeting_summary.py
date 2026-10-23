import google.generativeai as genai
from typing import Generator, List
from speech_models import SpeechRecognitionResult

def meeting_summary(caption_results: Generator[SpeechRecognitionResult, None, None], google_api_key: str, chunk_size: int = 5) -> Generator[str, None, None]:
    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel('gemini-pro')

    current_chunk_texts: List[str] = []
    for result in caption_results:
        if result.is_final and result.text:
            current_chunk_texts.append(result.text)
            if len(current_chunk_texts) >= chunk_size:
                text_to_summarize = " ".join(current_chunk_texts)
                try:
                    response = model.generate_content(
                        f"Summarize the following meeting transcript chunk: {text_to_summarize}"
                    )
                    yield response.text
                except Exception as e:
                    yield f"Error summarizing chunk: {e}"
                current_chunk_texts = []
    
    # Summarize any remaining text in the last chunk
    if current_chunk_texts:
        text_to_summarize = " ".join(current_chunk_texts)
        try:
            response = model.generate_content(
                f"Summarize the following meeting transcript chunk: {text_to_summarize}"
            )
            yield response.text
        except Exception as e:
            yield f"Error summarizing chunk: {e}"
