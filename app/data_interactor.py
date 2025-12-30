from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from typing import List, Dict, Optional
from typing import Optional

# MongoDB Client Setup
def get_database():
    """
    Initialize and return MongoDB database connection.
    Uses local MongoDB instance by default.
    """
    try:
        # Connection string - modify if your MongoDB is hosted elsewhere
        client = MongoClient(
            "mongodb://localhost:27017/", serverSelectionTimeoutMS=5000
        )

        # Test the connection
        client.admin.command("ping")
        print("✓ Successfully connected to MongoDB!")

        # Return the database
        db = client["library_db"]
        return db

    except ConnectionFailure as e:
        print(f"✗ Failed to connect to MongoDB: {e}")
        print("Make sure MongoDB is running on localhost:27017")
        return None


# Get database and collection
db = get_database()
books_collection = db["books"] if db is not None else None



class DataInteractor:

    @staticmethod
    def insert_book(
        title: str, author: str, year: int, genre: str, pages: int, available: bool = True
    ) -> str:

        book = {
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "pages": pages,
            "available": available,
        }

        if books_collection is None:
            return ""

        result = books_collection.insert_one(book)
        return f"Inserted ID: {result.inserted_id}"

    @staticmethod
    def insert_multiple_books(books: List[Dict]) -> List[str]:
        # Insert multiple documents

        if books_collection is None:
            return []

        result = books_collection.insert_many(books)
        return result.inserted_ids

    @staticmethod
    def find_all_books() -> List[Dict]:
        """
        Function 3: READ all books from the collection

        Returns:
            List[Dict]: List of all book documents
        """

        if books_collection is None:
            return []
        return list(books_collection.find())

    @staticmethod
    def find_books_by_author(author: str) -> List[Dict]:
        """
        Function 4: READ books by a specific author

        Args:
            author: Author name to search for

        Returns:
            List[Dict]: List of books by the specified author
        """

        if books_collection is None:
            return []

        book_resualt = books_collection.find({"author": author})

        book_l = []

        for book in book_resualt:
            book_l.append(book)

        return book_l

    @staticmethod
    def find_books_by_genre_and_year(genre: str, min_year: int) -> List[Dict]:
        """
        Function 5: READ books by genre published after a certain year

        Args:
            genre: Genre to filter by
            min_year: Minimum publication year (inclusive)

        Returns:
            List[Dict]: List of matching books
        """

        if books_collection is None:
            return []

        return list(books_collection.find({"genre": genre, "year": {"$gte": min_year}}))

    @staticmethod
    def update_book_availability(title: str, available: bool) -> int:
        """
        Function 6: UPDATE a book's availability status

        Args:
            title: Title of the book to update
            available: New availability status

        Returns:
            int: Number of documents modified
        """

        if books_collection is None:
            return 0

        result = books_collection.update_many(
            {"title": title}, {"$set": {"available": available}}
        )

        return result.modified_count

    @staticmethod
    def add_rating_to_book(title: str, rating: float) -> int:
        """
        Function 7: UPDATE - Add a rating field to a book

        Args:
            title: Title of the book
            rating: Rating value (0.0 to 5.0)

        Returns:
            int: Number of documents modified
        """

        if books_collection is None:
            return 0

        result = books_collection.update_one({"title": title}, {"$set": {"rating": rating}})

        return result.modified_count

    @staticmethod
    def increment_pages(title: str, additional_pages: int) -> int:
        """
        Function 8: UPDATE - Increment the page count of a book

        Args:
            title: Title of the book
            additional_pages: Number of pages to add

        Returns:
            int: Number of documents modified
        """

        if books_collection is None:
            return 0

        result = books_collection.update_one(
            {"title": title}, {"$inc": {"pages": additional_pages}}
        )

        return result.modified_count

    @staticmethod
    def delete_book_by_title(title: str) -> int:
        """
        Function 9: DELETE a book by its title

        Args:
            title: Title of the book to delete

        Returns:
            int: Number of documents deleted
        """
        if books_collection is None:
            return 0

        result = books_collection.delete_one({"title": title})
        return result.deleted_count

    @staticmethod
    def delete_books_by_genre(genre: str) -> int:
        """
        Function 10: DELETE all books of a specific genre

        Args:
            genre: Genre of books to delete

        Returns:
            int: Number of documents deleted

        """
        if books_collection is None:
            return 0

        result = books_collection.delete_many({"genre": genre})
        return result.deleted_count





class Contacthandeling:
    def __init__(self, id: Optional[int], first_name: str, last_name: str, phone_number: str):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number

    def convert_to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number
        }

