import sqlite3
from datetime import datetime
from heshlash import *
from tabulate import tabulate

def con():
    return sqlite3.connect('dbt.db')
def create_table_user():
    conn = con()
    cur = conn.cursor()
    query = """
            create table users(
                userID integer not null primary key autoincrement,
                first_name varchar(30),
                last_name varchar(30),
                birth_day varchar(10),
                phone varchar(13),
                username varchar(50),
                password varchar(150),
                is_admin boolean default false
            )
        """
    cur.execute(query)
    conn.commit()
    conn.close()

# create_table_user()

def write_user(data:dict):
    conn = con()
    cur = conn.cursor()
    data['password'] = hash_password(data['password'])
    value = tuple(data.values())
    cur.execute("""
            insert into users(
                first_name,
                last_name,
                birth_day,
                phone,
                username,
                password
            )
            values(?,?,?,?,?,?)
        """,value)
    
    conn.commit()
    conn.close()
def check_user(username:str,phone:str):
    conn = con()
    cur = conn.cursor()
    cur.execute("""
        select count(userID) from users
        where username=? and phone=?
        """, (username, phone))
    user_data = cur.fetchone()
    return user_data[0]
def is_exists():
    first_name = input("First name: ")
    last_name = input("Last name: ")
    birth_day = input("Birth day[yyyy-mm-dd]: ")
    phone= input("Phone number: ")
    username = input("Username: ")
    password=input("Password: ")
    user_data = check_user(username,phone)
    if user_data:
         print("Bu foydalanuchi oldin kirilgan")
    else:
        data = dict(
            first_name = first_name,
            last_name = last_name,
            birth_day = birth_day,
            phone= phone,
            username= username,
            password=password
              )
        write_user(data)
        print(" successfully ")
   
def login(username,password):
    conn = con()
    cur = conn.cursor()
    cur.execute("""
        select count(userID) from users
        where username=? and password=?
        """,(username,hash_password(password)))
    user_data = cur.fetchone()
    if user_data:
        cur.execute("""
            select * from users
            where username=? and password=?
        """,(username,hash_password(password)))
    user_data2 = cur.fetchone()
    if user_data2[-1]:
        return 1
    else:
        return 2
def create_course_table():
    conn = con()
    cur = conn.cursor()
    cur.execute("""
        create table courses(
            courseID integer not null primary key autoincrement,
            name varchar(50),
            number_of_students int,
            is_active boolean default true
        )
    """)
    conn.commit()
    conn.close()
def check_course(name):
    conn = con()
    cur = conn.cursor()
    cur.execute("""
        select count(courseID) from courses
        where name =?
    """,(name,))
    course = cur.fetchone()
    conn.close()
    return course[0]
def add_course():
    course_name = input('Course name:')
    num_students = int(input('Number of Students:'))
    conn = con()
    cur = conn.cursor()
    check = check_course(course_name)
    if check:
        print("This course already exists ")
    else:
        cur.execute("""
        insert into courses(
            name,
            number_of_students
        )
        values
        (?,?)
    """,(course_name,num_students))
        conn.commit()
        print("Course saved ")
def student_course_table():
    conn = con()
    cur = conn.cursor()
    cur.execute("""
        create table students(
            courseID integer not null primary key autoincrement,
            course_id integer, 
            student_id integer,
            join_date datetime,
            foreign key(course_id) references courses(courseID),
            foreign key(student_id) references users(userID)
            
           
            
        )
    """)
    conn.commit()
    conn.close()

# student_course_table()
def show_courses():
    conn = con()
    cur = conn.cursor()
    cur.execute("""
        select * from courses
    """)
    course = cur.fetchall()
    courses = [{'Id': i[0], 'Name':i[1], 'Free place':i[2]} for i in course]
    conn.close()
    print(tabulate(courses, headers='keys', tablefmt='fancy_grid'))
def show_students():
    conn = con()
    cur = conn.cursor()
    query = """
        select * from students
    """
    cur.execute(query)
    data = cur.fetchall()
    students_data = []
    for i,e in enumerate(data):
        cur.execute("""
            select * from courses
            where courseID=?
        """,(e[1],))
        fan = cur.fetchone()
        cur.execute("""
            select * from users
            where userID=?
        """,(e[2],))
        user_data = cur.fetchone()
        students_data.append({"No":i+1,"Student name":user_data[1],"Course":fan[1]})
    print(tabulate(students_data,headers='keys',tablefmt='fancy_grid'))
def show_my_courses(username):
    conn = con()
    cur = conn.cursor()
    cur.execute("""
        select userID from users
        where username=?
    """, (username,))
    user = cur.fetchone()
    cur.execute("""
        select course_id,join_date from students
        where student_id=?
    """, (user[0],))
    courses = cur.fetchall()
    if len(courses) == 0:
        return False

    my_course = []
    for i in courses:
        cur.execute("""
               select name from courses
               where courseID=?
           """, (i[0],))
        name = cur.fetchone()
        my_course.append({"Course name": name[0],"Joined time":str(i[1])[:19]})
    print(tabulate(my_course,headers='keys',tablefmt='fancy_grid'))
    return True
def join_course(username):
    show_courses()
    conn = con()
    cur = conn.cursor()
    course_id = input('Enter course id:')
    query = """
        select count(courseID) from courses
        where courseID = ?
    """
    values = (course_id,)
    cur.execute(query,values)
    data = cur.fetchone()
    if data:
        query2 = """
            select * from users
            where username=?
        """
        cur.execute(query2,(username,))
        user = cur.fetchone()
        cur.execute("""
            select count(courseID) from students
            where student_id=? and course_id=?
        """,(user[0],course_id))
        is_join = cur.fetchone()
        if not is_join[0]:
            cur.execute("""
                select * from courses
                where courseID=?
            """, (course_id,))
            num_students = cur.fetchone()
            if num_students[2] > 0:
                cur.execute("""
                    insert into students(
                        course_id, 
                        student_id,
                        join_date
                    )
                    values
                    (?,?,?)
                """,(course_id, user[0],datetime.now()))
                conn.commit()
                cur.execute("""
                    update courses set number_of_students=? where courseID=? 
                """,(num_students[2]-1, course_id))
                conn.commit()
                cur.execute("""
                    select * from courses
                    where courseId=?
                """,(course_id,))
                is_full = cur.fetchone()
                if is_full[2] == 0:
                    cur.execute("""
                        update courses set is_active=? where courseID=? 
                    """, (False, course_id))
                    conn.commit()
                conn.close()
                print("You join ")
            else:
                print('It\'s Full ')
                join_course(username)
        else:
            print("You already join this course!")
    else:
        print("This course is not exists ")


conn=con()
cur=conn.cursor()

# cur.execute('update users set is_admin=? where userID=?',(1,1))
# conn.commit()

        


    