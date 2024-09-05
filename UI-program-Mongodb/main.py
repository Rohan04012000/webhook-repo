from flask import Flask, render_template, jsonify
from flask_pymongo import PyMongo
from datetime import datetime

app = Flask(__name__)
app.config[
    "MONGO_URI"] = "mongodb+srv://eng17cs0013adityavardhansingh:wVhZxcosxUQGeLN2@cluster0.emapr.mongodb.net/github_webhook?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/latest_changes')
def latest_changes():
    try:
        collection = mongo.db.actions

        #latest_entry_cursor = collection.find().sort('timestamp', -1).limit(1)
        latest_entry_cursor = collection.find()
        latest_entry = list(latest_entry_cursor)  # Convert cursor to list

        if latest_entry:
            #entry = latest_entry[0]
            entry = latest_entry[-1]
            action_message = format_action(entry)
            return jsonify({'message': action_message})
        else:
            return jsonify({'message': 'No data available'})

    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'})


def format_action(entry):
    author = entry.get('author', 'Unknown')
    action = entry.get('action', 'Unknown')
    from_branch = entry.get('from_branch', '')
    to_branch = entry.get('to_branch', '')
    timestamp = entry.get('timestamp', datetime.now().isoformat())

    if action == 'Push':
        return f"{author} pushed to {to_branch} on {timestamp}"
    elif action == 'Pull Request':
        return f"{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}"
    elif action == 'Merge':
        return f"{author} merged branch {from_branch} to {to_branch} on {timestamp}"
    return 'Unknown action'


if __name__ == '__main__':
    app.run(debug=True, port=5001)
