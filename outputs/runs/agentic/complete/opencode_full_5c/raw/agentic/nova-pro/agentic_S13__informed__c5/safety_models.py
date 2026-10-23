from azure.ai.contentsafety.models import TextContent, Category


def create_text_content(text):
    return TextContent(content=text)


def create_category(text, severity):
    return Category(text=text, severity=severity)
