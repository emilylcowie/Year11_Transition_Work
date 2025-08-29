# ################################################
# Date:             29/08/2025                   #
# Time Started:     15:18                        #
# Time Taken:        minutes                     #
# To Do:           "Multiple Choice Format"      # 
##################################################

import os

class Quiz:
    def __init__(self, question_file):
        self.questions = self.load_questions(question_file)
        self.score = 0
        self.total = 0

    def load_questions(self, filepath):
        question_answer_list = []
        with open(filepath, 'r') as f:
            for line in f:
                if ',' in line:
                    question, answer = line.strip().split(',', 1)
                    question_answer_list.append((question, answer))
        return question_answer_list

    def welcome_message(self):
        print("Welcome to this general knowledge quiz!")
        user = input("What is your name? ")
        question_type = input("Would you like multiple choice questions or not? y/n")
        if question_type.lower() == 'y':
            print("You have chosen multiple choice questions.")
        else:
            print("You have chosen not to have multiple choice questions.")
        print(f'''
Welcome {user}! Here are the rules:
- You will be asked different questions, all with one word answers
- You will answer with one word
- You will be marked and scored with each question
- You can choose to leave the game at any point

Your Score is currently 0.
Let's get started!
''')

    def ask_questions(self):
        for question, answer in self.questions:
            print(question)
            user_input = input("Your answer: ")
            if self.check_answer(user_input, answer):
                print("Correct!")
                self.score += 1
            else:
                print(f"Incorrect! The correct answer was: {answer}")
            self.total += 1
            print(f"Score: {self.score / self.total * 100:.2f}% ({self.score}/{self.total})")
            exit = input("Do you want to continue? (yes/no): ")
            if exit.lower() == 'no':
                print(f"Thank you for playing! Your final score is: {self.score / self.total * 100:.2f}% ({self.score}/{self.total})")
                break
            else:
                print("Next question...\n")

    def check_answer(self, user_input, correct_answer):
        return user_input.lower() == correct_answer.lower()

def main():
    quiz = Quiz("Text_Files/QuestionBank.txt")
    quiz.welcome_message()
    print("\nHere is your first question:")
    quiz.ask_questions()

if __name__ == "__main__":
    main()