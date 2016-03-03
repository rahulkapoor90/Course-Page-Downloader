from sqlalchemy import Column, Integer, Unicode, UnicodeText, String
from base import Base
class Course(Base):
	__tablename__ = 'courses'
	course_code = Column(String(5))
	course_slot = Column(String(10))
	course_faculty = Column(String(20))
	course_secret = Column(String(10))
	course_key = Column(String(20), primary_key = True)
	def __init__(self, course_code, course_slot, course_faculty, course_secret):
		self.course_code = course_code
		self.course_slot = course_slot
		self.course_faculty = course_faculty
		self.course_secret = course_secret
		self.course_key = course_slot + course_code + course_faculty
