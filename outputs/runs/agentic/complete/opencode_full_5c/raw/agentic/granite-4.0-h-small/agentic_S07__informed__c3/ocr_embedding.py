import os
import json
import boto3
from google.protobuf.json_format import MessageToDict
from models import DocumentResultModel

# Later-step scored file – embed extracted document sections for semantic retrieval
# Uses Amazon Titan Embeddings (Bedrock) as concrete provider via boto3


class OcrEmbedding:
    def __init__(self):
        # Validate AWS Bedrock credentials
        for var in ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_REGION"]:
            if not os.getenv(var):
                raise RuntimeError(f"Missing AWS env var: {var}")
        self.bedrock = boto3.client(
            "bedrock-runtime",
            region_name=os.getenv("AWS_REGION"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

    def embed_text(self, text: str) -> List[float]:
        # Titan Embeddings endpoint: https://docs.aws.amazon.com/bedrock/latest/APIReference/API_TextEmbedding.html
        response = self.bedrock.text_embedding(
            ModelId="amazon.titan-text-premier-v1", Text=text
        )
        embedding_list = MessageToDict(
            response["Embedding"]
        )  # convert protobuf to dict
        # Convert list of numbers to pure Python list
        return (
            list(embedding_list["values"])
            if isinstance(embedding_list.get("values"), list)
            else embedding_list["values"]
        )

    def embed_document(self, doc: DocumentResultModel) -> List[float]:
        # Simple approach: concatenate plain text from all pages
        all_text = (
            ". ".join(page["text"] for page in doc.layout.pages)
            if hasattr(doc.layout, "pages")
            else doc.text
        )
        return self.embed_text(all_text)


if __name__ == "__main__":
    embedder = OcrEmbedding()
    sample = "This is a sample document to demonstrate embedding generation."
    embedding = embedder.embed_text(sample)
    print(f"Embedding vector length: {len(embedding)}")
