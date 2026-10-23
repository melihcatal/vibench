from typing import List, Dict, Any

Message = Dict[str, str]


def build_prompt_for_summarize(text: str) -> List[Message]:
    return [
        {
            "role": "system",
            "content": "You are a helpful assistant that creates concise and accurate summaries of text.",
        },
        {"role": "user", "content": text},
    ]


def build_prompt_for_extract_json(text: str) -> List[Message]:
    return [
        {
            "role": "system",
            "content": "You are a world class JSON extractor. Always respond with only valid JSON matching the expected structure. No other text.",
        },
        {
            "role": "user",
            "content": f"Extract structured data as JSON from this text:\n\n{text}",
        },
    ]


def build_prompt_for_answer(context: str, question: str) -> List[Message]:
    return [
        {
            "role": "system",
            "content": "You are a helpful assistant. Use the context to answer the question accurately. If the context does not contain the answer, say so.",
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {question}\nAnswer:",
        },
    ]


def build_prompt_for_completion(prompt: str) -> List[Message]:
    return [{"role": "user", "content": prompt}]
