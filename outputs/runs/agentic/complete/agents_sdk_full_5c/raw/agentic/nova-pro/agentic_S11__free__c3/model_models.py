from azure.ai.textanalytics import TextDocumentInput

def create_text_document_input(text):
    return TextDocumentInput(id="1", text=text)