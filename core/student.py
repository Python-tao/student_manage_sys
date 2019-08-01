import os
import sys
BASE_DIR = os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) )
sys.path.append(BASE_DIR)
from db import init_data
from db import init_database
from db.init_data import Session
from core import common
from sqlalchemy import func

class Student(object):
    def __init__(self, qq):
        self.qq = qq

    def get_qq(self):
        return init_data.get_qq()

    def get_stu_by_qq(self):
        student = common.get_student_by_qq(self.qq)
        return student

    def get_homework_status(self, subject_name):
        '''
            获取作业的状态。
        :param subject_name: 课程名称，为str类型变量。
        :return: target_list，未交作业的记录。
        '''
        subject = common.get_subject(subject_name)
        student = common.get_student_by_qq(self.qq)
        if subject != None and student != None:
            #获取该学员所指定的课程的学习记录。
            subject_record = Session.query(init_database.StudyRecord).filter(
                init_database.StudyRecord.subject == subject,
                init_database.StudyRecord.student == student,
            ).all()
            if type(subject_record) is list:
                print("你的{}作业状况如下:".format(subject_name))
                target_list=[]
                for item in subject_record:

                    print("id:{}|subject:{}|day:{}|homework_status:{}".format(\
                        item.id,item.subject.name,item.day,item.homework_status))
                    if item.homework_status=='No':
                        #为未交作业的记录保存到target_list列表中。
                        target_list.append(item.day)

                return target_list


            else:
                print(subject_record)


    def submit_homework(self, subject_name, subject_day):
        '''
        提交作业。

        :param subject_name: 课程名称。
        :param subject_day: 课程节次。
        :return:
        '''
        #通过课程名，学生qq，课程节次，获取对应的课程记录。
        study_record = common.get_subject_record(subject_name, self.qq, subject_day)

        if study_record != None:
            #把学习记录中的作业状态修改为已交。
            study_record.homework_status = "Yes"
            Session.commit()
            print("{}的作业提交成功。".format(subject_day))
            return True
        else:
            print("作业提交失败。")
            return False

    def get_score(self, subject_name):
        '''
        查看指定的课程的成绩
        :param subject_name: 课程名称。
        :return:
        '''
        subject = common.get_subject(subject_name)
        student = common.get_student_by_qq(self.qq)
        if subject != None and student != None:
            #根据学员和课程名称，获取学习记录。
            subject_record = Session.query(init_database.StudyRecord).filter(
                init_database.StudyRecord.subject == subject,
                init_database.StudyRecord.student == student,
            ).all()
            if type(subject_record) is list:
                print("你的{}成绩如下:".format(subject_name))
                for item in subject_record:
                    print(item)
            else:
                print(subject_record)
        else:
            print("无此记录。")
            # return None

    def get_rank(self, subject_name):
        '''
        获取排名。
            首先获取同一个课程的所有学员的作业成绩记录。
            然后每个学员统计各自的成绩总分。
            然后对总分进行排名。
            返回当前学员的名次。

        :param subject_name: 课程名称。
        :return:
        '''
        subject = common.get_subject(subject_name)
        student = common.get_student_by_qq(self.qq)
        #根据课程获取该课程对应的学员的列表。
        students_group=subject.student
        tar_dict={}
        for s_item in students_group:
            #获取每个学员的指定课程的学习记录。
            subject_records = Session.query(init_database.StudyRecord).filter(
                init_database.StudyRecord.subject == subject,
                init_database.StudyRecord.student==s_item
            ).order_by(init_database.StudyRecord.day.asc()).all()
            sum=0
            for i in subject_records:
                sum+=i.score
                #统计每个学员的作业总分，然后存入字典。
            tar_dict.update({s_item.qq:sum})
            #对字典排序。
        sort_dict=sorted(tar_dict.items(),key=lambda x:x[1])
        sort_dict.reverse()
        print(sort_dict)
        for i in sort_dict:
            if i[0]== self.qq:
                #获取当前学员的名次。
                rank=sort_dict.index(i)+1
        print("你在{}个学员中，排名{}。".format(len(sort_dict),rank))
        wait=input('press any key..')


