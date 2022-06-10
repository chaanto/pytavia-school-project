import json
import time
from urllib import response
import pymongo
import sys
import urllib.parse
import base64

sys.path.append("pytavia_core"    ) 
sys.path.append("pytavia_settings") 
sys.path.append("pytavia_stdlib"  ) 
sys.path.append("pytavia_storage" ) 
sys.path.append("pytavia_modules" ) 
sys.path.append("pytavia_modules/rest_api_controller") 

# adding comments
from pytavia_stdlib  import utils
from pytavia_core    import database 
from pytavia_core    import config 
from pytavia_core    import model
from pytavia_stdlib  import idgen 

from rest_api_controller import module1
from lecture import create_lecture, get_lecture, delete_lecture, update_lecture
from major import create_major, get_major, delete_major
from student import create_student, get_student, delete_student, update_student, filter_student
from course import create_course, get_course, delete_course
from lecture_course import create_lecture_course, get_lecture_course, delete_lecture_course, update_lecture_course
from student_course import create_student_course, get_student_course, delete_student_course
from timetable import create_timetable, get_timetable, delete_timetable
from schedule import get_schedule

##########################################################

from flask import request
from flask import render_template
from flask import Flask
from flask import session
from flask import make_response
from flask import redirect
from flask import url_for
from flask import flash


from flask_wtf.csrf import CSRFProtect
from flask_wtf.csrf import CSRFError
#
# Main app configurations
#
app             = Flask( __name__, config.G_STATIC_URL_PATH )
csrf            = CSRFProtect(app)
app.secret_key  = config.G_FLASK_SECRET
app.db_update_context, app.db_table_fks = model.get_db_table_paths(model.db)

########################## CALLBACK API ###################################

# @app.route("/v1/api/api-v1", methods=["GET"])
# def api_v1():
#     params = request.args.to_dict()
#     response = module1.module1(app).process( params )
#     return response.stringify_v1()
# # end def

# @app.route("/v1/api/api-post-v1", methods=["POST"])
# def api_post_v1():
#     params = request.form.to_dict()
#     response = module1.module1(app).process( params )
#     return response.stringify_v1()
# # end def

#Index -> Schedule 
@app.route("/", methods=["GET"])
def index():
    response = get_schedule.get_schedule_data(app).html()
    return response

#Lecture
@app.route("/lecture", methods=["GET"])
def lecture_get():
    response = get_lecture.get_lecture_data(app).html()
    return response

@app.route("/lecture/add", methods=["POST"])
def lecture_add():
    response = create_lecture.create_lecture_data(app).html()
    return response

@app.route("/lecture/delete/<string:lecture_id>")
def lecture_delete(lecture_id):
    response = delete_lecture.delete_lecture_data(app).html(lecture_id)
    return response

@app.route("/lecture/update/<string:lecture_id>", methods=["POST"])
def lecture_update(lecture_id):
    response = update_lecture.update_lecture_data(app).html(lecture_id)
    return response

#Major
@app.route("/major", methods=["GET"])
def major_get():
    response = get_major.get_major_data(app).html()
    return response

@app.route("/major/add", methods=["POST"])
def major_add():
    response = create_major.create_major_data(app).html()
    return response

@app.route("/major/delete/<string:major_id>")
def major_delete(major_id):
    response = delete_major.delete_major_data(app).html(major_id)
    return response

#Student
@app.route("/student", methods=["GET"])
def student_get():
    response = get_student.get_student_data(app).html()
    return response

@app.route("/student/add", methods=["POST"])
def student_add():
    response = create_student.create_student_data(app).html()
    return response

@app.route("/student/delete/<string:student_id>")
def student_delete(student_id):
    response = delete_student.delete_student_data(app).html(student_id)
    return response

@app.route("/student/update/<string:student_id>", methods=["POST"])
def student_update(student_id):
    response = update_student.update_student_data(app).html(student_id)
    return response

@app.route("/student/filter/<string:student_id>", methods=["GET"])
def student_filter(student_id):
    response = filter_student.filter_student_data(app).html(student_id)
    return response

#Course
@app.route("/course", methods=["GET"])
def course_get():
    response = get_course.get_course_data(app).html()
    return response

