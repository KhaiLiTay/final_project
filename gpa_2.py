import os, sys, bisect, pickle, statistics
import matplotlib.pyplot as plt

CLEARCMD = 'cls' #vscode change to 'clear'

benchmark_percentage = [0, 50, 60, 63, 67, 70, 73, 77, 80, 85, 90] 
benchmark_gpa = [0.0, 1.0, 1.7, 2.0, 2.3, 2.7, 3.0, 3.3, 3.7, 4.0, 4.3]
benchmark_letter = ['F', 'D', 'C-', 'C', 'C+', 'B-', 'B', 'B+', 'A-', 'A', 'A+']

class Course:
  def __init__(self, name, credits, weights):
    self.name = name
    self.credits = credits
    self.weights = weights
    self.scores = dict.fromkeys(weights, None)
    self.goal = 60

  @property
  def grades(self):
    percentage_grade = sum([v * self.weights[k] / 100 for k, v in self.scores.items() if v != None])
    rounded_grade = round(percentage_grade)
    grade_position = bisect.bisect_right(benchmark_percentage, rounded_grade)
    letter_grade = benchmark_letter[grade_position - 1]
    gpa_grade = benchmark_gpa[grade_position - 1]
    return rounded_grade, letter_grade, gpa_grade

  @property
  def passing(self):
    percentage_grade = self.grades[0]
    none_weights = sum([self.weights[k] for k, v in self.scores.items() if v == None])
    delta_goal = 0
    if none_weights > 0:
      delta_goal = (self.goal - percentage_grade) * 100 / none_weights 
    else:
      delta_goal = self.goal - percentage_grade
    return delta_goal

courses = {}
try:  #already existed file
  with open('gpa_save.pkl', 'rb') as save:
    courses = pickle.load(save)
  sys.stdout.write("Welcome back!")  #open existed file

except FileNotFoundError: #the file does not exist
  sys.stdout.write('uwu no save found~ but you cant see this message~')

while True:
  os.system(CLEARCMD)
  
  print()
  print('——————————— courses ————————————')
  if len(courses) == 0:
    print('no courses added yet~')
    print()
  else:
    for course in courses.values():
      g1, g2, g3 = course.grades
      print(f'{course.name} ({course.credits} creds): {g1}% | {g3} | {g2}')
      for item, score in course.scores.items():
        print(f' - {item} ({course.weights[item]}%): {score}%')
      print(f'{course.goal}% (goal) - {course.goal - course.passing}% (w_avg) = {course.passing}% to reach goal')
      print()

    t_credits = sum([i.credits for i in courses.values()])
    t_score = statistics.mean([i.grades[0] for i in courses.values()])
    t_gpa = statistics.mean([i.grades[2] for i in courses.values()])
    print(f'total ({t_credits}): {round(t_score)}% | {t_gpa}')
    print()

  print('——————————— commands ———————————')
  print(': add [name] [credits] [weights]')
  print(': set [course] [item] [score]')
  print(': goal [course] [score]')
  print(': chart')
  print(': q')
  print()

  print('————————————————————————————————')
  params = input(': ').split(' ')

  match params[0]:
    case 'add':
      try:
        if len(params) < 5:
          raise ValueError("Insufficient parameters. The format should be like this:\nadd Calculus 3 midterm 50 final 50")

        name, credits, *temp = params[1:]
        weights = {}

        if not isinstance(name, str):
          raise TypeError("Invalid course name. The name must be a string, e.g., Calculus")

        try:
          credits = int(credits)
        except ValueError:
          raise ValueError("Invalid credit value. Credit must be a number, e.g., 3")

        for i in range(0, len(temp), 2):
          try:
            item = temp[i]
            score = temp[i + 1]
            if not isinstance(item, str):
              raise TypeError("Invalid weight item. The item must be a string, e.g., midterm")
            if not score.isdigit():
              raise TypeError("Invalid weight score. The score must be an integer, e.g., 50")
            weights[item] = int(score)
          except (IndexError, TypeError):
            sys.stderr.write("The format of weights should be like this: midterm 50\n")
            sys.stderr.write("You can enter more than one weight, e.g., midterm 50 final 50\n\n")
            raise

        courses[name] = Course(name, int(credits), weights)
      except (ValueError, TypeError) as e:
        sys.stderr.write(str(e) + "\n\n")
      except:
        sys.stderr.write("The format of a record should be like this:\n")
        sys.stderr.write("add Calculus 3 midterm 50 final 50\n\n")
 
    case 'set':
      try:
        if len(params) < 4:
          raise ValueError("Invalid number of parameters. The format should be like this:\nset Calculus midterm 100")

        name, item, score = params[1:]
        if name not in courses:
          raise ValueError("Course not found. Please make sure the course exists.")

        if item not in courses[name].scores:
          raise ValueError("Item not found. Please make sure the item exists for the course.")

        try:
          courses[name].scores[item] = int(score)       
        except ValueError:
          raise ValueError("Invalid score. The score should be a number, e.g., 100")
      
      except (ValueError, KeyError) as e:
        sys.stderr.write(str(e) + "\n\n")
      except:
        sys.stderr.write("The format should be like this:\n")
        sys.stderr.write("set Calculus midterm 100\n\n")

    case 'goal':
      try:
        if len(params) < 3:
          raise ValueError("Invalid number of parameters. The format should be like this:\ngoal Calculus 80")

        name, score = params[1:]
        if name not in courses:
          raise ValueError("Course not found. Please make sure the course exists.")

        try:
          courses[name].goal = int(score)
        except ValueError:
          raise ValueError("Invalid goal. The goal should be a number, e.g., 80")
      except (ValueError, KeyError) as e:
          sys.stderr.write(str(e) + "\n\n")
      except:
          sys.stderr.write("The format should be like this:\n")
          sys.stderr.write("goal Calculus 80\n\n")


    case 'chart':
      course_names = list(courses.keys())
      course_scores = [course.grades[0] for course in courses.values()]

      plt.bar(course_names, course_scores)
      plt.xlabel('Course')
      plt.ylabel('Percentage Grade')
      plt.title('Grades for Courses')
      plt.xticks(rotation=45)
      plt.show()

    case 'q':
      with open('gpa_save.pkl', 'wb') as save:
        pickle.dump(courses, save, pickle.HIGHEST_PROTOCOL)
      os.system(CLEARCMD)
      exit()
    
    case _:
        sys.stderr.write("Invalid command\n\n")
        
  input('Press Enter to continue...')
