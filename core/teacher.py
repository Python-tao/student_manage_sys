import os
import sys
BASE_DIR = os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) )
sys.path.append(BASE_DIR)


from db import init_data
from db import init_database
from db.init_data import Session
from core import common

class Teacher(object):
    def __init__(self, name):
        self.name = name

    def get_teacher_name(self):
        #根据老师名称获取数据库中的对应的老师的"对象"。
        teacher = Session.query(init_database.Teacher).filter(
            init_database.Teacher.name == self.name).first()
        return teacher

    def get_current_subject(self):
        subject = Session.query(init_database.Subject).filter(
            init_database.Subject.name.like("%")).all()
        return subject

    def add_subject(self, subject_name):
        # 增加课程 成功True， 失败False
        try:
            #创建新课程的对象。
            subject = init_database.Subject(name=subject_name)
            #添加到会话中。
            Session.add(subject)
            #执行。
            Session.commit()
            print("课程{}添加成功！".format(subject_name))
            return True
        except Exception as e:
            print("添加失败！",e)
            return False

    def add_student_to_subject(self, student_qq, subject_name):
        '''
        把学生增加到课程
        :param student_qq: 学员的qq号码。
        :param subject_name: 课程名称。
        :return:
        '''

        student =common.get_student_by_qq(student_qq)
        #获取课程的对象。
        subject = common.get_subject(subject_name)
        if student is not None and subject is not None:
            try:
                #调用对象的relationship后使用append添加学生对象。
                subject.student.append(student)
                Session.commit()
                print("学员{}添加到{}成功。".format(student.name,subject.name))
                return True
            except Exception as e:
                print("添加失败！", e)
                return False
        else:
            print("学员QQ号或者课程不存在。")

    def get_current_teacher(self):
        #获取当前已有的老师列表。
        teachers = Session.query(init_database.Teacher).filter(
            init_database.Teacher.name.like("%")).all()
        return teachers


    def add_study_record(self, subject_name):
        '''
        增加课程记录

        :param subject_name: 课程名称。
        :return:
        '''
        #获取课程对象。
        subject=common.get_subject(subject_name)
        #获取当前已有的老师的列表。
        teachers=self.get_current_teacher()
        #获取报了该课程的学生列表。
        students = subject.student
        #获取该课程的旧学习记录。
        old_records=Session.query(init_database.StudyRecord).filter(
                init_database.StudyRecord.subject == subject
            ).order_by(init_database.StudyRecord.day.asc()).all()
        new_records = []
        if len(old_records)==0:
            print("这是全新课程")

            for t in teachers:
                print("id:{} | 姓名:{}".format(teachers.index(t),t.name))
            print("请输入此课程的老师:")
            choice=input(">>")
            #选择一个负责此课程的老师。
            target_teacher=teachers[int(choice)]

            for student in students:
                #创建新课程记录。
                study_record=init_database.StudyRecord(subject=subject,\
                student=student,teacher=target_teacher,day="day1",status=1,homework_status='No',score=0)
                new_records.append(study_record)
            Session.add_all(new_records)
            Session.commit()
            print("课程:{}增加了{}的学习记录。".format(subject_name,study_record.day))

        else:
            print("这是进行中的课程")
            print("目前最新的上课记录为:")
            for item in old_records:
                print(item)
            #获取新的上课记录对应的节次。
            target_day="day"+str(int(old_records[-1].day.split('day')[-1])+1)
            #获取负责该课程的老师的对象。
            target_teacher=old_records[-1].teacher
            choice=input("是否需要增加{}的上课记录：".format(target_day))
            if choice=="y" or choice== "Y":
                for student in students:
                    #创建课程记录。
                    study_record = init_database.StudyRecord(subject=subject, \
                     student=student, teacher=target_teacher, day=target_day,
                     status=1, homework_status='No', score=0)
                    new_records.append(study_record)
                Session.add_all(new_records)
                Session.commit()
                print("课程:{}增加了{}的学习记录。".format(subject_name, target_day))


    def modify_score(self, subject_name, student_qq):
        '''
           修改成绩
              首先获取该学生所有作业记录。
              然后选择需要修改的条目。
              输入新的作业成绩。
              写入该成绩。

           :param subject_name: 课程的名称。
           :param student_qq: 学员的qq。
           :return:
           '''
        subject = common.get_subject(subject_name)
        student = common.get_student_by_qq(student_qq)
        #获取对应课程和和学员的学习记录。
        while True:
            study_record=Session.query(init_database.StudyRecord).filter(
                    init_database.StudyRecord.subject == subject,
                init_database.StudyRecord.student == student
                ).order_by(init_database.StudyRecord.day.asc()).all()
            for item in study_record:
                #打印出该学员的对应课程的作业记录。
                print("id:{} 作业记录：{}".format(study_record.index(item),item))

            print("请输入需要修改的作业记录:(q for exit!)")
            choice=input(">>")
            if choice == "q":
                break
            #获取待修改的作业记录对象。
            target_record=study_record[int(choice)]
            print("请输入新成绩: (0~100分)")
            score=input(">>")
            #重新赋值作业分数。
            target_record.score = score
            Session.commit()
            print("成绩修改好了。")





