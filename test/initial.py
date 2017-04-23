import socket
import sys
import os
import subprocess
from time import sleep
import traceback
import re
import datetime



class TestServer:
    #class for instantiating the test server
    def __init__(self,datastore_path,application_path):
        #desired location for the datastore of the test server
        self.temp_datastore_path = datastore_path
        #path to google app engine application directory
        self.app_path = application_path
        #this is going to be the process object for the server
        self.server_process = None

    #should not be called if a local development server is already started
    def startServer(self):
        # the following "with" block starts the local development server as a subprocess
        # we don't want the output of the test server,
        # so stderr and stdout are directed to /dev/null
        with open(os.devnull, 'w') as fp:
            # make sure this file is deleted
            del_p = subprocess.Popen(["rm",self.temp_datastore_path],stdout=fp,stderr=fp)
            del_p.wait()
            # security on user input important here ***
            # ie if user input "/home/consider && <malicious shell command>" it could be bad
            # start local server, specifying location for new datastore
            self.server_process = subprocess.Popen(["dev_appserver.py","--datastore_path="+self.temp_datastore_path,self.app_path,"--clear_datastore"],stdout=fp,stderr=fp)
            #TODO: check if dev_appserver is in path, if it's not fail
        TestServer.wait_for_server()

    #terminates test server and deletes datastore
    def quit_server(self):
        self.server_process.terminate()
        del_p = subprocess.Popen(["rm",self.temp_datastore_path])
        del_p.wait()

    def stop_server(self):
        self.server_process.terminate()
        self.server_process = None

    def resume_server():
        self.server_process = subprocess.Popen(["dev_appserver.py","--datastore_path="+temp_datastore_path,self.app_path],stdout=fp,stderr=fp)
        TestServer.wait_for_server()

    @staticmethod
    def wait_for_server():
        for i in range(0,15):
            sleep(1)
            if TestServer.isAServerRunning():
                break
            if i == 14:
                print("ERROR: server did not start in 15 seconds")

    @staticmethod
    def isAServerRunning():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1',8080))
        sock.close()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result2 = sock.connect_ex(('127.0.0.1',8000))
        sock.close()
        if result == 0 and result2 == 0:
            return True
        else:
            return False

#config assignment
temp_datastore_path ="/tmp/test-tmp-datastore"
#==================[START: initial checks]==================
#check to make sure we are running tests on a valid platform
if ("linux" not in sys.platform) and ("darwin" not in sys.platform):
    print("Sorry, this test script was designed to work with linux, not "+sys.platform)
    exit()

#check number of arguments
if len(sys.argv) < 2:
	print("not enough arguments!")
	print("$ ./test.py <path to consider>")
	exit()

#get user arguments
program = sys.argv[0]
path_to_consider = sys.argv[1]

# check user input for security
# some security on user input (look for: ***)
if (";" or "&" or "|" or " ") in path_to_consider:
	print("not a valid path to consider: ;, &, |, and whitespace are not allowed")
	exit()
if not os.path.exists(path_to_consider):
    print("not a valid path to consider: path <"+path_to_consider+"> does not exist")
    print("try using an absolute path. eg:")
    print("./test.py /home/millstev/summer16/capstone/consider")
    exit()

#check to see if a server is already started
if TestServer.isAServerRunning():
   print("Please terminate the local server before running the test script")
   exit()
else:
   print("Please start consider in the terminal in the next 15 seconds")

#==================[END: initial checks]==================
#==================[START: set up test server]==================
#in this assignment, we start a local development server

test_server = TestServer(temp_datastore_path,path_to_consider)
test_server.startServer()

#==================[END: set up test server]==================



#==================[START: prepare to run tests]==================

#in this assignment we define methods for use in the test cases
#most of these test methods are implemented via webscraping the local dev server

import requests
import json

#this session will be used in the tests
session = requests.Session()
#DEFINE METHODS USED FOR TESTS

