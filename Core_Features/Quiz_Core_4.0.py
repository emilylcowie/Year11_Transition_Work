# ################################################
# Date:             26/07/2025                   #
# Time Started:     10:07                        #
# Time Taken:       16 minutes                   #
# To Do:           "Ask questions"               # 
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
    with open("Text_Files/QuestionBank.txt", 'r') as question_file:
        for line in question_file:
            if ',' in line:
                question, answer = line.strip().split(',', 1)
                question_answer_list.append((question, answer))
    return question_answer_list

def ask_questions():
    question_number = random.randint(0, len(questions()) - 1)
    print(questions()[question_number][0])

def main():
    welcome_message()
    ask_questions()
