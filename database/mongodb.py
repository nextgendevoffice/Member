from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client['membership_system']

def add_member(member_data):
    return db.members.insert_one(member_data)

def get_member(user_id):
    return db.members.find_one({"user_id": user_id})