#used for logging in
#second parameter True if we want to log in as administrator
def login(email_addr,isAdmin):
    url_string = "http://localhost:8080/_ah/login?email="+email_addr
    if isAdmin:
        url_string = url_string + "&admin=True"
    url_string = url_string + "&action=Login&continue=http://localhost:8080/"
    r = session.get(url_string)
    sleep(0.15)

#used to log out
def logout():
    session.get("http://localhost:8080/_ah/login?continue=http://localhost:8080/courses&action=logout")

def admin_post(datainput):
    r = session.post("http://localhost:8080/admin",data=datainput)
    if not ("200" or "401" in str(r)):
        print("error: admin post request responded with "+str(r))
    sleep(0.15)
    return r

def courses_post(datainput):
    r = session.post("http://localhost:8080/courses",data=datainput)
    if not ("200" or "401" in str(r)):
        print("error: courses post request responded with "+str(r))
    sleep(0.15)
    return r

def assignments_post(datainput):
    r = session.post("http://localhost:8080/assignments",data=datainput)
    if not ("200" or "401" in str(r)):
        print("error: assignments post request responded with "+str(r))
    sleep(0.15)
    return r

def rounds_post(datainput):
    r = session.post("http://localhost:8080/rounds",data=datainput)
    if not ("200" or "401" in str(r)):
        print("error: rounds post request responded with "+str(r))
    sleep(0.15)
    return r

def students_post(datainput):
    r = session.post("http://localhost:8080/students",data=datainput)
    if not ("200" or "401" in str(r)):
        print("error: students post request responded with "+str(r))
    sleep(0.15)
    return r

def student_rounds_post(datainput):
    r = session.post("http://localhost:8080/student_rounds",data=datainput)
    if not ("200" or "401" in str(r)):
        print("error: student_rounds post request responded with "+str(r))
    sleep(0.15)
    return r

def student_rounds_get(key):
    return session.get("http://localhost:8080/student_rounds?assignment="+key)

def groups_post(datainput):
    r = session.post("http://localhost:8080/groups",data=datainput)
    if not ("200" or "401" in str(r)):
        print("error: groups post request responded with "+str(r))
    sleep(0.15)
    return r

def studentRespond(response,key):
    data={"option":"option1","comm":response,"assignment":key}
    return student_rounds_post(data)

def addAssignment(course_name,assignment_name):
    data={"course":course_name,"assignment":assignment_name,"action":"add"}
    return assignments_post(data)

def modifyNumberOfGroups(num,course_name,assignment_name):
    data={"groups":num,"course":course_name,"assignment":assignment_name,"action":"add"}
    return groups_post(data)

def addInitialQuestion(duetime,question,numberQuestions,course,assignment):
    options = ["test question"]*numberQuestions
    options = str(options).replace("'",'"')
    data={"course":course.upper(),"assignment":assignment.upper(),"time":duetime,"question":question,"number":numberQuestions,"round":"1","roundType":"initial","startBuffer":"0","options":options,"action":"add"}
    return rounds_post(data)

def addDiscussionRounds(num,duration,course,assignment):
    data = {"total_discussions":num,"duration":duration,"course":course,"assignment":assignment,"action":"add_disc"}
    return rounds_post(data)

def deleteDiscussionRound(round_id,course,assignment):
    data = {"round_id":round_id,"course":course,"assignment":assignment,"action":"delete"}
    return rounds_post(data)

def changeDiscussionRound(round_id,course,assignment,description,deadline,starttime):
    data = {"round_id":round_id,"course":course,"assignment":assignment,"description":description,"roundType":"discussion","action":"change","deadline":deadline,"start_time":starttime}
    return rounds_post(data)

def addCourse(course_name):
    data={"name":course_name,"action":"add"}
    return courses_post(data)

