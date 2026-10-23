from mistralai import Client

client = Client(api_key="YOUR_MISTRAL_API_KEY")


def summarize_error_logs(logs):
    response = client.chat.completions.create(
        model="mistral-large-latest",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes error logs.",
            },
            {"role": "user", "content": logs},
        ],
    )
    return response.choices[0].message.content
