from flask_pymongo import PyMongo

# Setup mongo here.
mongo = PyMongo()

def insert_into_mongodb(request_id, author, action, from_branch, to_branch, timestamp):
    try:
        #Access the 'actions' collection in the 'github_webhook' database
        collection = mongo.db.actions
        #Creating the document to insert
        document = {
            "request_id": request_id,
            "author": author,
            "action": action,
            "from_branch": from_branch,
            "to_branch": to_branch,
            "timestamp": timestamp
        }

        # Insert the document into the actions collection.
        result = collection.insert_one(document)
        return f"Document inserted"
    except: #Exception as e:
        #print("Something went wrong in Database file")
        return f"An error occurred:"
