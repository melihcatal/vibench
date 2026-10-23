from typing import List, Dict, Any, Optional
from google.cloud import firestore
from database_client import get_firestore_client
from database_models import Document

def query_documents(collection_name: str, field: str, value: Any) -> List[Document]:
    """Queries documents from a specified Firestore collection by a field value.

    Args:
        collection_name (str): The name of the Firestore collection.
        field (str): The field to query by.
        value (Any): The value to match for the given field.

    Returns:
        List[Document]: A list of Document objects matching the query.
    """
    db = get_firestore_client()
    query = db.collection(collection_name).where(field, "==", value)

    results: List[Document] = []
    try:
        docs = query.stream()
        for doc in docs:
            print(f"Found document: {doc.id} => {doc.to_dict()}")
            results.append(Document.from_firestore_document(doc.id, doc.to_dict()))
        print(f"Query successful: found {len(results)} documents in collection {collection_name} where {field} == {value}.")
    except Exception as e:
        print(f"Error querying documents in collection {collection_name}: {e}")
        raise

    return results

if __name__ == "__main__":
    # Example Usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set or running in a GC environment
    # For local testing, ensure Firestore emulator is running or credentials are set up.
    collection = "products"

    # Create some sample data for querying
    from upsert_document import upsert_document
    print("\nPopulating sample data for query...")
    upsert_document(collection, "prod001", {"name": "Laptop Pro", "category": "Electronics", "price": 1200.00, "available": True})
    upsert_document(collection, "prod002", {"name": "Desktop PC", "category": "Electronics", "price": 1500.00, "available": True})
    upsert_document(collection, "prod003", {"name": "Mechanical Keyboard", "category": "Peripherals", "price": 150.00, "available": False})
    upsert_document(collection, "prod004", {"name": "Gaming Mouse", "category": "Peripherals", "price": 75.00, "available": True})
    upsert_document(collection, "prod005", {"name": "Smartwatch", "category": "Wearables", "price": 300.00, "available": False})


    print("\nQuerying documents where category == 'Electronics'...")
    try:
        electronics_products = query_documents(collection, "category", "Electronics")
        print(f"Electronics products found: {len(electronics_products)}")
        for product in electronics_products:
            print(f" - {product.id}: {product.data.get('name')}")

        print("\nQuerying documents where available == True...")
        available_products = query_documents(collection, "available", True)
        print(f"Available products found: {len(available_products)}")
        for product in available_products:
            print(f" - {product.id}: {product.data.get('name')}")

        print("\nQuerying documents where category == 'Books' (expected none)...")
        books = query_documents(collection, "category", "Books")
        print(f"Books found: {len(books)}")

    except Exception as e:
        print(f"Example usage failed: {e}")
