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

# From schedule file
SCHEDULE_FILE = []
id = ""
name = ""
schedule = []
selected_titles = {}

# Temporary
subjects = []
class_titles = []
class_offerings = []
sections = []


with open('../schedules/e298ede66f1e47e8bc5421fdf41dfbbd.json') as infile:
    SCHEDULE_FILE = json.load(infile)
    id = SCHEDULE_FILE["id"]
    name = SCHEDULE_FILE["name"]
    schedule = SCHEDULE_FILE["schedule"]
    selected_titles = SCHEDULE_FILE["selected_titles"]


with open('../data/subjects.json') as infile:
    subjects = json.load(infile)

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/builder', methods=['GET', 'POST'])
def builder_menu():

    if request.method == 'POST':
        # Post Dropdown #1: retrieve all unique titles related to subject
        # No json updates, simply temporary updates
        if request.get_json().get("goal") == "getTitles":
            # Load all classes related to subject
            subject = request.get_json().get("subject")
            with open('../data/course_data/' + subject + '.json') as infile:
                class_offerings = json.load(infile)

            # Add unique class titles to class_titles
            class_titles = []
            for c in class_offerings:
                if c["title"] not in class_titles:
                    class_titles.append(c["title"])
            return jsonify({
                'class_titles': class_titles,
                'subject': subject,
                })

        # Post Dropdown #2: Retrieve all sections/classes that match the title
        # Update schedule file to include selected class title + sections
        # Add
        elif request.get_json().get("goal") == "getSections":
            # Retrieve class title & subject
            class_title = request.get_json().get("classTitle")
            subject = request.get_json().get("subject")
            with open('../data/course_data/' + subject + '.json') as infile:
                class_offerings = json.load(infile)
            
            # Subset of all classes - contains all sections that match title 
            # ie: for ELEM FRENCH I - FREN 101 -> course numbers 10372 & 16432
            sections = []
            for s in class_offerings:
                if s["title"] == class_title:
                    sections.append(s)
            SCHEDULE_FILE["selected_titles"][class_title] = sections
            print(SCHEDULE_FILE["selected_titles"])
            print(id)
            write_json(SCHEDULE_FILE, 'e298ede66f1e47e8bc5421fdf41dfbbd')
            return jsonify({
                'subject': subject,
                'sections': sections
                })

    else: 
        return jsonify({
            'schedule': schedule,
            'name': name,
            'id': id,
            'subjects': subjects,
            'selected_titles': selected_titles
        })

def write_json(data, file_id):
    with open('../schedules/' + file_id + '.json','w') as f: 
        json.dump(data, f) 
        

if __name__ == '__main__':
    app.run()
