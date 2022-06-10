import json
import sys
import traceback
from matplotlib.pyplot import title
import requests
from datetime import datetime

sys.path.append("pytavia_core"    )
sys.path.append("pytavia_modules" )
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib"  )
sys.path.append("pytavia_storage" )

from flask          import render_template
from flask          import request
from flask          import url_for
from flask          import redirect
from pytavia_stdlib import idgen
from pytavia_stdlib import utils
from pytavia_core   import database
from pytavia_core   import config
from pytavia_core   import helper
from pytavia_core   import bulk_db_multi
from bson import ObjectId
import operator

class update_lecture_course_data:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def
        
    def html(self, lecture_course_id):
        if request.method == 'POST' :
            data = request.form
            
            course_vals = list(self.mgdDB.db_course.find({"_id": ObjectId(data["course"])}, {'_id': 1, 'name': 1}))[0]
            lecture_vals = list(self.mgdDB.db_lecture.find({"_id": ObjectId(data["lecture"])}, {'_id': 1, 'name': 1}))[0]
            
            NAME = data['name']
            LECTURE = lecture_vals
            COURSE = course_vals
        
            self.mgdDB.db_student_course.update_many(
                {"lecture_course.id" : lecture_course_id}, 
                {"$set" : {
                    'lecture_course.name' : NAME
                }})
            
            self.mgdDB.db_timetable.update_many(
                {'lecture_course.id': lecture_course_id},
                {"$set": {
                    'lecture_course.name' : NAME,
                    'course.name': COURSE.get('name'),
                    'lecture.name': LECTURE.get('name'),
                }}
            )
            
            query = {"_id" : ObjectId(lecture_course_id)}
            set_query = {
                "$set" : {
                    "name" : NAME,
                    "lecture": LECTURE,
                    "course": COURSE,
                }
            }
            self.mgdDB.db_lecture_course.update_one(query, set_query)
            
        return redirect('/lecturecourse')
    # end def
# end class

