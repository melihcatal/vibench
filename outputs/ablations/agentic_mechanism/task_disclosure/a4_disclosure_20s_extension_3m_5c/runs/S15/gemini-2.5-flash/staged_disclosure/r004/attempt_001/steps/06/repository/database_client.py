from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class DatabaseClient:
    def __init__(self, connection_string: str, db_name: str):
        self.connection_string = connection_string
        self.db_name = db_name
        self.client = None
        self.db = None

    def connect(self):
        try:
            self.client = MongoClient(self.connection_string)
            self.client.admin.command('ping')
            self.db = self.client[self.db_name]
            print("Successfully connected to MongoDB Atlas!")
        except ConnectionFailure as e:
            print(f"Could not connect to MongoDB Atlas: {e}")
            self.client = None
            self.db = None
        except Exception as e:
            print(f"An unexpected error occurred during connection: {e}")
            self.client = None
            self.db = None

    def close(self):
        if self.client:
            self.client.close()
            print("MongoDB Atlas connection closed.")
        else:
            print("No active connection to close.")

    def get_collection(self, collection_name: str):
        if self.db:
            return self.db[collection_name]
        else:
            print("Not connected to a database. Call connect() first.")
            return None

    def insert_one(self, collection_name: str, document: dict):
        collection = self.get_collection(collection_name)
        if collection:
            try:
                result = collection.insert_one(document)
                return result.inserted_id
            except Exception as e:
                print(f"Error inserting document: {e}")
                return None
        return None

    def find_one(self, collection_name: str, query: dict):
        collection = self.get_collection(collection_name)
        if collection:
            try:
                return collection.find_one(query)
            except Exception as e:
                print(f"Error finding document: {e}")
                return None
        return None

    def update_one(self, collection_name: str, query: dict, update: dict):
        collection = self.get_collection(collection_name)
        if collection:
            try:
                result = collection.update_one(query, {"$set": update})
                return result.modified_count
            except Exception as e:
                print(f"Error updating document: {e}")
                return None
        return None

    def delete_one(self, collection_name: str, query: dict):
        collection = self.get_collection(collection_name)
        if collection:
            try:
                result = collection.delete_one(query)
                return result.deleted_count
            except Exception as e:
                print(f"Error deleting document: {e}")
                return None
        return None

if __name__ == "__main__":
    # This is a placeholder for your MongoDB Atlas connection string.
    # Replace <username>, <password>, <cluster-url>, and <db-name> with your actual credentials.
    # It is recommended to load this from environment variables or a secure configuration system.
    MONGO_CONNECTION_STRING = "mongodb+srv://<username>:<password>@<cluster-url>/<db-name>?retryWrites=true&w=majority"
    DATABASE_NAME = "mydatabase" # Replace with your database name

    client = DatabaseClient(MONGO_CONNECTION_STRING, DATABASE_NAME)
    client.connect()

    if client.db:
        # Example Usage:
        users_collection = client.get_collection("users")
        if users_collection:
            # Insert a document
            new_user = {"name": "John Doe", "email": "john.doe@example.com"}
            inserted_id = client.insert_one("users", new_user)
            if inserted_id:
                print(f"Inserted user with ID: {inserted_id}")

            # Find a document
            found_user = client.find_one("users", {"name": "John Doe"})
            if found_user:
                print(f"Found user: {found_user}")

            # Update a document
            modified_count = client.update_one("users", {"name": "John Doe"}, {"email": "john.d@example.com"})
            if modified_count:
                print(f"Updated {modified_count} user(s).")

            # Delete a document
            deleted_count = client.delete_one("users", {"name": "John Doe"})
            if deleted_count:
                print(f"Deleted {deleted_count} user(s).")

    client.close()
