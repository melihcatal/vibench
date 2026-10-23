import dashscope

# DashScope Qwen API
# Set your API key in the environment variable DASHSCOPE_API_KEY


def answer_with_context(context: str, question: str) -> str:
    """Answer a question using provided context with DashScope Qwen model."""
    client = dashscope.ChatCompletion()
    response = client.chat(
        model="qwen",
        messages=[
            {"role": "user", "content": f"{context}\n\n{question}"},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    context = "Context information goes here..."
    question = "What is the answer?"
    print(answer_with_context(context, question))
