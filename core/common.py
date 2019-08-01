
# 教师，学生，课程通用的方法

import sys
import os
BaseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BaseDir)

from db import init_data
from db import init_database
from db.init_data import Session


def get_student_by_qq(student_qq):
    """通过学生qq获取学生信息"""
    student = Session.query(init_database.Student).filter(
        init_database.Student.qq == student_qq).first()
    return student


def get_subject(subject_name):
    """通过班级名称获取班级信息"""
    subject = Session.query(init_database.Subject).filter(
        init_database.Subject.name == subject_name).first()
    return subject


def get_subject_record(subject_name, student_qq, day):
    """通过班级名称，学生qq，日期获取班级记录"""
    subject = get_subject(subject_name)
    student = get_student_by_qq(student_qq)
    if subject != None and student != None:
        study_record = Session.query(init_database.StudyRecord).filter(
            init_database.StudyRecord.subject == subject,
            init_database.StudyRecord.student == student,
            init_database.StudyRecord.day == day
        ).first()
        return study_record
    else:
        print("学生qq或者科目不存在。")
        return None




