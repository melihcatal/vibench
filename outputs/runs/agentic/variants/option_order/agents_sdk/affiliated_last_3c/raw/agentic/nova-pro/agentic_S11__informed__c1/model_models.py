from azure.ai.textanalytics import TextDocumentInput

def create_text_input(text):
    return TextDocumentInput(id='1', text=text)
