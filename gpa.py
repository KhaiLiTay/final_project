#gpa部分已可以完全運行
#卻美化

#!/usr/bin/python3

import sys 

# 成績對應等級的標準和GPA
grade_benchmark = {'A+': 90, 'A': 85, 'A-':80, 'B+':77, 'B':73, 'B-':70, 'C+':67, 'C':63, 'C-':60, 'D':50, 'F':0}
gpa_benchmark = {'A+': 4.3, 'A': 4.0, 'A-':3.7, 'B+':3.3, 'B':3.0, 'B-':2.7, 'C+':2.3, 'C':2.0, 'C-':1.7, 'D':1.0, 'F':0.0}

class Course:
    def __init__(self, name, credit):
        # 初始化課程的屬性
        self._name = name
        self._credit = credit
        self._grading = {}  # 評分項目及其比例
        self._scores = {}   # 評分項目的分數
        self._final_score = 0   # 最終得分
        self._gpa = 0.0    # GPA
        self._grade = 'X'  # 等級
   
    def view(self):
        # 顯示課程的相關資訊，包括課程名稱、學分、各評分項目及其分數、最終得分、GPA和等級
        print("")
        print("==========================")
        print(f'Course Name: {self._name} , Credit: {self._credit}')
        print("==========================")
        #print("Description" + '\t' + "Ratio" + '\t' + "Score")
        #print("===========        ======    =====")
        for descr, ratio in self._grading.items():
            score = self._scores[descr]
            print(f'{descr} ({ratio}%): {score:}%')
        self.set_final_score()  # 計算最終得分
        self.set_gpa()  # 計算GPA
        print("==========================")
        print(f'Final Score : {self._final_score}')
        print(f'GPA : {self._gpa}   Grade : {self._grade}')
        print("==========================")

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
        # 根據評分項目的分數和比例計算最終得分
        total = 0
        for desc, ratio in self._grading.items():
            score = self._scores[desc]
            total += score * (ratio / 100)
        self._final_score = total
       
    def set_gpa(self):
        # 根據最終得分計算對應的等級和GPA
        closest_grade = None
        closest_point_diff = float('inf')

        for grade, point in grade_benchmark.items():
            point_diff = abs(self._final_score - point)
            if point_diff < closest_point_diff:
                closest_point_diff = point_diff
                closest_grade = grade

        if closest_grade:
            self._grade = closest_grade
            self._gpa = gpa_benchmark[closest_grade]

    def set_scores(self, descr, score):
        # 設定評分項目的分數
        self._scores[descr] = score

    def add_grading(self, descr, ratio):
        # 新增評分項目及其比例
        self._grading[descr] = ratio
        self._scores[descr] = 0

class Courses:
    def __init__(self):
        self._courses = []  # 課程列表
        self._credits = 0   # 總學分
        self._gpa = 0.0     # GPA

    def add(self):
        # 新增課程
        while True:
            course_name = input("\n'q' to terminate | Course Name  : ")
            if course_name == 'q': break
            course_credit = int(input("Credit  : "))
            self._courses.append(Course(course_name, course_credit))
            self._credits += course_credit

    def add_gradings(self):
        # 為課程新增評分項目及其比例
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
        # 為課程新增評分項目的分數
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
        # 顯示所有課程的名稱和學分
        if len(self._courses) == 0:
            print("\nNo available records")
            return
        
        print("")
        for course in self._courses:
            print(f'{course.get_name} {course.get_credit}')
    
    def view_overall(self):
        # 顯示所有課程的總得分、GPA和等級
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
        # 顯示特定課程的詳細資訊
        while True:
            self.view()
            if self.empty: return
            course_name = input("\n'q' to terminate |[VIEW DETAIL] Course Name  : ")
            if course_name == 'q': break
            
            for course in self._courses:
                if course.get_name == course_name:
                    course.view()

    #TODO: function get seleceted course

    def set_overall_gpa(self):
        # 計算總GPA
        total_grade_points = 0
        total_credits = 0

        for course in self._courses:
            course.set_final_score()
            course.set_gpa()
            total_grade_points += (course._gpa * course._credit)
            total_credits += course._credit

        self._gpa = round(total_grade_points / total_credits, 2)

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
            courses.set_overall_gpa()
            courses.view_overall()
        elif cmd == "detail":
            courses.view_detail()
    elif cmd == "exit":
        break
    else:
        sys.stderr.write("Invalid Command")