def addStudents(emails,course,assignment):
    data = {"emails":str(emails).replace("'",'"'),"course":course,"assignment":assignment,"action":"add"}
    return students_post(data)

def removeStudent(email):
    data = {"email":email,"action":"remove"}
    return students_post(data)

#this method is confusing: the point is to locate and extract a token from the response
#this token is needed as a session cookie for authenticated requests
#basically, in order for a POST request to console to be successful, it must include this token as a cookie
def get_xsrf_token():
    req = requests.get("http://localhost:8000/console")
    reg = re.compile("xsrf_token.*\}")
    reg2 = re.compile("\w+")
    result = reg2.findall(str(reg.findall(req.text)[0]).split()[1])[0]
    if not result:
        print("ERROR: could not find xsrf_token!")
        return ""
    else:
        return result
xsrf_token = get_xsrf_token()

#this method is a way to send a console script to the interactive console webpage
#the point is so that the database may be queried programmatically
#the ans.text response will only contain what would have been printed out on the console
#so include print statements in the script in order to get the value in the response
def console(script):
    data = {"code":script,"module_name":"default","xsrf_token":xsrf_token}
    ans = requests.post("http://localhost:8000/console",data=data)
    return ans.text.strip()

#goes to the student home page and gets a list of keys for displayed assignments
def get_assignment_key_list():
    answer = []
    req = session.get("http://localhost:8080/student_home")
    reg = re.compile("redirect.*btn-block")
    result = reg.findall(req.text)
    for r in result:
        spl = r.split("'")
        answer.append(spl[1])
    return answer

def print_passed(num):
    print("\t\ttest "+str(num)+" passed")

def print_failed(num,errormsg):
    print("\t\ttest "+str(num)+" FAILED: "+errormsg)

def get_instructor_count():
    script = "from src import model\nprint(len(model.Instructor.query().fetch()))\n"
    result = console(script)
    return int(result)

def get_course_count(instructor_email):
    script = "from src import model\ninstructor = model.Instructor.query(model.Instructor.email=='"+instructor_email+"').fetch()[0]\ncourses = model.Course.query(ancestor=instructor.key).fetch()\nprint(len(courses))"
    result = console(script)
    return int(result)

def get_total_course_count():
    script = "from src import model\ncourses = model.Course.query().fetch()\nprint(len(courses))"
    result = console(script)
    return int(result)

def get_total_response_count():
    script = "from src import model\nresponses = model.Response.query().fetch()\nprint(len(responses))"
    result = console(script)
    return int(result)

def get_assignment_count(instructor_email):
    script = "from src import model\ninstructor = model.Instructor.query(model.Instructor.email=='"+instructor_email+"').fetch()[0]\nassignments = model.Assignment.query(ancestor=instructor.key).fetch()\nprint(len(assignments))"
    result = console(script)
    return int(result)

def get_group_count(instructor_email,course,assignment):
    script = "from src import model\n"
    script += "instructor = model.Instructor.query(model.Instructor.email=='"+instructor_email+"').fetch()[0]\n"
    script += "assignments = model.Assignment.query(ancestor=instructor.key).fetch()\n"
    script += "for s in assignments:\n"
    script += " if s.name == '"+assignment.upper()+"':\n"
    script += "  print(s.groups)\n"
    script += "  break\n"
    result = console(script)
    return int(result)

def get_total_assignment_count():
    script = "from src import model\nassignments = model.Assignment.query().fetch()\nprint(len(assignments))"
    result = console(script)
    return int(result)

def get_total_round_count():
    script = "from src import model\nrounds = model.Round.query().fetch()\nprint(len(rounds))"
    result = console(script)
    return int(result)

def get_total_student_count():
    script = "from src import model\nstudents = model.Student.query().fetch()\nprint(len(students))"
    result = console(script)
    return int(result)

def addInstructor(email):
    data = {'action':'add','email':email}
    admin_post(data)

def toggleInstructor(email):
    data = {'action':'toggle','email':email}
    admin_post(data)

