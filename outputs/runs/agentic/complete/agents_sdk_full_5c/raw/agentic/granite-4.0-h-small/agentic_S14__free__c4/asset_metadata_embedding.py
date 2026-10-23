import os
import boto3
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document
from storage_client import get_s3_client

def create_metadata_embedding_store(bucket_name: str, prefix: str, embedding_model: str = 'text-embedding-ada-002') -> FAISS:
    """Create a FAISS vector store containing embeddings of object metadata and extracted text.

    - Retrieves objects under the given prefix.
    - Uses OpenAI embeddings (or any other provider config).
    - Returns a FAISS vectorstore for similarity search.
    """
    embeddings = OpenAIEmbeddings(model=embedding_model)
    vectorstore = FAISS.load_or_create(embeddings, os.path.join('/tmp', f'{bucket_name}_{prefix}_index'))
    s3 = get_s3_client()
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
        for obj in page.get('Contents', []):
            key = obj['Key']
            # Retrieve simple metadata and assume text content is stored under the same key
            metadata = {
                'key': key,
                'size': obj.get('Size', 0),
                'last_modified': obj.get('LastModified', '').isoformat()
            }
            # For demo, we reuse the object text as supplementary content; replace with OCR/translation results as needed
            text = ''  # TODO: populate via OCR/translation pipelines if needed
            doc = Document(page=text, metadata=metadata)
            vectorstore.add([doc])
    vectorstore.persist(os.path.join('/tmp', f'{bucket_name}_{prefix}_index'))
    return vectorstore