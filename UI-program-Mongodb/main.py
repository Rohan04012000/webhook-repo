from flask import Flask, render_template, jsonify
from flask_pymongo import PyMongo
from datetime import datetime

app = Flask(__name__)
#Configuring Mongodb URI to connect to Mongodb Atlas Cluster.
app.config["MONGO_URI"] = "mongodb+srv://eng17cs0013adityavardhansingh:wVhZxcosxUQGeLN2@cluster0.emapr.mongodb.net/github_webhook?retryWrites=true&w=majority&appName=Cluster0"
#Initializing Pymongo for mongodb connection.
mongo = PyMongo(app)


#Route for rendering the first index.html page.
@app.route('/')
def index():
    return render_template('index.html')

#Endpoint for fetching latest change to Mongodb collection.
@app.route('/latest_changes')
def latest_changes():
    try:
        #Accessing the 'actions' collections from 'github-webhook' database.
        collection = mongo.db.actions

        #Fetching all entries from 'actions' collection.
        latest_entry_cursor = collection.find()
        latest_entry = list(latest_entry_cursor)  # Convert cursor to list

        #If there is any entry in collection.
        if latest_entry:
            #Get the last entry.
            entry = latest_entry[-1]
            action_message = format_action(entry)
            return jsonify({'message': action_message})
        else:
            return jsonify({'message': 'No data available'})

    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'})


def format_action(entry):
    #Extract author, action, branch names, and timestamp.
    #Select author name, if not found then 'Unknown'.
    author = entry.get('author', 'Unknown')
    action = entry.get('action', 'Unknown')
    from_branch = entry.get('from_branch', '')
    to_branch = entry.get('to_branch', '')
    timestamp = entry.get('timestamp', datetime.now().isoformat())

    #Formatting the message based on the action type = Push, Pull Request, Merge.
    if action == 'Push':
        return f"{author} pushed to {to_branch} on {timestamp}"
    elif action == 'Pull Request':
        return f"{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}"
    elif action == 'Merge':
        return f"{author} merged branch {from_branch} to {to_branch} on {timestamp}"

    # If the action type is unknown, return this message.
    return 'Unknown action'


if __name__ == '__main__':
    #Run the app in debug mode on port 5001 as the webhook code is running on 5000.
    app.run(debug=True, port=5001)
