import dashscope

DASHSCOPE_API_KEY = "your-dashscope-api-key"

client = dashscope.Client(DASHSCOPE_API_KEY)


def caption_embedding(caption):
    pass


if __name__ == "__main__":
    caption_embedding("sample caption")
