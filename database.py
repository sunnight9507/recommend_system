from pymongo import MongoClient


def data2db(to_db_data, database, collection):
    client = MongoClient("mongodb://localhost:27017/")
    db = client[database]
    temp_collection = db[collection]
    for data in to_db_data:
        try:
            temp_collection.insert_one(data)
        except:
            print("데이터 추가에 실패했습니다.")
