#!/usr/bin/python3

import sys 
grade_benchmark = {'A+': 90, 'A': 85, 'A-':80, 'B+':77, 'B':73, 'B-':70, 'C+':67, 'C':63, 'C-':60, 'D':50, 'E':0}
gpa_benchmark = {'A+': 4.3, 'A': 4.0, 'A-':3.7, 'B+':3.3, 'B':3.0, 'B-':2.7, 'C+':2.3, 'C':2.0, 'C-':1.7, 'D':0.0, 'E':0.0}
class Course:
    def __init__(self, name, credit):
        self._name = name
        self._credit = credit
        self._grading = {}
        self._scores = {}
        self._final_score = 0
        self._gpa = 0.0
        self._grade = 'X'
    
    def view(self):
        print("")
        print(f'Course Name: {self._name} , Credit: {self._credit}')
        for descr, ratio in self._grading.items():
            score = self._scores[descr]
            print(f'{descr} ({ratio}%): {score}%')
        self.set_final_score()
        self.set_gpa()
        print(f'Final Score : {self._final_score}')
        print(f'GPA : {self._gpa}   Grade : {self._grade}')

    @property
    def get_name(self):
        return self._name
    @property
    def get_credit(self):
        return self._credit
    @property
    def get_grading(self):
        return self._grading
    @property
    def get_final_score(self):
        return self._final_score
    @property
    def get_gpa(self):
        return self._gpa
    
    def set_final_score(self):
        total = 0
        for desc, ratio in self._grading.items():
            score = self._scores[desc]
            total += score * (ratio / 100)
        self._final_score = total

    def set_gpa(self):
        for grade, point in grade_benchmark.items():
            self.set_final_score()
            if self._final_score >= point:
                self._grade = grade
                self._gpa = gpa_benchmark[grade]
                break

    def set_scores(self, descr, score):
        self._scores[descr] = score

    def add_grading(self, descr, ratio):
        self._grading[descr] = ratio
        self._scores[descr] = 0

class Courses:
    def __init__(self):
        self._courses = []
        self._credits = 0
        self._gpa = 0.0

    def add(self):
        while True:
            course_name = input("\n'q' to terminate | Course Name  : ")
            if course_name == 'q': break
            course_credit = int(input("Credit  : "))
            self._courses.append(Course(course_name, course_credit))
            self._credits += course_credit

    def add_gradings(self):
        while True:
            self.view()
            course_name = input("\n'q' to terminate |[ADD GRADING] Course Name  : ")
            if course_name == 'q': break
            
            for course in self._courses:
                if course.get_name == course_name:
                    while True:
                        descr = input("'q' to terminate | Grading Description  : ")
                        if descr == 'q': break
                        ratio = int(input("Ratio  : "))
                        course.add_grading(descr, ratio)

    def add_scores(self):
        while True:
            self.view()
            course_name = input("\n'q' to terminate |[ADD SCORES] Course Name  : ")
            if course_name == 'q': break
            
            for course in self._courses:
                if course.get_name == course_name:
                    course.view()
                    for descr, ratio in course.get_grading.items():
                        score = int(input(f'{descr} ({ratio}%) score  : '))
                        course.set_scores(descr, score)

    def view(self):
        if len(self._courses) == 0:
            print("\nNo available records")
            return
        
        print("")
        for course in self._courses:
            print(f'{course.get_name} {course.get_credit}')
    
    def view_overall(self):
        if len(self._courses) == 0:
            print("\nNo available records")
            return
        

        print("")
        print(f"Current GPA  : {self._gpa}")
        for course in self._courses:
            course.set_final_score()
            course.set_gpa()
            print(f'{course.get_name} (credit = {course.get_credit})  : {course.get_final_score}   , GPA : {course.get_gpa}')

    def view_detail(self):
        while True:
            self.view()
            if self.empty: return
            course_name = input("\n'q' to terminate |[VIEW DETAIL] Course Name  : ")
            if course_name == 'q': break
            
            for course in self._courses:
                if course.get_name == course_name:
                    course.view()

    #TODO: function get seleceted course

    def set_gpa(self):
        for course in self._courses:
            tmp += course.get_gpa * (course.get_credit / self._credits)
        self._gpa = tmp

    @property
    def empty(self):
        return len(self._courses) == 0

courses = Courses()
while True:
    cmd = input("\nadd / view / exit  : ")
    if cmd == "add":
        if not courses.empty:
            while True:
                cmd = input("\n[ADD] course / grading / scores / back : ")
                if cmd == "course":
                    courses.add()
                elif cmd == "grading":
                    courses.add_gradings()
                elif cmd == "scores":
                    courses.add_scores()
                elif cmd == "back":
                    break
        else:
            courses.add()
    elif cmd == "view":
        cmd = input("\n[VIEW] all / detail  : ")
        if cmd == "all":
            courses.view_overall()
        elif cmd == "detail":
            courses.view_detail()
    elif cmd == "exit":
        break
    else:
        sys.stderr.write("Invalid Command")
