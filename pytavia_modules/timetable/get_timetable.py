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

class get_timetable_data:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    def html(self):
        get_data = self.mgdDB.db_timetable.find().sort("created_at")
        get_data_lecture_course = self.mgdDB.db_lecture_course.find().sort("created_at")
        
        timetable_data = list(get_data)
        lecture_course_data = list(get_data_lecture_course)
        
        # i think this was conventional way to fetch data
        # still figuring out how to improve
        for timetable in timetable_data :
            timetable['lecture_course'] = timetable['lecture_course'].get('name')
            timetable['lecture'] = timetable['lecture'].get('name')
            timetable['course'] = timetable['course'].get('name')
                
        response = helper.response_msg(
            "VIEW_HTML_SUCCESS",
            "VIEW HTML SUCCESS", {},
            "0000"
        )
        try:
            response = render_template(
                '/school_template/index_timetable.html', 
                timetable_datas=timetable_data,
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