@app.route("/course/add", methods=["POST"])
def course_add():
    response = create_course.create_course_data(app).html()
    return response

@app.route("/course/delete/<string:course_id>")
def course_delete(course_id):
    response = delete_course.delete_course_data(app).html(course_id)
    return response

#Lecture Course
@app.route("/lecturecourse", methods=["GET"])
def lecture_course_get():
    response = get_lecture_course.get_lecture_course_data(app).html()
    return response

@app.route("/lecturecourse/add", methods=["POST"])
def lecture_course_add():
    response = create_lecture_course.create_lecture_course_data(app).html()
    return response

@app.route("/lecturecourse/delete/<string:lecture_course_id>")
def lecture_course_delete(lecture_course_id):
    response = delete_lecture_course.delete_lecture_course_data(app).html(lecture_course_id)
    return response

@app.route("/lecturecourse/update/<string:lecture_course_id>", methods=["POST"])
def lecture_course_update(lecture_course_id):
    response = update_lecture_course.update_lecture_course_data(app).html(lecture_course_id)
    return response


#Student Course
@app.route("/studentcourse", methods=["GET"])
def student_course_get():
    response = get_student_course.get_student_course_data(app).html()
    return response

@app.route("/studentcourse/add", methods=["POST"])
def student_course_add():
    response = create_student_course.create_student_course_data(app).html()
    return response

@app.route("/studentcourse/delete/<string:student_course_id>")
def student_course_delete(student_course_id):
    response = delete_student_course.delete_student_course_data(app).html(student_course_id)
    return response

#Timetable
@app.route("/timetable", methods=["GET"])
def timetable_get():
    response = get_timetable.get_timetable_data(app).html()
    return response

@app.route("/timetable/add", methods=["POST"])
def timetable_add():
    response = create_timetable.create_timetable_data(app).html()
    return response

@app.route("/timetable/delete/<string:timetable_id>")
def timetable_delete(timetable_id):
    response = delete_timetable.delete_timetable_data(app).html(timetable_id)
    return response



### Sample generic endpoints
"""
# TODO: update example using new db actions
### sample generic archive -- archive book
@app.route("/process/book/archive", methods=["POST"])
def book_proc_archive():
    params = request.form.to_dict()
    response = generic_proc.generic_proc(app).archive({
        "collection"    : "db_book",
        "pkey"          : params["pkey"]
    })

    if response.get('status_code') == config.G_STATUS['SUCCESS']['CODE']:
        return response.http_stringify()
    else:
        return response.http_stringify()

### sample generic restore -- restore book
@app.route("/process/book/restore", methods=["POST"])
def book_proc_restore():
    params = request.form.to_dict()
    response = generic_proc.generic_proc(app).restore({
        "collection"    : "db_book",
        "pkey"          : params["pkey"]
    })

    if response.get('status_code') == config.G_STATUS['SUCCESS']['CODE']:
        return response.http_stringify()
    else:
        return response.http_stringify()

### sample two way reference -- reference book to author and author to book
@app.route("/process/book/add_author", methods=["POST"])
def book_proc_add_author():
    params = request.form.to_dict()
    response = generic_proc.generic_proc(app).add_two_way_reference({
        "main"  : {
            "collection"    : "db_book",
            "pkey"          : params["book_pkey"]
        },  
        "sub"  : {
            "collection"    : "db_author",
            "pkey"          : params["author_pkey"]
        }
    })

    if response.get('status_code') == config.G_STATUS['SUCCESS']['CODE']:
        return response.http_stringify()
    else:
        return response.http_stringify()

### sample remove two way reference -- dereference book to author and vise versa
@app.route("/process/book/remove_group", methods=["POST"])
def book_proc_remove_group():
    params = request.form.to_dict()
    response = generic_proc.generic_proc(app).remove_two_way_reference({
        "main"  : {
            "collection"    : "db_book",
            "pkey"          : params["book_pkey"]
        },  
        "sub"  : {
            "collection"    : "db_author",
            "pkey"          : params["author_pkey"]
        }
    })

    if response.get('status_code') == config.G_STATUS['SUCCESS']['CODE']:
        return response.http_stringify()
    else:
        return response.http_stringify()
"""