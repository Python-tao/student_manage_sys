import os
import sys
BASE_DIR = os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) )
sys.path.append(BASE_DIR)



from conf import settings
from core.student import Student
from core.teacher import Teacher

'''
主函数

'''

def student_view():
    """学生视图"""
    qq = input("请输入学生qq号：")
    student = Student(qq)

    stu_obj=student.get_stu_by_qq()
    if stu_obj==None:
        print("查无此号:{}，请重新输入。".format(qq))
        student_view()
    else:
        print("你好,{}同学.欢迎进入学员管理系统。请选择你要执行的操作。".format(stu_obj.name))
        while True:
            msg='''
1.交作业
2.查成绩
3.看排名
q.退出
            '''
            print(msg)
            choice = input(">>")
            if choice == "1":#交作业
                print("你报了以下课程：")
                sub_list = []
                for item in stu_obj.my_subjects:
                    sub_list.append(item.name)
                    print("No:{},课程名称:{}.".format(item.id, item.name))
                print("请选择你要提交作业的课程:", sub_list)
                subject_name = input(">>")
                if subject_name in sub_list:
                    #显示当前作业的状态。
                    res_list=student.get_homework_status(subject_name)
                    print("请选择你要提交作业的节次:", res_list)
                    day_name= input(">>")
                    if day_name in res_list:
                        student.submit_homework(subject_name,day_name)
                    else:
                        print("输入有误。")

                else:
                    print("你输入的是什么？")

            elif choice == "2":#查成绩
                print("你报了以下课程：")
                sub_list=[]
                for item in stu_obj.my_subjects:
                    sub_list.append(item.name)
                    print("No:{},课程名称:{}.".format(item.id,item.name))
                print("请选择你要查询的课程:",sub_list)
                subject_name = input(">>")
                if subject_name in sub_list:
                    student.get_score(subject_name)
                    wait=input("press any key..")
                else:
                    print("你输入的是什么？")


            elif choice == "3":#看排名
                print("你报了以下课程：")
                sub_list = []
                for item in stu_obj.my_subjects:
                    sub_list.append(item.name)
                    print("No:{},课程名称:{}.".format(item.id, item.name))
                print("请选择你要看排名的课程:", sub_list)
                subject_name = input(">>")
                if subject_name in sub_list:
                    #调用get_rank方法计算排名。
                    student.get_rank(subject_name)

                else:
                    print("你输入的是什么？")
            elif choice=="q":
                run()

            else:
                print("请输入正确的选项")


def teacher_view():
    """教师视图"""
    teacher_name = input("输入老师姓名:")
    teacher = Teacher(teacher_name)
    stu_obj=teacher.get_teacher_name()
    if stu_obj==None:
        print("查无此人:{}，请重新输入。".format(teacher_name))
        teacher_view()
    else:
        print("你好,{}老师.欢迎进入学员管理系统。请选择你要执行的操作。".format(teacher.name))
    while True:
        msg='''
1.增加课程
2.把学生增加到班级
3.增加上课记录
4.修改学生成绩 
q.退出
        '''
        print(msg)
        choice = input(">>")
        if choice == "1":#增加课程
            current_sub=[]
            res=teacher.get_current_subject()
            for item in res:
                current_sub.append(item.name.lower())
            print("当前已有课程：{}".format(current_sub))
            print("请输入需要添加的课程：")
            subject_name = input(">>")
            #判断输入的课程是否与已有的课程重名，有重名则不必添加。
            if subject_name.lower() in current_sub:
                print("已经有这个课程了。")
            else:
                #执行增加课程的方法。
                ret = teacher.add_subject(subject_name)
                print(ret)
        elif choice == "2":#把学生增加到班级
            print("请输入学生qq号：")
            qq = input(">>")
            print("请输入课程名称：")
            subject_name = input(">>")
            #执行增加学员到课程中的方法。
            teacher.add_student_to_subject(qq, subject_name)


        elif choice == "3":#增加上课记录
            current_sub = []
            res = teacher.get_current_subject()
            for item in res:
                current_sub.append(item.name)

            print("当前已有课程：{}".format(current_sub))
            print("请输入需要添加上课记录的课程：")
            subject_name = input(">>")
            #判断输入的课程是否为已有的课程。
            if subject_name in current_sub:
                #执行增加上课记录的方法。
                teacher.add_study_record(subject_name)

            else:
                print("输入有误.")


        elif choice == "4":#修改学生成绩
            qq = input("请输入学生qq号：")
            subject_name = input("课程名称:")
            ret = teacher.modify_score(subject_name, qq)
        elif choice == "q":
            run()

        else:
            print("请输入正确的选项")












def run():
    msg='''
##欢迎进入学员管理系统###
    请选择角色：
    1.教师
    2.学生     
    '''


    print(msg)
    role = input(">>").strip()


    print(role)
    if role == "1":
        teacher_view()
    elif role == "2":
        student_view()
    else:
        print("输入错误，退出程序")
        exit()

