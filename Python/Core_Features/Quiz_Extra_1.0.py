# #####################################################
# Date:             29/08/2025                        #
# Time Started:     15:18                             #
# Time Taken:        minutes                          #
# To Do:          Randomized Questions but prevent    #
#                 same questions being asked multiple #
#                 times in one session                #
#######################################################

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
                    question, choices, answer = line.strip().split(',', -1)
                    if '|' in choices:
                        choices = choices.strip().split('|', -1)
                    question_answer_list.append((question, choices, answer))
        return question_answer_list

    def welcome_message(self):
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

    def ask_questions(self, question_type):
        for question, choices, answer in self.questions:
            print(f'{self.total+1}. {question}\n')
            if question_type.lower() == 'y':
                for i in choices:
                    print('-',i)
            user_input = input("\nYour answer: ")
            if self.check_answer(user_input, answer):
                print("Correct!\n")
                self.score += 1
            else:
                print(f"Incorrect! The correct answer was: {answer}")
            self.total += 1
            print(f"Score: {self.score / self.total * 100:.2f}% ({self.score}/{self.total})")
            exit = input("\nDo you want to continue? (y/n): ")
            if exit.lower() == 'n':
                print(f"Thank you for playing! Your final score is: {self.score / self.total * 100:.2f}% ({self.score}/{self.total})")
                break
            else:
                print("Next question...\n")

    def check_answer(self, user_input, correct_answer):
        return user_input.lower() == correct_answer.lower()

def main():
    quiz = Quiz("../Text_Files/QuestionBank.txt")
    quiz.welcome_message()
    quiz.ask_questions(input("Would you like multiple choice questions? (y/n): "))

if __name__ == "__main__":
    main()