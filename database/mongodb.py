from pymongo import MongoClient
from config import MONGO_URI
import uuid

client = MongoClient(MONGO_URI)
db = client["membership_system"]


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
    db.credits.update_one(
        {"user_id": user_id}, {"$inc": {"amount": amount}}, upsert=True
    )


def adjust_credit(user_id, amount):
    db.credits.update_one(
        {"user_id": user_id}, {"$inc": {"amount": amount}}, upsert=True
    )


def create_withdrawal_request(user_id, amount):
    request_id = str(uuid.uuid4())
    withdrawal_request = {
        "request_id": request_id,
        "user_id": user_id,
        "amount": amount,
        "status": "pending",
    }
    db.withdrawal_requests.insert_one(withdrawal_request)
    return request_id


def get_withdrawal_requests(status=None, user_id=None):
    query = {}
    if status:
        query["status"] = status
    if user_id:
        query["user_id"] = user_id
    return list(db.withdrawal_requests.find(query))

def get_withdrawal_request(request_id):
    result = withdrawal_requests_collection.find_one({"request_id": request_id})
    return result


def approve_withdrawal_request(request_id):
    request = db.withdrawal_requests.find_one({"request_id": request_id})
    if request and request["status"] == "pending":
        update_withdrawal_request_status(request_id, "approved")
        return True
    return False


def reject_withdrawal_request(request_id):
    request = db.withdrawal_requests.find_one({"request_id": request_id})
    if request and request["status"] == "pending":
        user_id = request["user_id"]
        amount = request["amount"]
        update_withdrawal_request_status(request_id, "rejected")
        deposit_credit(user_id, amount)
        return True
    return False


def update_withdrawal_request_status(request_id, status):
    db.withdrawal_requests.update_one(
        {"request_id": request_id}, {"$set": {"status": status}}
    )


def get_user_withdrawal_requests(user_id):
    return list(db.withdrawal_requests.find({"user_id": user_id}))
