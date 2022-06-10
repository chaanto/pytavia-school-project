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

class get_student_course_data:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    def html(self):
        get_data_student_course = self.mgdDB.db_student_course.find()
        get_lecture_course = self.mgdDB.db_lecture_course.find()
        get_student = self.mgdDB.db_student.find()
        
        student_course_data = list(get_data_student_course)
        lecture_course_data = list(get_lecture_course)
        student_data = list(get_student)
        
        # i think this was conventional way to fetch data
        # still figuring out how to improve
        for student_course in student_course_data :
            student_course['student'] = student_course['student'].get('name')
            student_course['lecture_course'] = student_course['lecture_course'].get('name')
                
        response = helper.response_msg(
            "VIEW_HTML_SUCCESS",
            "VIEW HTML SUCCESS", {},
            "0000"
        )
        try:
            response = render_template(
                '/school_template/index_student_course.html', 
                student_course_datas=student_course_data,
                student_datas=student_data,
                lecture_course_datas=lecture_course_data,
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

