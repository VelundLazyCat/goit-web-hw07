from models import Teacher, Group, Student, Subject, Grade
from my_db import session
from faker import Faker
from random import randint, choice
from sqlalchemy.exc import SQLAlchemyError


NUMBER_STUDENTS = 50
NUMBER_TECHERS = 5
NUMBER_SUBJECTS = 8
NUMBER_GROUPS = 3
NUMBER_GRADES = 20
MIN_GRADE = 1
MAX_GRADE = 100

fake_data = Faker('uk-UA')

fake_students = []  # тут зберігатимемо студентів
fake_teachers = []  # тут зберігатимемо викладачів
fake_subjects = []  # тут зберігатимемо предмети
fake_groups = []    # тут зберігатимемо групи студентів
fake_grades = []    # тут зберігатимемо оцінки з предмету предмету для кожного студента


# створення груп
def insert_grops():
    for _ in range(NUMBER_GROUPS):
        group = Group(group_name=fake_data.word())
        session.add(group)


# створення викладачів
def insert_teachers():
    for _ in range(NUMBER_TECHERS):
        teacher = Teacher(teacher_name=fake_data.name())
        session.add(teacher)


# створення студентів із вказівклю до якої групи належить
def insert_students():
    for _ in range(NUMBER_STUDENTS):
        student = Student(student_name=fake_data.name(),
                          group_id=randint(1, NUMBER_GROUPS + 1))
        session.add(student)


# створення предметів із вказівкою викладача
def insert_subjects():
    for _ in range(NUMBER_SUBJECTS):
        subject = Subject(subject_name=fake_data.word(),
                          teacher_id=randint(1, NUMBER_TECHERS + 1))
        session.add(subject)


# створення оцінок з предметів із вказівкою викладача
def insert_grades():
    for student in range(1, NUMBER_STUDENTS + 1):
        for _ in range(1, NUMBER_GRADES + 1):
            grade = Grade(grade_name=randint(MIN_GRADE, MAX_GRADE),
                          date_of=fake_data.date_this_decade(),
                          student_id=student,
                          subjects_id=randint(1, NUMBER_SUBJECTS + 1))
            session.add(grade)


if __name__ == '__main__':
    try:
        insert_grops()
        insert_teachers()
        insert_students()
        insert_subjects()
        insert_grades()
        session.commit()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        session.close()
