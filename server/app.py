from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid
import json


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

SCHEDULE = []
id = ""
name = ""
subjects = []
class_titles = []
class_offerings = []
sections = []

with open('../schedules/b82fe23e366a464aae0798c40b67ec53.json') as infile:
    temp = json.load(infile)
    id = temp["id"]
    name = temp["name"]
    SCHEDULE = temp["schedule"]
with open('../data/subjects.json') as infile:
    subjects = json.load(infile)

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/builder', methods=['GET', 'POST'])
def builder_menu():
    if request.method == 'POST':
        if request.get_json().get("goal") == "titles":
            subject = request.get_json().get("subject")
            with open('../data/course_data/' + subject + '.json') as infile:
                class_offerings = json.load(infile)
            class_titles = []
            for c in class_offerings:
                if c["title"] not in class_titles:
                    class_titles.append(c["title"])
            return jsonify({
                'class_titles': class_titles,
                'subject': subject,
                })
        elif request.get_json().get("goal") == "sections":
            class_title = request.get_json().get("classTitle")
            subject = request.get_json().get("subject")
            with open('../data/course_data/' + subject + '.json') as infile:
                class_offerings = json.load(infile)
            sections = []
            for s in class_offerings:
                if s["title"] in class_title:
                    sections.append(s)
            return jsonify({
                'subject': subject,
                'sections': sections
                })
    else: 
        return jsonify({
            'status': 'success',
            'schedule': SCHEDULE,
            'name': name,
            'id': id,
            'subjects': subjects,
        })
        

if __name__ == '__main__':
    app.run()
