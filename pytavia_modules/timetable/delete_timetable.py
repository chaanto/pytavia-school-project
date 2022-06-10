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
from bson.objectid import ObjectId

class delete_timetable_data:

    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def
        
    def html(self, timetable_id):
        self.mgdDB.db_timetable.delete_one({"_id" : ObjectId(timetable_id)})

        return redirect('/timetable')
    # end def
# end class

