# ################################################
# Date:             26/07/2025                   #
# Time Started:     10:17                        #
# Time Taken:        minutes                   #
# To Do:           "Loop through the questions   #
#                   and get user input & check"  # 
##################################################

def welcome_message():
    print("Welcome to this general knowledge quiz!")
    user = input("What is your name? ")
    print(f'''
Welcome {user}! Here are the rules:
- You will be asked different questions, all with one word answers
- You will answer with one word
- You will be marked and scored with each question
- You can choose to leave the game at any point

Your Score is currently 0.
Let's get started!
''')

def questions():
    question_answer_list = []
    with open("../Text_Files/QuestionBank.txt", 'r') as question_file:
        for line in question_file:
            if ',' in line:
                question, answer = line.strip().split(',', 1)
                question_answer_list.append((question, answer))
    return question_answer_list

def ask_questions():
    score = 0
    total = 0
    for i in range(len(questions())):
        print(questions()[i][0])
        user_input = input("Your answer: ")
        if check_answer(user_input, questions()[i][1]):
            print("Correct!")
            score += 1
            total += 1
        else:
            print(f"Incorrect! The correct answer was: {questions()[i][1]}")
            total += 1
        print(f"Score: {score / total * 100:.2f}% ({score}/{total})")
        exit = input("Do you want to continue? (yes/no): ")
        if exit.lower() == 'no':
            print(f"Thank you for playing! Your final score is: {score / total * 100:.2f}% ({score}/{total})")
            break
        else:
            print("Next question...\n")

def check_answer(user_input, correct_answer):
    if user_input.lower() == correct_answer.lower():
        return True
    else:
        return False

def main():
    welcome_message()
    print("\nHere is your first question:")
    ask_questions()

main()