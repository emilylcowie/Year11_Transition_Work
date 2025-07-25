# ################################################
# Date:             25/07/2025                   #
# Time Started:     22:29                        #
# Time Taken:                                    #
# To Do:           "Store at least 5 questions   #
#                   and answers (use lists or    #
#                   a list of tuples)."          # 
##################################################

def Welcome_Message():
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
    with open("Core_Features/QuestionBank.txt", 'r') as question_file:
        questions = question_file.readlines()

def answers():
    with open("Core_Features/AnswerBank.txt", 'r') as answer_file:
        answers = answer_file.readlines()