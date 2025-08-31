# #####################################################
# Date:             31/08/2025                        #
# Time Started:     15:41                             #
# To Do:            Add a countdown timer for each    #
#                   question using time.sleep().      #
#######################################################

import random
import time
import signal


class TimeoutException(Exception):
    pass


def time_up():
    raise TimeoutException("Time's up!")


class Quiz:
    def __init__(self, question_file):
        self.questions = self.load_questions(question_file)
        self.num_of_qus = len(self.questions)
        self.score = 0
        self.total = 0

    def load_questions(self, filepath):
        question_answer_list = []
        with open(filepath, 'r') as f:
            for line in f:
                if ',' in line:
                    parts = line.strip().split(',', 2)
                    question = parts[0]
                    choices = parts[1].split('|') if parts[1] else []
                    answer = parts[2]
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
        
    def get_random_question(self, questions_pool):
        random_qu = random.choice(questions_pool)
        questions_pool.remove(random_qu)
        return random_qu
    
    def get_user_answer_with_timeout(self):
        print("You have 5 seconds to answer!")
        signal.signal(signal.SIGALRM, time_up)
        signal.alarm(5)
        try:
            user_input = input("\nYour answer: ")
            signal.alarm(0)
        except TimeoutException as e:
            print(e)
            user_input = ""
        except Exception as e:
            print("Unexpected error:", e)
            user_input = ""
        return user_input

    def ask_questions(self, question_type):
        questions_pool = self.questions.copy()
        while questions_pool:
            question, choices, answer = self.get_random_question(questions_pool)
            self.display_question(question, choices, question_type)
            self.update_score(self.get_user_answer_with_timeout(), answer)
            if not self.prompt_continue():
                break

    def display_question(self, question, choices, question_type):
        print(f'{self.total + 1}. {question}\n')
        if question_type.lower() == 'y' and choices:
            for choice in choices:
                print('-', choice)

    def update_score(self, user_input, correct_answer):
        if self.check_answer(user_input, correct_answer):
            print("Correct!\n")
            self.score += 1
        else:
            self.incorrect_message(correct_answer)
        self.total += 1
        print(f"Score: {self.score / self.total * 100:.2f}% ({self.score}/{self.total})")

    def prompt_continue(self):
        exit_game = input("\nClick to continue, or 'n' to quit: ")
        if exit_game.lower() == 'n':
            print(f"Thank you for playing! Your final score is: {self.score / self.total * 100:.2f}% ({self.score}/{self.total})")
            return False
        else:
            print("Next question...\n")
            return True

    def check_answer(self, user_input, correct_answer):
        return user_input.strip().lower() == correct_answer.strip().lower()

    def incorrect_message(self, correct_answer):
        print(f"Incorrect! The correct answer was: {correct_answer}\n")


def main():
    quiz = Quiz("Text_Files/QuestionBank.txt")
    print(quiz.num_of_qus)
    quiz.welcome_message()
    quiz.ask_questions(
        input("Would you like multiple choice questions? (y/n): "))


if __name__ == "__main__":
    main()
