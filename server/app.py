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
            'class_offerings': class_offerings
            })
    else: 
        return jsonify({
            'status': 'success',
            'schedule': SCHEDULE,
            'name': name,
            'id': id,
            'subjects': subjects,
        })
        


# @app.route('/builder/<builder_id>', methods = ['GET', 'POST'])
# def builder_menu():
#     response_object = {'status': 'success'}
#     if request.method == 'POST':
#         post_data = request.get_json()
#         BOOKS.append({
#             'id': uuid.uuid4().hex,
#             'title': post_data.get('title'),
#             'author': post_data.get('author'),
#             'read': post_data.get('read')
#         })
#         write_json(BOOKS)
#         response_object['message'] = 'Book added!'
#     else:
#         response_object['books'] = BOOKS
#     return jsonify(response_object)
if __name__ == '__main__':
    app.run()
