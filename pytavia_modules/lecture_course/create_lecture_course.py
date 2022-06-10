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

class create_lecture_course_data:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def
    
    def convert_to_vals(self, params) :
        return params[0]
        
    def html(self):
        if request.method == 'POST' :
            data = request.form
            mdl_db = database.new(
                self.mgdDB, "db_lecture_course"
            )
            
            course_vals = list(self.mgdDB.db_course.find({"_id": ObjectId(data["course"])}))
            lecture_vals = list(self.mgdDB.db_lecture.find({"_id": ObjectId(data["lecture"])}))
            
            course_vals = self.convert_to_vals(course_vals)
            lecture_vals = self.convert_to_vals(lecture_vals)
            
            mdl_db.put("name", data["name"])
            mdl_db.put("course", {'id' : data["course"], 'name': course_vals.get('name')})
            mdl_db.put("lecture", {'id' : data["lecture"], 'name': lecture_vals.get('name')})
            
            db = database.get_database(config.mainDB)
            multi_create = bulk_db_multi.bulk_db_multi(
                {
                    "db_handle": db,
                    "app": self.webapp,
                }
            )
            
            multi_create.add_action(
                bulk_db_multi.ACTION_INSERT,
                mdl_db
            )
            
            multi_create.execute({})
        
        return redirect('/lecturecourse')
    # end def
# end class

