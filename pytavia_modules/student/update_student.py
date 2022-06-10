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

class update_student_data:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def
        
    def html(self, student_id):
        if request.method == 'POST' :
            data = request.form
            
            major_vals = list(self.mgdDB.db_major.find({"_id": ObjectId(data["major"])}, {'_id': 1, 'name': 1}))[0]
    
            NAME = data['name']
            MAJOR = major_vals
        
            self.mgdDB.db_student_course.update_many(
                {"student.id" : student_id}, 
                {"$set" : {
                    'student.name' : NAME,
                    'major.name': MAJOR.get("name"),
                }})
            
            query = {"_id" : ObjectId(student_id)}
            set_query = {
                "$set" : {
                    "name" : NAME,
                    "major": MAJOR,
                }
            }
            
            self.mgdDB.db_student.update_one(query, set_query)
            
        return redirect('/student')
    # end def
# end class

