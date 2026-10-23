def summarize_prompt(text: str, max_words: int = 100) -> str:
    return f"""Summarize the following text in {max_words} words or fewer:

{text}

Provide a concise summary:"""


def extract_json_prompt(text: str, instructions: str) -> str:
    return f"""Extract the information from the text as a JSON object following these instructions:

{instructions}

TEXT:
{text}

Output only valid JSON, no other text."""


def rag_prompt(context: str, question: str) -> str:
    return f"""Answer the question based strictly on the provided context. If the answer cannot be found in the context, respond with "Information not available in context".

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:"""


def completion_prompt(prompt: str) -> str:
    return prompt
