from pymongo import MongoClient
import pprint as pp
client = MongoClient()

db = client.test_database

# collection = db.test_collection

dat = db.posts.find_one()

pp.pprint(dat)
