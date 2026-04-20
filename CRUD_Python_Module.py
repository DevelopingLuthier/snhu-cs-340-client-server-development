# Example Python Code to Insert a Document 

from pymongo import MongoClient 
from bson.objectid import ObjectId 

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self, user: str, password: str, host: str, port: int, database: str, collection: str): 
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 
        # 
        # You must edit the password below for your environment. 
        # 
        # Connection Variables 
        # 
        USER = user # 'aacuser' 
        PASS = password # 'aGoodPassword!' 
        HOST = host 
        PORT = port 
        DB = database 
        COL = collection 
        # 
        # Initialize Connection 
        # 
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT)) 
        self.database = self.client['%s' % (DB)] 
        self.collection = self.database['%s' % (COL)] 

    # Create a method to return the next available record number for use in the create method
    def getNextRecordNumber(self) -> int:
        # get last rec_num by sorting in descending order
        last_record = self.database.animals.find_one({}, sort=[('rec_num', -1)])
        # if there are no records, make next rec_num 1
        next_record_number = 1 if last_record is None else last_record['rec_num'] + 1
        return next_record_number
            
    # Complete this create method to implement the C in CRUD. 
    def create(self, data: dict) -> bool:
        if data is None:
            raise Exception("Nothing to save, because data parameter is empty")
        if type(data) is not dict:  # data should be dictionary
            raise Exception("Data must be in key/value (dictionary) format")
        
        data['rec_num'] = self.getNextRecordNumber() # ensures that next rec_num is used
        insert_result = self.database.animals.insert_one(data)
        return insert_result.acknowledged

    # Create method to implement the R in CRUD.
    def read(self, data: dict) -> list | bool:
        if data is None:
            raise Exception("Nothing to read, data parameter is empty")
                            
        cursor = self.database.animals.find(data)  # gets all documents matching key/value pair
        results = list(cursor)  # converts cursor object to list
        return results if results else False  # returns results if they exist
    
    # Create method to implement the U in CRUD.
    def update(self, lookupData: dict, updateData: dict) -> int:
        if lookupData is None or updateData is None:
            raise Exception("Nothing to update, both parameters are required")
        if type(lookupData) is not dict or type(updateData) is not dict:  # data should be dictionary
            raise Exception("Data must be in key/value (dictionry) format")
            
        update_result = self.database.animals.update_many(lookupData, {"$set": updateData})
        return update_result.modified_count  # returns number of records updated
    
    # Create method to implement the D in CRUD.
    def delete(self, lookupData:dict) ->int:
        if lookupData is None:
            raise Exception("Nothing to delete, data parameter is empty")
        if type(lookupData) is not dict:
            raise Exception("Lookup data must be in key/value (dictionary) format")
            
        delete_result = self.database.animals.delete_many(lookupData)
        return delete_result.deleted_count  # returns number of records deleted
