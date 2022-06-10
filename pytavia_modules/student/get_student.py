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

class get_student_data:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    def html(self):
        get_data = self.mgdDB.db_student.find().sort("created_at")
        get_data_major = self.mgdDB.db_major.find().sort("created_at")
        
        student_data = list(get_data)
        major_data = list(get_data_major)
        
        # i think this was conventional way to fetch data
        # still figuring out how to improve
        for student in student_data :
            student['major'] = student['major'].get('name')
                
        response = helper.response_msg(
            "VIEW_HTML_SUCCESS",
            "VIEW HTML SUCCESS", {},
            "0000"
        )
        try:
            response = render_template(
                '/school_template/index_student.html', 
                student_datas=student_data,
                major_datas=major_data,
                
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

