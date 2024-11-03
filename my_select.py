from sqlalchemy import select, func, desc, and_
from models import Teacher, Group, Student, Subject, Grade
from my_db import session


# Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_01():
    """SELECT s.student_id, s.student_name, ROUND(AVG(g.grade_name), 1) AS average_grade
    FROM students AS s
    LEFT JOIN grades AS g ON s.student_id = g.student_id
    GROUP BY s.student_id
    ORDER BY average_grade DESC
    LIMIT 5;"""
    result = session.query(Student.student_id, Student.student_name, func.round(func.avg(Grade.grade_name), 1).label(
        'average_grade')).select_from(Student).join(Grade).group_by(Student.student_id).order_by(desc('average_grade')).limit(5).all()
    return result


# Знайти студента із найвищим середнім балом з певного предмета.
def select_02():
    """SELECT sub.subject_name , s.student_id, s.student_name , 
       ROUND(AVG(g.grade_name), 1) AS average_grade
       FROM grades g
       JOIN subjects sub ON sub.subject_id = g.subject_id
       JOIN students s ON s.student_id = g.student_id
       WHERE g.subject_id = 2
       GROUP BY s.student_id
       ORDER  BY average_grade DESC
       LIMIT 1;"""
    result = session.query(Subject.subject_name, Student.student_id, Student.student_name,
                           func.round(func.avg(Grade.grade_name),
                                      1).label('average_grade')
                           ).select_from(Grade).join(Subject).join(Student).filter(Grade.subjects_id == 2
                                                                                   ).group_by(Student.student_id).order_by(desc('average_grade')).limit(1).first()
    return result


# Знайти середній бал у групах з певного предмета.
def select_03():
    """SELECT gr.group_id , gr.group_name, sub.subject_name,
       ROUND(AVG(g.grade_name), 1) AS average_grade
       FROM grades g
       JOIN subjects sub ON sub.subject_id = g.subject_id
       JOIN students s ON s.student_id = g.student_id
       JOIN groups gr ON gr.group_id = s.group_id 
       WHERE g.subject_id = 2
       GROUP BY gr.group_id;"""
    result = session.query(Group.group_id, Group.group_name, Subject.subject_name,
                           func.round(func.avg(Grade.grade_name), 1).label(
                               'average_grade')).select_from(Grade).join(Subject).join(Student).join(Group).filter(Grade.subjects_id == 2).group_by(Group.group_id).all()
    return result


# Знайти середній бал на потоці (по всій таблиці оцінок).
def select_04():
    """SELECT AVG(g.grade_name) average_grade
       FROM grades g;"""
    result = session.query(func.round(func.avg(Grade.grade_name), 1).label("average_grades")
                           ).select_from(Grade).all()

    return result


# Знайти які курси читає певний викладач.
def select_05():
    """SELECT t.teacher_name, s.subject_name
       FROM teachers t 
       JOIN subjects s ON s.teacher_id = t.teacher_id 
       WHERE s.teacher_id = 3;"""
    result = session.query(Teacher.teacher_name, Subject.subject_name).select_from(
        Teacher).join(Subject).filter(Subject.teacher_id == 3).all()
    return result


# Знайти список студентів у певній групі.
def select_06():
    """SELECT g.group_name, s.student_id, s.student_name
       FROM students s
       JOIN groups g ON s.group_id = g.group_id 
       WHERE s.group_id = 2;"""
    result = session.query(Group.group_name, Student.student_id, Student.student_name).select_from(
        Student).join(Group).filter(Student.group_id == 2).all()
    return result


# Знайти оцінки студентів у окремій групі з певного предмета.
def select_07():
    """SELECT group_students.group_id, sb.subject_name, 
       group_students.student_name, gr.grade_name
       FROM (
       SELECT g.group_id, s.student_name, s.student_id
       FROM students s
       JOIN groups g ON g.group_id = s.group_id
       WHERE g.group_id = 2) AS group_students
       JOIN grades AS gr ON  gr.student_id = group_students.student_id
       JOIN subjects sb ON sb.subject_id = gr.subject_id 
       WHERE gr.subject_id = 2;"""

    stmt = session.query(Group.group_id, Student.student_id, Student.student_name
                         ).select_from(Student).join(Group).filter(Group.group_id == 2).subquery()

    result = session.query(stmt, Subject.subject_name, Grade.grade_name
                           ).select_from(stmt).join(Grade).join(Subject
                                                                ).filter(Subject.subject_id == 2).all()

    return result


# Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_08():
    """"SELECT t.teacher_name, s.subject_name, ROUND(AVG(g.grade_name), 1)
        FROM grades g
        JOIN subjects s ON s.subject_id = g.subject_id
        JOIN teachers t ON t.teacher_id = s.teacher_id
        WHERE s.teacher_id = 3
        GROUP BY s.subject_name;"""

    result = session.query(Teacher.teacher_name, Subject.subject_name, func.round(func.avg(Grade.grade_name), 1)
                           ).select_from(Grade).join(Subject).join(Teacher
                                                                   ).filter(Subject.teacher_id == 3).group_by(Subject.subject_name).all()
    return result


