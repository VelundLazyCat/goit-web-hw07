from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class Teacher(Base):
    __tablename__ = 'teachers'
    teacher_id = Column(Integer, primary_key=True, autoincrement=True)
    teacher_name = Column(String(150), nullable=False)


class Group(Base):
    __tablename__ = 'groups'
    group_id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String(50), nullable=False)


class Student(Base):
    __tablename__ = 'students'
    student_id = Column(Integer, primary_key=True, autoincrement=True)
    student_name = Column(String(150), nullable=False)
    group_id = Column('group_id', ForeignKey(
        'groups.group_id', ondelete='CASCADE'))
    group = relationship('Group', backref='students')


class Subject(Base):
    __tablename__ = 'subjects'
    subject_id = Column(Integer, primary_key=True, autoincrement=True)
    subject_name = Column(String(50), nullable=False)
    teacher_id = Column('teacher_id', ForeignKey(
        'teachers.teacher_id', ondelete='CASCADE'))
    teacher = relationship('Teacher', backref='subjects')


class Grade(Base):
    __tablename__ = 'grades'
    grade_id = Column(Integer, primary_key=True)
    grade_name = Column(Integer, nullable=False)
    date_of = Column('date_of', Date, nullable=True)
    student_id = Column('student_id', ForeignKey(
        'students.student_id', ondelete='CASCADE'))
    subjects_id = Column('subject_id', ForeignKey(
        'subjects.subject_id', ondelete='CASCADE'))
    student = relationship('Student', backref='grade_name')
    subject = relationship('Subject', backref='grade_name')


'''docker run --name postgres-webb -p 5432:5432 -e POSTGRES_PASSWORD=567234 -d'''
