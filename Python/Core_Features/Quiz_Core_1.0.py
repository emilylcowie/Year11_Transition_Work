# ######################################
# Date:             25/07/2025         #
# Time Started:     22:19              #
# Time Taken:       8 Minutes          #
# To Do:           "Greet the user and #
#                   explain the rules" #
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