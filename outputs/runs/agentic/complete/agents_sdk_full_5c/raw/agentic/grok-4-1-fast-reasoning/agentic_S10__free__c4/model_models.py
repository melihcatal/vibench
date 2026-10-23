def build_summarize_prompt(text: str) -> str:
    return f"""Summarize the following text concisely:

{text}

Summary:"""

def build_qa_prompt(context: str, question: str) -> str:
    return f"""Using only the provided context, answer the question.

Context:
{context}

Question: {question}

Answer:"""

def build_extract_prompt(text: str, instructions: str) -> str:
    return f"""Extract the information as JSON following these instructions:

{instructions}

Text:
{text}

Respond with only valid JSON:"""

def build_completion_prompt(prompt: str) -> str:
    return prompt
