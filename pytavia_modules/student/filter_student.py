import json
import sys
import traceback
import requests
from yaml import serialize

sys.path.append("pytavia_core"    )
sys.path.append("pytavia_modules" )
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib"  )
sys.path.append("pytavia_storage" )

from flask          import render_template, jsonify
from pytavia_stdlib import idgen
from pytavia_stdlib import utils
from pytavia_core   import database
from pytavia_core   import config
from pytavia_core   import helper
from datetime import datetime
from bson import ObjectId, json_util

class filter_student_data:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    def html(self, student_id):
        student = list(self.mgdDB.db_student.find({'_id': ObjectId(student_id)}, {'id':1, 'name':1, 'major':1}))[0]
        major_id = student['major'].get('id')
        course_ids = list(self.mgdDB.db_course.find({'major.id': major_id}))
        course_list = []
        for course in course_ids :
            course_id = course.get('_id')
            course_list.append(str(course_id))
        lecture_course_ids = list(self.mgdDB.db_lecture_course.find({'course.id': {"$in": course_list}}, {'id':1, 'name': 1}))
        serialize_lecture_course_ids = json.loads(json_util.dumps(lecture_course_ids))
        
        
        return jsonify({'lectureCourses': serialize_lecture_course_ids})
