from pymongo import MongoClient

# Replace with your MongoDB Atlas connection string
# Example: "mongodb+srv://<username>:<password>@<cluster-name>.mongodb.net/?retryWrites=true&w=majority"
MONGO_CONNECTION_STRING = "YOUR_MONGODB_ATLAS_CONNECTION_STRING" 

class DatabaseClient:
    def __init__(self):
        if not MONGO_CONNECTION_STRING or MONGO_CONNECTION_STRING == "YOUR_MONGODB_ATLAS_CONNECTION_STRING":
            raise ValueError("MongoDB connection string not configured. Please update MONGO_CONNECTION_STRING.")
        self.client = MongoClient(MONGO_CONNECTION_STRING)
        self.db = self.client.get_database() # You can specify a database name here, e.g., self.client.my_database

    def get_collection(self, collection_name: str):
        return self.db[collection_name]

    def close_connection(self):
        self.client.close()

# Example usage (can be removed or modified based on actual needs)
if __name__ == "__main__":
    try:
        db_client = DatabaseClient()
        # Access a collection
        # users_collection = db_client.get_collection("users")
        # print("Successfully connected to MongoDB Atlas and got 'users' collection.")
        # db_client.close_connection()
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
