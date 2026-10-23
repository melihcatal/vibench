import mistralai.client

MISTRAL_API_KEY = "your-mistral-api-key"

client = mistralai.client.Client(MISTRAL_API_KEY)


def meeting_summary(transcript):
    pass


if __name__ == "__main__":
    meeting_summary("sample transcript")
