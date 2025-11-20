# ######################################
# Date:             25/07/2025         #
# Time Started:     22:29              #
# Time Taken:       20 minutes         #
# To Do:           "Question Bank"     #
########################################

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
    try:
        with open("Core_Features/QuestionBank.txt", 'r') as question_file:
            content = question_file.read()
            if content.strip():
                print(content)
            else:
                print("No questions found in QuestionBank.txt.")
    except FileNotFoundError:
        print("Error: QuestionBank.txt not found. Please check the file path.")

questions()