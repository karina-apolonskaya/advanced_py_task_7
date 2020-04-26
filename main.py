import psycopg2


def create_db():
    with psycopg2.connect(
            dbname="",
            user="",
            password=""
    ) as conn:
        cur = conn.cursor()
        cur.execute("""
         create table if not exists student(
            id integer primary key not null,
            name varchar(100) not null,
            gpa numeric(10,2),
            birth timestamp with time zone);
         """)
        cur.execute("""
         create table if not exists course(
            id integer primary key not null,
            name varchar(100) not null);
         """)
        cur.execute("insert into course(id, name) values (%s, %s);", (1, "Python"))
        cur.execute("insert into course(id, name) values (%s, %s);", (2, "Javascript"))
        conn.commit()
        cur.execute("select * from student;")
        cur.execute("select * from course;")
        students = cur.fetchall()
        course = cur.fetchall()
    return students, course


def add_student(id, name, gpa, birth):
    student = {'st_id': [id, name, gpa, birth]}
    with psycopg2.connect(
            dbname="",
            user="",
            password=""
    ) as conn:
        cur = conn.cursor()
        cur.execute("insert into student(id, name, gpa, birth) values (%s, %s, %s, %s);", student['st_id'])
        conn.commit()
        cur.execute("select id, name, gpa, birth from student where id = %s;", student['st_id'][0])
        added_student = cur.fetchall()
    return added_student


def get_student(student_id):
    with psycopg2.connect(
            dbname="",
            user="",
            password=""
    ) as conn:
        cur = conn.cursor()
        cur.execute("select id, name, gpa, birth from student where id = %s;", (student_id,))
        st_name = cur.fetchall()
    return st_name


def add_students(course_id, student_id, name, gpa, birth):
    student = {'st_id': [student_id, name, gpa, birth]}
    with psycopg2.connect(
            dbname="",
            user="",
            password=""
    ) as conn:
        cur = conn.cursor()
        cur.execute("insert into student(id, name, gpa, birth) values (%s, %s, %s, %s);", student['st_id'])
        conn.commit()
        cur.execute("""
         create table if not exists student_course(
            id serial primary key not null,
            course_id INTEGER REFERENCES course(id),
            student_id INTEGER REFERENCES student(id));
         """)
        cur.execute("insert into student_course (course_id, student_id) values (%s, %s);",
                    (course_id, student['st_id'][0]))
        conn.commit()
        cur.execute("""select s.id, s.name, c.name from student_course sc
        join student s on s.id = sc.student_id join course c on c.id = sc.course_id;""")
        add_student_to_course = cur.fetchall()
    return add_student_to_course


def get_students(course_id):
    with psycopg2.connect(
            dbname="",
            user="",
            password=""
    ) as conn:
        cur = conn.cursor()
        cur.execute("""select s.id, s.name from student_course sc join student s on s.id = sc.student_id 
        join course c on c.id = sc.course_id
        where sc.course_id = %s;""", (course_id,))
        students = cur.fetchall()
    return students


# created_db = create_db()
# print(created_db)

# student_added = add_student('9', 'Alexey', '10.20', '15.02.1988')
# print(student_added)

# student_name = get_student(7)
# print(student_name)

# student_course = add_students(2, 8, "Michael", "11.05", "12.05.1990")
# print(student_course)

# students_from_course = get_students(2)
# print(students_from_course)
