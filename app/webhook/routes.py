from flask import Blueprint, json, request
from datetime import datetime
from app.extensions import insert_into_mongodb

#Blueprint is used to group routes and related funtions.
#url_prefix is webhook which means any route defines within this webhook should have /webhook prefix to the URL.
webhook = Blueprint('Webhook', __name__, url_prefix = '/webhook')

#Full Url to access /receiver endpoint should be http://localhost:5000/webhook/receiver
@webhook.route('/receiver', methods = ["GET","POST"])
def receiver():
    #Checking if the content type is application/json, which was setup in Github webhook.
    if request.headers["Content-Type"] == 'application/json':
        my_info = request.json

        #Initializing variables with default values, which is to be stored in Mongodb.
        request_id = None
        author = None
        action = None
        from_branch = None
        to_branch = None
        timestamp = None

        #Determining the action type on Github.
        #When Push action is done on Github repo.
        if "pusher" in my_info:
            # Selecting Variables for Mongodb Schema.
            print("this is push action--------------->")
            action = "Push"
            request_id = str(my_info["head_commit"]["id"])
            author = my_info["head_commit"]["author"]["name"]
            #Extract branch name from "ref":"refs/heads/main"
            from_branch = my_info["ref"].split('/')[-1]
            #For push, from_branch and to_branch are the same.
            to_branch = my_info["ref"].split('/')[-1]
            timestamp = my_info["head_commit"]["timestamp"]

        #When Pull action is done on Github repo.
        elif "pull_request" in my_info and my_info["action"] == "opened":
            #Selecting variables for Mongodb Schema.
            #This fields can be selected from looking at the json format of request.json
            print("this is pull request by 2nd user.++++++++++++")
            action = "Pull Request"
            request_id = str(my_info["pull_request"]["id"]) #Selecting PR id
            author = my_info["pull_request"]["user"]["login"]   #Selecting suthor who made pull request
            from_branch = my_info["pull_request"]["head"]["ref"] #from branch
            to_branch = my_info["pull_request"]["base"]["ref"]  #to branch
            timestamp = my_info["pull_request"]["created_at"]

        #When pull request merge is done on Github repo.
        elif "pull_request" in my_info and my_info["action"] == "closed":
            print("this is merge action +===+++====+++++=====")
            action = "Merge"
            author = my_info["pull_request"]["merged_by"]["login"]
            request_id = str(my_info["pull_request"]["merge_commit_sha"])
            #author = my_info["pull_request"]["user"]["login"]
            from_branch = my_info["pull_request"]["head"]["ref"]
            to_branch = my_info["pull_request"]["base"]["ref"]
            timestamp = my_info["pull_request"]["merged_at"]


        #Formatting the date to meet the requirements.
        if timestamp:
            dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S%z")
            day = dt.day
            ordinal_suffix = get_ordinal_suffix(day)
            timestamp = dt.strftime(f"%d{ordinal_suffix} %B %Y - %I:%M %p UTC")

        #print(f"Request ID: {request_id}")
        #Calling insert_into_mongodb function to update the document.
        insert_into_mongodb(request_id, author, action, from_branch, to_branch, timestamp)

        return {}, 200
    #An error when sent payload is not application/json type.
    return {"message": "Invalid Content-Type / no JSON payload"}, 400

#Helper function to add ordinal suffix to the day
def get_ordinal_suffix(day):
    if 10 <= day % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    return suffix


