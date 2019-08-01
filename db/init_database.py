#Author:xyt
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from sqlalchemy import create_engine,ForeignKey,Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,Date,Enum
from sqlalchemy.orm import sessionmaker,relationship

from conf import settings


#远程sql数据库。
# engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}". \
#                             format(settings.db_server_conf['user'],
#                                    settings.db_server_conf['pwd'],
#                                    settings.db_server_conf['host'],
#                                    settings.db_server_conf['port'],
#                                    settings.db_server_conf['db'],
#                                    ),
#                             encoding='utf-8', echo=False)

#本地sqlite数据库
engine = create_engine("sqlite:///%s/db/database.db"%(BASE_DIR))



Base = declarative_base()  # 生成orm基类

#学员表
class Student(Base):
    __tablename__ = 'student'  # 表名
    id = Column(Integer, primary_key=True, autoincrement=True)  #字段
    name = Column(String(32),nullable=False)
    qq = Column(String(32),nullable=False)


    def __repr__(self):
        #返回值输入形式。
        return "<id:{}|name:{}|QQ:{}>".format(self.id,self.name, self.qq)


#老师表
class Teacher(Base):
    __tablename__ = 'teacher'  # 表名
    id = Column(Integer, primary_key=True, autoincrement=True)  #字段
    name = Column(String(32),nullable=False)


    def __repr__(self):
        #返回值输入形式。
        return "<id:{} | name:{}>".format(self.id,self.name)

# 创建关系表，第三张表连接grade和stuent
#科目表和学员表是多对多的关系，一个科目可以有多个学员报名，一个学员也可以报多个科目。
subject2student=Table("subject2student",Base.metadata,
                      Column("subject_id",Integer,ForeignKey("subject.id")),
                    Column("student_id",Integer,ForeignKey("student.id"))
                      )





#科目表
class Subject(Base):
    __tablename__ = 'subject'  # 表名
    id = Column(Integer, primary_key=True, autoincrement=True)  #字段
    name = Column(String(32),unique=True)


    student=relationship("Student",secondary=subject2student,backref="my_subjects")

    def __repr__(self):
        #打印此对象时的输出形式。
        return "<id:{} | name:{}>".format(self.id,self.name)








#学习记录表
class StudyRecord(Base):
    __tablename__ = 'study_record'  # 表名
    id=Column(Integer,primary_key=True, autoincrement=True)
    #老师id
    teacher_id = Column(Integer, ForeignKey("teacher.id"))
    stu_id=Column(Integer,ForeignKey("student.id"))
    subject_id=Column(Integer,ForeignKey("subject.id"))
    #节次
    day=Column(String(64),nullable=False)
    #出勤状态
    status=Column(Integer,nullable=False,default=0)
    #作业状态
    homework_status=Column(String(32),nullable=False,default="No")
    #作业分数
    score=Column(Integer,nullable=False)

    #在ORM内存中创建一个student字段，通过此字段可以反查student表中的数据。
    student=relationship("Student",foreign_keys=[stu_id],backref="my_study_record")#这是ORM自己的附加功能，与mysql无关。
    subject=relationship("Subject",foreign_keys=[subject_id],backref="my_study_record")#这是ORM自己的附加功能，与mysql无关。
    teacher=relationship("Teacher",foreign_keys=[teacher_id],backref="my_study_record")#这是ORM自己的附加功能，与mysql无关。
    def __repr__(self):
        #返回值输入形式。
        return "<id:{}|teacher:{}|student:{}|subject:{}|day:{}|status:{}|homework_status:{}|score:{}>".\
            format(self.id,self.teacher.name,self.student.name,self.subject.name,self.day,self.status,self.homework_status,self.score)






if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("数据库初始化成功")