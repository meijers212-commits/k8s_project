from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from typing import List, Dict, Optional
from typing import Optional
from bson import ObjectId
from dotenv import load_dotenv
import os


load_dotenv()


host = os.getenv("MONGO_HOST")
mongo_port = os.getenv("MONGO_PORT")
mongo_db = os.getenv("MONGO_DB")


# MongoDB Client Setup
def get_database():
    """
    Initialize and return MongoDB database connection.
    Uses local MongoDB instance by default.
    """
    try:
        # Connection string - modify if your MongoDB is hosted elsewhere
        client = MongoClient(
            f"mongodb://{host}:{mongo_port}/", serverSelectionTimeoutMS=5000
        )

        # Test the connection
        client.admin.command("ping")
        print("✓ Successfully connected to MongoDB!")

        # Return the database
        db = client[mongo_db]
        return db

    except ConnectionFailure as e:
        print(f"✗ Failed to connect to MongoDB: {e}")
        print("Make sure MongoDB is running on localhost:27017")
        return None


class Datainteractor:

    @staticmethod
    def create_contact(contact_data: dict) -> str:
        db = get_database()
        contacts_db = db["contacts"] if db is not None else None
        if contacts_db.find_one({"phone_number": contact_data["phone_number"]}):
            raise ValueError("A contact with this phone number already exists")
        if contacts_db is None:
            raise RuntimeError("Contact database is not available")
        result = contacts_db.insert_one(contact_data)
        return str(result.inserted_id)

    @staticmethod
    def get_all_contacts() -> List[Dict]:
        db = get_database()
        contacts_db = db["contacts"] if db is not None else None
        if contacts_db is None:
            return []

        contacts = []
        for contact in contacts_db.find():
            contact["_id"] = str(contact["_id"])
            contacts.append(contact)
        return contacts

    @staticmethod
    def update_contact(contact_id: str, contact_data: dict) -> bool:
        db = get_database()
        contacts_db = db["contacts"] if db is not None else None
        pone_number = contact_data["pone_number"]
        if pone_number and contacts_db.find_one({"pone_number": pone_number}):
            raise ValueError("A contact with this phone number already exists")
        if contacts_db is None:
            return False
        result = contacts_db.update_one(
            {"_id": ObjectId(contact_id)}, {"$set": contact_data}
        )
        return result.matched_count > 0

    @staticmethod
    def delete_contact(contact_id: str) -> bool:
        db = get_database()
        contacts_db = db["contacts"] if db is not None else None
        if contacts_db is None:
            return False
        result = contacts_db.delete_one({"_id": ObjectId(contact_id)})
        return result.deleted_count > 0


class ContactHandling:
    def __init__(self, first_name: str, last_name: str, phone_number: str):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number

    def convert_to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
        }
