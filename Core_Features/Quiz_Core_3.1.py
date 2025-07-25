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
    question_answer_list = []
    with open("Core_Features/QuestionBank.txt", 'r') as question_file:
        for line in question_file:
            if ',' in line:
                question, answer = line.strip().split(',', 1)
                question_answer_list.append((question, answer))
    return question_answer_list

