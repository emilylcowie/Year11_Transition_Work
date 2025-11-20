# ################################################
# Date:             26/07/2025                   #
# Time Started:     09:45                        #
# Time Taken:       16 minutes                   #
# To Do:           "Store at least 5 questions   #
#                   and answers (use lists or    #
#                   a list of tuples)."          # 
##################################################

import random

def welcome_message():
    print("Welcome to this general knowledge quiz!")
    user = input("What is your name? ")
    print(f'''
Welcome {user}! Here are the rules:
- You will be asked different questions, all with one word answers
- You will answer with one word
- You will be marked and scored with each question
- You can choose to leave the game at any point
''')

def questions():
    question_answer_list = []
    with open("../Text_Files/QuestionBank.txt", 'r') as question_file:
        for line in question_file:
            if ',' in line:
                question, answer = line.strip().split(',', 1)
                question_answer_list.append((question, answer))
    return question_answer_list

#test
question_no1 = (questions()[0][0])
answer_no1 = (questions()[0][1])
print(question_no1)
print(answer_no1)