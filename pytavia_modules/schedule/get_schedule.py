import json
import sys
import traceback
import requests

sys.path.append("pytavia_core"    )
sys.path.append("pytavia_modules" )
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib"  )
sys.path.append("pytavia_storage" )

from flask          import render_template
from pytavia_stdlib import idgen
from pytavia_stdlib import utils
from pytavia_core   import database
from pytavia_core   import config
from pytavia_core   import helper
from datetime import datetime
from bson import ObjectId

class get_schedule_data:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def
    
    def dict_merge(dict1, dict2):
        res = {**dict1, **dict2}
        return res

    def html(self):
        get_data_timetable = self.mgdDB.db_timetable.find().sort("date")
        get_data_student_course = self.mgdDB.db_student_course.find().sort("name")
        
        timetable_vals = list(get_data_timetable)
        student_course_vals = list(get_data_student_course)
        
        
        for timetable in timetable_vals :
            timetable_id = timetable['lecture_course'].get('id')
            for student_course in student_course_vals :
                student_id = student_course['lecture_course'].get('id')
                if student_id == timetable_id :
                    if not timetable.get('student') :
                        timetable.update({'student': [student_course['student'].get('name')]})
                    else :
                        student = timetable.get('student')
                        student.append(student_course['student'].get('name'))
                
            timetable['lecture_course'] = timetable['lecture_course'].get('name')
            timetable['course'] = timetable['course'].get('name')
            timetable['lecture'] = timetable['lecture'].get('name')
                
        response = helper.response_msg(
            "VIEW_HTML_SUCCESS",
            "VIEW HTML SUCCESS", {},
            "0000"
        )
        try:
            response = render_template(
                '/school_template/index.html', 
                schedule_datas=timetable_vals,
            )
        except :
            print(traceback.format_exc())
            response.put( "status"      ,  "VIEW_HTML_FAILED" )
            response.put( "desc"        ,  "GENERAL ERROR" )
            response.put( "status_code" ,  "9999" )
        # end try
        return response
    # end def
# end class