def toggleCourse(coursename):
    data = {'action':'toggle','name':coursename}
    courses_post(data)

def toggleAssignment(coursename,assignmentname):
    data = {'action':'toggle','course':coursename,'assignment':assignmentname}
    assignments_post(data)

def isInstructorActive(email):
    script = "from src import model\ninstructor = model.Instructor.query(model.Instructor.email=='"+email+"').fetch()[0]\nprint(instructor.is_active)"
    result = console(script)
    if "True" in result:
        return True
    elif "False" in result:
        return False
    else:
        print("error: could not retrieve instructor")

def isCourseActive(name):
    script = "from src import model\ncourse = model.Course.query(model.Course.name=='"+name.upper()+"').fetch()[0]\nprint(course.is_active)"
    result = console(script)
    if "True" in result:
        return True
    elif "False" in result:
        return False
    else:
        print("error: could not retrieve course")

def isAssignmentActive(coursename,assignmentname):
    script = "from src import model\ncourse = model.Course.query(model.Course.name=='"+coursename.upper()+"').fetch()[0]\nassignment = model.Assignment.query(ancestor=course.key).fetch()\nfor sec in assignment:\n if (sec.name == '"+assignmentname.upper()+"'):\n  print(sec.is_active)\n"
    result = console(script)
    if "True" in result:
        return True
    elif "False" in result:
        return False
    else:
        print("error: could not retrieve assignment")

def endCurrentRound(course,assignment):
    data={"action":"end-current-round","course":course,"assignment":assignment}
    r = rounds_post(data)

def startRounds(course,assignment,):
    data={"action":"start","course":course,"assignment":assignment}
    rounds_post(data)

def getDeadline(round_id):
    script = "from src import model\n"
    script += "rounds = model.Round.query(model.Round.number == "+str(round_id)+").fetch()[0]\n"
    script += "print(rounds.deadline)\n"
    return console(script)

def getDescription(round_id):
    script = "from src import model\n"
    script += "rounds = model.Round.query(model.Round.number == "+str(round_id)+").fetch()[0]\n"
    script += "print(rounds.description)\n"
    return console(script)

def getStarttime(round_id):
    script = "from src import model\n"
    script += "rounds = model.Round.query(model.Round.number == "+str(round_id)+").fetch()[0]\n"
    script += "print(rounds.starttime)\n"
    return console(script)

#returns 0 if no round is current
def getCurrentRoundNum(assignment):
    script = "from src import model\n"
    script += "assignments = model.Assignment.query(model.Assignment.name=='"+assignment.upper()+"').fetch()[0]\n"
    script += "print(assignments.current_round)\n"
    ans = console(script)
    if ans == "": ans = "0"
    return int(console(script))

def canAddInstructor():
    canAddInstructor.prev_inst_num += 1
    start_count = get_instructor_count()
    addInstructor('instructor'+str(canAddInstructor.prev_inst_num)+'@gmail.com')
    after_count = get_instructor_count()
    return (after_count != start_count)
canAddInstructor.prev_inst_num = 1000

def canToggleInstructor(email):
    toggleInstructor(email)
    afterToggle = isInstructorActive(email)
    #we toggle twice so the instructor goes back to the original toggle state
    toggleInstructor(email)
    afterToggle2 = isInstructorActive(email)
    return (afterToggle != afterToggle2)

def canToggleCourse(coursename):
    toggleCourse(coursename)
    afterToggle = isCourseActive(coursename)
    #we toggle twice so the instructor goes back to the original toggle state
    toggleCourse(coursename)
    afterToggle2 = isCourseActive(coursename)
    return (afterToggle != afterToggle2)

def canToggleAssignment(coursename,assignmentname):
    toggleAssignment(coursename,assignmentname)
    afterToggle = isAssignmentActive(coursename,assignmentname)
    #we toggle twice so the instructor goes back to the original toggle state
    toggleAssignment(coursename,assignmentname)
    afterToggle2 = isAssignmentActive(coursename,assignmentname)
    return (afterToggle != afterToggle2)


