import os
from pymongo import MongoClient

client = MongoClient(os.environ["MONGO_URI"])
db = client["member_credit"]
collection = db["credits"]
