import datetime
import random
import sys
import os
import string
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


from sqlalchemy.orm import sessionmaker
from db import init_database




Session_class = sessionmaker(bind=init_database.engine)
Session = Session_class()



def get_qq():
    # 随机获取6位qq号
    nums = string.digits  # 0123456789
    qq = "".join(random.sample(nums, 6))  # 获取6位QQ号
    return qq


def init_data():
    # 初始化数据库
    student1 = init_database.Student(name="Tom", qq=111111)
    student2 = init_database.Student(name="Jack", qq=222222)
    student3 = init_database.Student(name="Jason", qq=333333)
    student4 = init_database.Student(name="Ben", qq=444444)
    student5 = init_database.Student(name="Jone", qq=555555)

    teacher1 = init_database.Teacher(name="Mr.Li")
    teacher2 = init_database.Teacher(name="Mr.Ma")
    teacher3 = init_database.Teacher(name="Mr.Alex")

    subject1 = init_database.Subject(name="Linux")
    subject2 = init_database.Subject(name="Python")
    subject3 = init_database.Subject(name="Django")
    #创建关系表的数据。
    subject1.student=[student1,student2]
    subject2.student=[student1,student2,student3]




    study_record1 = init_database.StudyRecord(
        subject= subject1, student =student1,teacher=teacher1, day='day1',status=1,score=70)
    study_record2 = init_database.StudyRecord(
        subject= subject1, student =student2,teacher=teacher1, day='day1',status=1,score=75)
    study_record3 = init_database.StudyRecord(
        subject= subject1, student =student1,teacher=teacher1, day='day2',status=1,score=80)
    study_record4 = init_database.StudyRecord(
        subject= subject1, student =student2,teacher=teacher1, day='day2',status=1,score=85)
    study_record5 = init_database.StudyRecord(
        subject= subject1, student =student1,teacher=teacher1, day='day3',status=1,score=65)
    study_record6 = init_database.StudyRecord(
        subject= subject1, student =student2,teacher=teacher1, day='day3',status=1,score=60)


    study_record7 = init_database.StudyRecord(
        subject=subject2, student=student1, teacher=teacher2, day='day1', status=1, score=60)
    study_record8 = init_database.StudyRecord(
        subject=subject2, student=student2, teacher=teacher2, day='day1', status=1, score=50)
    study_record9 = init_database.StudyRecord(
        subject=subject2, student=student3, teacher=teacher2, day='day1', status=1, score=55)
    study_record10 = init_database.StudyRecord(
        subject=subject2, student=student1, teacher=teacher2, day='day2', status=1, score=55)
    study_record11 = init_database.StudyRecord(
        subject=subject2, student=student2, teacher=teacher2, day='day2', status=1, score=45)
    study_record12 = init_database.StudyRecord(
        subject=subject2, student=student3, teacher=teacher2, day='day2', status=1, score=35)







    Session.add_all([student1, student2, student3, student4, student5])
    Session.add_all([teacher1, teacher2, teacher3])
    Session.add_all([subject1, subject2, subject3])
    Session.add_all([study_record1, study_record2, study_record3, \
                     study_record4, study_record5, study_record6, \
                     study_record7, study_record8, study_record9, \
                     study_record10, study_record11, study_record12])

    Session.commit()
    print("数据初始化成功！")

if __name__ == "__main__":
    #运行数据初始化。
    init_data()
    Session.close()