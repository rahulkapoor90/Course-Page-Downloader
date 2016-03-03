from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import base
from Course import Course 
from User import User
from Api import Api
engine = create_engine("sqlite:///course.db")
base.Base.metadata.create_all(engine, checkfirst = True)
Session = sessionmaker(bind = engine)
db = Session()
userdata = db.query(User)
user = User()
first = False
loggedin = False
if userdata.count() == 0:
	print "Welcome to Auto Course Downloader! To get started fill the details below"
	user_regno = raw_input("Enter regno: ")
	user_password = raw_input("Enter password: ")
	user.user_regno = user_regno
	user.user_password = user_password
	db.add(user)
	first = True
else:
	for firstu in userdata:
		user.user_regno = firstu.user_regno
		user.user_password = firstu.user_password
login = Api.login(user.user_regno, user.user_password)
if login[0] == True:
	cookies = login[1]
	loggedin = True
	if first:
		courses = Api.get_courses(cookies)
		db.add_all(courses)
		db.commit()
	else:
		courses = db.query(Course)
else:
	print "Invalid Credentials Quitting the program"

	


			
		
 

