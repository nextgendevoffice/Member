from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client['membership_system']

def add_member(member_data):
    return db.members.insert_one(member_data)

def get_member(user_id):
    return db.members.find_one({"user_id": user_id})

def get_credit(user_id):
    credit = db.credits.find_one({"user_id": user_id})
    return credit["amount"] if credit else 0

def withdraw_credit(user_id, amount):
    credit = db.credits.find_one({"user_id": user_id})
    if not credit or credit["amount"] < amount:
        return False, 0

    db.credits.update_one({"user_id": user_id}, {"$inc": {"amount": -amount}})
    return True, credit["amount"] - amount

def deposit_credit(user_id, amount):
    db.credits.update_one({"user_id": user_id}, {"$inc": {"amount": amount}}, upsert=True)
    
def adjust_credit(user_id, amount):
    db.credits.update_one({"user_id": user_id}, {"$inc": {"amount": amount}}, upsert=True)