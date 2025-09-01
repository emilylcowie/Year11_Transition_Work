# #####################################################
# Date:             01/09/2025                        #
# Time Started:     12:43                             #
# To Do:            Let the user choose a category    #
#######################################################

import random
import sys
import signal
import time


class TimeoutException(Exception):
    pass


def time_up(signum, frame):
    raise TimeoutException("\nTime's up!")


def character_input(info):
    for char in info:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.020)
    return input()


def character_print(info):
    try:
        for char in info:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.020)
        print()
    except Exception as e:
        print(info)


class Quiz:
    def __init__(self, question_file):
        self.categories = ["80's Music", 'Coffee', 'David Bowie',
                           'Harry Potter', 'Houseplants', 'Language', 'Programming', 'Sport']
        self.questions = self.load_questions(question_file)
        self.num_of_qus = len(self.questions)
        self.score = 0
        self.total = 0

    def load_questions(self, filepath):
        question_answer_list = []
        with open(filepath, 'r') as f:
            for line in f:
                if ',' in line:
                    parts = line.strip().split(',', 3)
                    category = parts[0]
                    question = parts[1]
                    choices = parts[2].split('|') if parts[1] else []
                    answer = parts[3]
                    
                    choices[0] = "a:" + choices[0]
                    choices[1] = "b:" + choices[1]
                    choices[2] = "c:" + choices[2]
                    choices[3] = "d:" + choices[3]
                    print(choices)

                    question_answer_list.append(
                        (category, question, choices, answer))
        return question_answer_list

    def filter_questions_by_category(self):
        while True:
            choice = character_input(
                f"Please choose a category from the following:\n - {'\n - '.join(self.categories)}   : ").lower()
            if choice not in [cat.lower() for cat in self.categories]:
                character_print("Invalid category. Please try again.")
            else:
                break

        new_questions = []
        for category, question, choices, answer in self.questions:
            if choice.lower() == category.lower():
                new_questions.append((category, question, choices, answer))
        return new_questions

    def welcome_message(self):
        character_print("Welcome to this general knowledge quiz!")
        user = character_input("What is your name? ")
        # character_print(f'''
# Welcome {user}! Here are the rules:
# - You will be asked different questions, either multiple choice or not
# - You can choose which category you want, or shuffle the questions
# - You will be marked and scored with each question
# - You can choose to leave the game at any point

# Your Score is currently 0.
# Let's get started!
# ''')

    def choose_question_type(self):
        while True:
            choice = character_input(
                "Would you like to (a) choose a category or (b) shuffle the questions?\n")
            if choice.lower() == 'a':
                return self.filter_questions_by_category()
            elif choice.lower() == 'b':
                character_print("The questions will be shuffled!\n")
                return self.questions.copy()
            else:
                character_print("Invalid choice. Please try again.\n")

    def ask_questions(self, question_type, questions):
        questions_pool = questions.copy()
        while questions_pool:
            category, question, choices, answer = self.get_random_question(
                questions_pool)
            self.display_question(question, choices, question_type)
            self.update_score(self.get_user_answer_with_timeout(), answer)
            if not self.prompt_continue():
                break

    def get_random_question(self, questions_pool):
        random_qu = random.choice(questions_pool)
        questions_pool.remove(random_qu)
        return random_qu

    def display_question(self, question, choices, question_type):
        character_print(f'{self.total + 1}. {question}\n')
        if question_type.lower() == 'y':
            for choice in choices:
                character_print(f'- {choice}')

    def get_user_answer_with_timeout(self):
        character_print("You have 10 seconds to answer!")
        signal.signal(signal.SIGALRM, time_up)
        signal.alarm(10)
        try:
            user_input = character_input("\nYour answer: ")
            signal.alarm(0)
        except TimeoutException as e:
            character_print(e)
            user_input = ""
        except Exception as e:
            character_print(f"Unexpected error: {e}")
            user_input = ""
        return user_input

    def update_score(self, user_input, correct_answer):
        if self.check_answer(user_input, correct_answer):
            character_print("Correct!\n")
            self.score += 1
        else:
            self.incorrect_message(correct_answer)
        self.total += 1
        character_print(
            f"Score: {self.score / self.total * 100:.2f}% ({self.score}/{self.total})")

    def prompt_continue(self):
        exit_game = character_input("\nClick to continue, or 'n' to quit: ")
        if exit_game.lower() == 'n':
            character_print(
                f"Thank you for playing! Your final score is: {self.score / self.total * 100:.2f}% ({self.score}/{self.total})")
            return False
        else:
            character_print("Next question...\n")
            return True

    def check_answer(self, user_input, correct_answer):
        return user_input.strip().lower() == correct_answer.strip().lower()

    def incorrect_message(self, correct_answer):
        character_print(
            f"Incorrect! The correct answer was: {correct_answer}\n")

# --------------------------------------------------------------------------------------------------


def main():
    quiz = Quiz("Text_Files/QuestionBank.txt")
    quiz.welcome_message()
    quiz.ask_questions(
        character_input("Would you like multiple choice questions? (y/n): "), quiz.choose_question_type())


if __name__ == "__main__":
    main()
