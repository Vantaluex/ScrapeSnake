# mongo_connection_class.py
import os

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


class MongoDBConnection:
    """
    A class to manage a single MongoDB connection.

    This class provides methods to connect, close, and access databases/collections,
    ensuring a singleton-like behavior for the connection within its instance.
    It can also be used as a context manager for automatic connection closing.
    """

    def __init__(self, uri=None):
        """
        Initializes the MongoDBConnection instance.

        Args:
            uri (str, optional): The MongoDB connection URI. If None, it attempts
                                 to get it from the MONGODB_URI environment variable.

        Raises:
            ValueError: If the URI is not provided and MONGODB_URI env var is not set.
        """
        self._client = None
        self._uri = uri if uri is not None else os.environ.get("MONGODB_URI")

        if not self._uri:
            raise ValueError(
                "MongoDB URI not provided and MONGODB_URI environment variable not set."
            )

    def connect(self):
        """
        Establishes and returns the MongoDB client connection.
        If a connection already exists, it returns the existing one.

        Raises:
            ConnectionError: If MongoDB connection fails.
            RuntimeError: For other unexpected connection errors.

        Returns:
            pymongo.MongoClient: The connected MongoDB client instance.
        """
        if self._client is None:
            try:
                self._client = MongoClient(self._uri)
                # The ismaster command is cheap and does not require auth.
                # It helps confirm the connection is active.
                self._client.admin.command("ismaster")
                print("MongoDB client connected successfully.")
            except ConnectionFailure as e:
                self._client = None
                raise ConnectionError(f"MongoDB connection failed: {e}") from e
            except Exception as e:
                self._client = None
                raise RuntimeError(
                    f"An unexpected error occurred during MongoDB connection: {e}"
                ) from e
        return self._client

    def close(self):
        """
        Closes the MongoDB client connection if it is active.
        """
        if self._client:
            self._client.close()
            self._client = None
            print("MongoDB client closed.")

    def get_database(self, db_name="sample_mflix"):
        """
        Retrieves a database object from the connected client.

        Args:
            db_name (str, optional): The name of the database. Defaults to "sample_mflix".

        Returns:
            pymongo.database.Database: The requested MongoDB database object.
        """
        client = self.connect()  # Ensure client is connected before getting database
        return client.get_database(db_name)

    # Example: Add a specific collection accessor if needed
    def get_movies_collection(self):
        """
        Retrieves the 'movies' collection from the 'sample_mflix' database.

        Returns:
            pymongo.collection.Collection: The 'movies' collection.
        """
        db = self.get_database("sample_mflix")
        return db.get_collection("movies")

    # --- Context Manager Protocol ---
    def __enter__(self):
        """
        Connects to MongoDB when entering a 'with' statement.
        """
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Closes the MongoDB connection when exiting a 'with' statement.
        """
        self.close()
