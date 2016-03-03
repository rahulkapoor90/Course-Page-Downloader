from bs4 import BeautifulSoup
import shutil
import requests as req
from CaptchaParser import CaptchaParser
from PIL import Image
from Course import Course
import json
captcha_url = 'https://academics.vit.ac.in/student/captcha.asp'
submit_url = 'https://academics.vit.ac.in/student/stud_login_submit.asp'
timetable_url = 'https://academics.vit.ac.in/student/timetable_ws.asp'
home_url = 'https://academics.vit.ac.in/student/stud_home.asp'
course_page_url = 'https://academics.vit.ac.in/student/coursepage_view.asp'
class Api:
	@staticmethod
	def login(regno, password):
		res = []
		print "Parsing captcha for you."
		res = req.get(captcha_url, stream = True)
		cookies = res.cookies
		with open('captcha.bmp', 'wb') as out_file:
			shutil.copyfileobj(res.raw, out_file)
		img = Image.open("captcha.bmp")
		parser = CaptchaParser()
		captcha = parser.getCaptcha(img)
		data = {}
		data['message'] = "";
		data['regno'] = regno
		data['passwd'] = password
		data['vrfcd'] = captcha
		print "Logging In..."
		login_res = req.post(submit_url, data = data, cookies = cookies)
		req.get(home_url, cookies = cookies) # just to make sure that session id is validated
		success = True
		res = [success, cookies]
		return res
	@staticmethod
	def get_courses(cookies):
		print "Getting your list of courses..."
		timetable_res = req.get(timetable_url, cookies = cookies)
		soup = BeautifulSoup(timetable_res.text, "html.parser")
		ttsoup = soup.findAll('table')[1]
		courses = []
		for course in ttsoup.findAll('tr'):
			if course['bgcolor'] == "#EDEADE":
				details = course.findAll('td')
				course_code = ""
				course_slot = ""
				course_fac = ""
				try:
					course_code = details[3].string
					course_fac = details[11].string.split(" - ")[0]
					course_slot = details[9].string
				except IndexError:
					course_code = details[1].string
					course_fac = details[9].string
					course_slot = details[7].string
				cur_course = Course(course_code, course_slot, course_fac, "xyz")
				courses.append(cur_course)
		print "Going to Course Page..."
		print len(courses)
		for course in courses:
			params = {}
			params['sem'] = 'WS'
			params['slt'] = course.course_slot
			params['crs'] = course.course_code
			res = req.get(course_page_url, cookies = cookies, params = params)
			print "Getting details of course and faculties " + course.course_code
			soup = BeautifulSoup(res.text, "html.parser")
			try:
				faculty_soup = soup.table.findAll('table')[1]
				for factag in faculty_soup.findAll('tr'):
					if factag['bgcolor'] == "#E1ECF2":
						fac_name = factag.findAll('td')[3].string.split(" - ")[1]
						if fac_name == course.course_faculty:
							course.course_secret = factag.form.td.findAll('input')[1]['value']
							print course.course_secret
							break
			except IndexError:
				print "Course page not available for course " + course.course_code
				courses.remove(course)
			if course.course_secret == "xyz":
				print "Course page not available for course " + course.course_code
				courses.remove(course)
		return courses