inst_directories = ["/courses","/group_responses","/groups","/responses","/rounds","/assignments","/students"]
std_directories = ["/student_home","/student_rounds"]
admin_directories = ["/admin"]
#leave a user type as None if you don't want to run tests for that user type
def testGET(admin,instructor,student,course,assignment,situation_string):
    print("\trunning GET tests for the situation <"+situation_string+">")
    #instructor GET testing
    if instructor is not None:
        login(instructor,False)
        #TEST to make sure instructor gets 200 when expected
        for dir in inst_directories:
            r = session.get("http://localhost:8080"+dir)
            if not "200" in str(r):
                print("\t\t\tFAILED (expected 200): instructor got <"+str(r)+"> when sending a GET request to <"+dir+"> when <"+situation_string+">")
            else:
                print("\t\t\tpassed: instructor got 200 for "+dir)
        #TEST to make sure instructor gets 401 as expected
        for dir in admin_directories:
            r = session.get("http://localhost:8080"+dir)
            if not "401" in str(r):
                print("\t\t\tFAILED (expected 401): instructor got <"+str(r)+"> when sending a GET request to <"+dir+"> when <"+situation_string+">")
            else:
                print("\t\t\tpassed: instructor got 401 for "+dir)
        logout()
    #student GET testing
    if student is not None:
        login(student,False)
        #TEST to make sure student gets 200 when expected
        for dir in std_directories:
            #we need to treat /student_rounds differently because the GET request url contains the assignment key
            if dir == "/student_rounds":
                keys = get_assignment_key_list()
                if len(keys) > 0:
                    r = student_rounds_get(keys[0])
                    if not "200" in str(r):
                        print("\t\t\tFAILED (expected 200): student got <"+str(r)+"> when sending a GET request to <"+dir+"> when <"+situation_string+">")
                    else:
                        print("\t\t\tpassed: student got 200 for "+dir)
            else:
                r = session.get("http://localhost:8080"+dir)
                if not "200" in str(r):
                    print("\t\t\tFAILED (expected 200): student got <"+str(r)+"> when sending a GET request to <"+dir+"> when <"+situation_string+">")
                else:
                    print("\t\t\tpassed: student got 200 for "+dir)
        #TEST to make sure student gets 401 as expected
        for dir in inst_directories:
            r = session.get("http://localhost:8080"+dir)
            if not ("302" in str(r.history) and "student_home" in r.url):
                print("\t\t\tFAILED (expected 302 to student_home): url response was <"+r.url+">, history was <"+str(r.history)+"> when sending a GET request to <"+dir+"> when <"+situation_string+">")
            else:
                print("\t\t\tpassed: student got 302, 200 for "+dir)
        #TEST to make sure student gets 401 as expected
        for dir in admin_directories:
            r = session.get("http://localhost:8080"+dir)
            if not "401" in str(r):
                print("\t\t\tFAILED (expected 401): student got <"+str(r)+"> when sending a GET request to <"+dir+"> when <"+situation_string+">")
            else:
                print("\t\t\tpassed: student got 401 for "+dir)
        logout()
    #admin GET testing
    if admin is not None:
        login(admin,True)
        #TEST to make sure admin gets 200 when expected
        for dir in admin_directories:
            r = session.get("http://localhost:8080"+dir)
            if not "200" in str(r):
                print("\t\t\tFAILED (expected 200): admin got <"+str(r)+"> when sending a GET request to <"+dir+"> when <"+situation_string+">")
            else:
                print("\t\t\tpassed: admin got 200 for "+dir)
        logout()

#==================[END: prepare to run tests]==================



import admin, students, courses, assignments, rounds, groups, GETtests   
    
   


#==================[END: run tests]==================
