import boto3
import embeddings

cw_logs = boto3.client("logs", region_name="us-west-2")
embeddings_client = embeddings.Client()

log_group_name = "MyLogGroup"


def embed_log_message(log_message):
    embedding = embeddings_client.embed_text(log_message)
    return embedding


if __name__ == "__main__":
    log_message = "This is a sample log message."
    embedding = embed_log_message(log_message)
    print(embedding)
