# 主题：学员管理系统

需求：

用户角色，讲师＼学员， 用户登陆后根据角色不同，能做的事情不同，分别如下

# 讲师视图
```
　　管理课程，可创建课程，
   可根据学员qq号把学员加入课程。
　　可创建指定班级的上课纪录，注意一节上课纪录对应多条学员的上课纪录，即每节课都有整班学员上，
    为了纪录每位学员的学习成绩，需在创建每节上课纪录同时为这个班的每位学员创建一条作业记录。
　　为学员批改成绩， 一条一条的手动修改成绩
```
# 学员视图
```
    提交作业
    查看作业成绩
    一个学员可以同时属于多个课程，就像报了Linux的同时也可以报名Python一样，
    所以提交作业时需先选择课程，再选择具体上课的节数
    学员可以查看自己的课程成绩排名
```
# 分析：
```
    数据库表结构
    teacher（id, name） # 教师表
    student(id, name, qq, subject) # 学生表，其中subject是relationship字段
    subject(id, name, student) # 课程表，其中student是relationship字段
    study_record(subject_id, student_id, day, status,homework_status, score) # 学习记录表，一对多关系表
    subject2student(grade_id, student_id) # 课程与学员对应关系表，为多对多关系表
```
# 目录结构
```
- bin 
    -run_SMS.py        程序启动入口
- conf
    -settinggs.py   全局配置文件，保存mysql的ip和端口。    
    
-core               核心代码
    -main.py        主要的交互逻辑函数。
    -student.py     学生的功能封装
    -teacher.py     教师的功能封装
    -common.py      以上二个对象公共函数。
-db                 本地sqlite数据库管理
    -init_data      数据库，初始数据添加
    -init_database  数据库数据结构的初始化
    -database.db    用sqlite存储数据
```