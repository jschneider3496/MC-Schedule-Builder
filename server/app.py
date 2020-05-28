from flask import Flask, jsonify, request
from flask_cors import CORS
from random_word import RandomWords
import json, os, uuid

r = RandomWords()

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# From schedule file
# SCHEDULE_FILE = {}
# with open('../schedules/e298ede66f1e47e8bc5421fdf41dfbbd.json') as infile:
#     SCHEDULE_FILE = json.load(infile)

# Temporary
subjects = []
class_titles = []
class_offerings = []
sections = []

def get_schedules():
    schedules = []
    for entry in os.scandir('../schedules/'):
        temp = []
        with open(entry.path) as infile:
            temp = json.load(infile)
        schedules.append(temp)
    return schedules

def get_schedule_file(id):
    with open('../schedules/' + id + '.json') as infile:
        return json.load(infile)

with open('../data/subjects.json') as infile:
    subjects = json.load(infile)

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/schedules', methods=['GET'])
def return_schedules():
    return jsonify({"schedules": get_schedules()})

@app.route('/create', methods=['GET'])
def create_schedule():
    id = uuid.uuid4().hex
    name = (str(r.get_random_word() + " " + r.get_random_word())).upper()
    temp = {
        'id': id,
        'name': name,
        'schedule': [],
        'selected_titles': {},
        'subjects': []
    }
    write_json(temp, id)
    return jsonify({"schedule_file": get_schedule_file(id)})

@app.route('/builder/<schedule_id>', methods=['GET','POST','PUT'])
def builder_menu(schedule_id):
    SCHEDULE_FILE = get_schedule_file(schedule_id)
    if request.method == 'PUT':
        payload = request.get_json().get("payload")
        goal = request.get_json().get("goal")
        if goal == 'updateSchedule':
            SCHEDULE_FILE["schedule"] = payload
            write_json(SCHEDULE_FILE, schedule_id)
        if goal == 'removeSelectedTitle':
            SCHEDULE_FILE = remove_sections(payload, SCHEDULE_FILE)
            SCHEDULE_FILE["selected_titles"].pop(payload)
            write_json(SCHEDULE_FILE, schedule_id)
        return jsonify({"status": "success"})

    elif request.method == 'POST':
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
            write_json(SCHEDULE_FILE, schedule_id)
            return jsonify({
                'subject': subject,
                'sections': sections
                })

    elif request.method == "GET": 
        return jsonify({
            'schedule': SCHEDULE_FILE["schedule"],
            'name': SCHEDULE_FILE["name"],
            'id': SCHEDULE_FILE["id"],
            'subjects': subjects,
            'selected_titles': SCHEDULE_FILE["selected_titles"]
        })

def remove_sections(title, SCHEDULE_FILE):
    for s in SCHEDULE_FILE["schedule"]:
        if title == s['title']:
            SCHEDULE_FILE["schedule"].remove(s)
    return SCHEDULE_FILE

# Update schedule file with new data
def write_json(data, file_id):
    with open('../schedules/' + file_id + '.json','w') as f: 
        json.dump(data, f) 
        

if __name__ == '__main__':
    app.run()
