from database_client import get_database_and_container
import os

def query_documents(database_name: str, container_name: str, query: str, parameters: list = None):
    container = get_database_and_container(database_name, container_name)
    if parameters is None:
        parameters = []
    
    # The query_items method returns an iterator, which we convert to a list for easier handling.
    response = list(container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True  # Enable if querying across multiple partitions
    ))
    return response

if __name__ == "__main__":
    database_name = os.environ.get("COSMOS_DB_DATABASE_NAME", "YourDatabaseName")
    container_name = os.environ.get("COSMOS_DB_CONTAINER_NAME", "YourContainerName")

    # Example query: find documents where 'value' field is greater than 100
    sample_query = "SELECT * FROM c WHERE c.value > @value_param"
    sample_parameters = [{'name': '@value_param', 'value': 100}]

    try:
        documents = query_documents(database_name, container_name, sample_query, sample_parameters)
        print(f"Queried documents: {documents}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
