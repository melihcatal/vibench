from typing import List, Dict, Any


def build_summarize_prompt(text: str) -> List[Dict[str, str]]:
    return [
        {
            "role": "system",
            "content": "You are an expert at summarizing text concisely while preserving key information.",
        },
        {"role": "user", "content": f"Please summarize the following text:\n\n{text}"},
    ]


def build_qa_prompt(context: str, question: str) -> List[Dict[str, str]]:
    return [
        {
            "role": "system",
            "content": "You are a helpful assistant. Answer the question based only on the provided context.",
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:",
        },
    ]


def build_extract_json_prompt(text: str, schema: str) -> List[Dict[str, str]]:
    return [
        {
            "role": "system",
            "content": f"You are an expert at extracting structured data. Output only valid JSON matching this schema: {schema}",
        },
        {"role": "user", "content": text},
    ]


def parse_chat_completion(response: Any) -> str:
    return response.choices[0].message.content.strip()