# Знайти список курсів, які відвідує студент.
def select_09():
    """"SELECT s.student_name, sb.subject_name
        FROM students s 
        JOIN grades g ON s.student_id = g.student_id
        JOIN subjects sb ON sb.subject_id = g.subject_id
        WHERE s.student_id = 17
        GROUP BY sb.subject_name"""

    result = session.query(Student.student_name, Subject.subject_name
                           ).select_from(Student).join(Grade).join(Subject
                                                                   ).filter(Student.student_id == 17).group_by(Subject.subject_name).all()
    return result


# Знайти список курсів, які певному студенту читає певний викладач.
def select_10():
    """SELECT s.student_name, sb.subject_name, t.teacher_name
       FROM students s  
       JOIN grades g ON s.student_id = g.student_id
       JOIN subjects sb ON sb.subject_id = g.subject_id
       JOIN teachers t ON sb.teacher_id = t.teacher_id 
       WHERE s.student_id = 17 AND t.teacher_id = 3
       GROUP BY sb.subject_name"""
    result = session.query(Student.student_name, Subject.subject_name, Teacher.teacher_name
                           ).select_from(Student).join(Grade).join(Subject).join(Teacher
                                                                                 ).filter(and_(Student.student_id == 17, Teacher.teacher_id == 3)
                                                                                          ).group_by(Subject.subject_name).all()
    return result


# Середній бал, який певний викладач ставить певному студентові.
def select_11():
    """SELECT s.student_name,  ROUND(AVG(g.grade_name), 1), t.teacher_name
       FROM students s  
       JOIN grades g ON s.student_id = g.student_id
       JOIN subjects sb ON sb.subject_id = g.subject_id
       JOIN teachers t ON sb.teacher_id = t.teacher_id 
       WHERE s.student_id = 17 AND t.teacher_id = 3;"""
    result = session.query(Student.student_name, func.round(func.avg(Grade.grade_name), 1), Teacher.teacher_name
                           ).select_from(Student).join(Grade).join(Subject).join(Teacher
                                                                                 ).filter(and_(Student.student_id == 17, Teacher.teacher_id == 3)
                                                                                          ).all()
    return result


# Оцінки студентів у певній групі з певного предмета на останньому занятті.
def select_12():
    """SELECT s.student_id, s.student_name, g.grade_name, g.date_of
       FROM grades g 
       JOIN students s ON g.student_id = s.student_id 
       WHERE g.subject_id = 2 AND s.group_id = 3 AND g.date_of =(
           SELECT max(date_of)
           FROM grades g2 
           JOIN students s2 ON s2.student_id = g2.student_id
           WHERE g2.subject_id = 2 AND s2.group_id = 3);"""
    stmt = (select(func.max(Grade.date_of)).join(Student).filter(
        and_(Grade.subjects_id == 2, Student.group_id == 3))).scalar_subquery()

    result = session.query(Student.student_id, Student.student_name, Grade.grade_name, Grade.date_of).select_from(
        Grade).join(Student).filter(and_(Grade.subjects_id == 2, Student.group_id == 3, Grade.date_of == stmt)).all()
    return result


if __name__ == '__main__':

    # 1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    print('#1\nstudent_id, student_name, max of avg grade')
    for i in select_01():
        print(i)
    print('-'*30)

    # 2. Знайти студента із найвищим середнім балом з певного предмета.
    print('#2\nsubject, student_id, student_name, max avg grade')
    print(select_02())
    print('-'*30)

    # 3. Знайти середній бал у групах з певного предмета.
    print('#3\ngroup_id, group_name, subject_name, avg grade')
    for i in select_03():
        print(i)
    print('-'*30)

    # 4. Знайти середній бал на потоці (по всій таблиці оцінок).
    print('#4\navg grade on course')
    print(select_04())
    print('-'*30)

    # 5. Знайти які курси читає певний викладач.
    print('#5\nteacher_name, subject_name')
    print(select_05())
    print('-'*30)

    # 6. Знайти список студентів у певній групі.
    print('#6\ngroup_name, student_id, student_name')
    for i in select_06():
        print(i)
    print('-'*30)

    # 7. Знайти оцінки студентів у окремій групі з певного предмета.
    print('id_group, id_student, student_name, subject_name, grade')
    for i in select_07():
        print(i)
    print('-'*30)

    # 8. Знайти середній бал, який ставить певний викладач зі своїх предметів.
    print('teacher_name, subject_name, avg_grade')
    print(select_08())
    print('-'*30)

    # 9. Знайти список курсів, які відвідує студент.
    print('student_name, subject_name')
    for i in select_09():
        print(i)
    print('-'*30)

    # 10. Знайти список курсів, які певному студенту читає певний викладач.
    print('teacher_name, subject_name, student_name')
    for i in select_10():
        print(i)
    print('-'*30)

    # Додаткові завдання
    # 11. Середній бал, який певний викладач ставить певному студентові.
    print('student_name, avg_grade, teacher_name')
    for i in select_11():
        print(i)
    print('-'*30)

    # 12. Оцінки студентів у певній групі з певного предмета на останньому занятті.
    print('group_id, subject_name, student_name, grade, last_date')
    for i in select_12():
        print(i)
    print('-'*30)
