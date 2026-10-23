import os

# The name of the DynamoDB table, configured via an environment variable.
TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME", "documents")
