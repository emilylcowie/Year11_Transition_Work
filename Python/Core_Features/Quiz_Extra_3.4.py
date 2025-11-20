# #####################################################
# Date:             01/09/2025                        #
# Time Started:     16:48                             #
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
            question_data = self.get_random_question(questions_pool)
            self.handle_single_question(question_data, question_type)
            if not self.prompt_continue():
                break

    def handle_single_question(self, question_data, question_type):
        category, question, choices, answer = question_data
        self.display_question(question, choices, question_type)
        user_input = self.get_user_answer_with_timeout()
        self.evaluate_answer(user_input, choices, answer)

    def evaluate_answer(self, user_input, choices, correct_answer):
        if self.check_answer(user_input, choices, correct_answer):
            character_print("Correct!\n")
            self.score += 1
        else:
            self.incorrect_message(correct_answer)
        self.total += 1
        self.display_score()

    def display_score(self):
        character_print(
            f"Score: {self.score / self.total * 100:.2f}% ({self.score}/{self.total})")

    def get_random_question(self, questions_pool):
        random_qu = random.choice(questions_pool)
        questions_pool.remove(random_qu)
        return random_qu

    def display_question(self, question, choices, question_type):
        character_print(f'{self.total + 1}. {question}\n')
        if question_type.lower() == 'y':
            letters = ['a', 'b', 'c', 'd']
            for i in range(0, len(choices)):
                character_print(f'{letters[i]}: {choices[i]}')

    def get_user_answer_with_timeout(self):
        character_print("You have 5 seconds to answer!")
        signal.signal(signal.SIGALRM, time_up)
        signal.alarm(5)
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

    def prompt_continue(self):
        exit_game = character_input("\nClick to continue, or 'n' to quit: ")
        if exit_game.lower() == 'n':
            character_print(
                f"Thank you for playing! Your final score is: {self.score / self.total * 100:.2f}% ({self.score}/{self.total})")
            return False
        else:
            character_print("Next question...\n")
            return True

    def check_answer(self, user_input, choices, correct_answer):
        letter_to_index = {'a': 0, 'b': 1, 'c': 2, 'd': 3}
        if user_input in letter_to_index:
            if choices[letter_to_index[user_input]] == correct_answer:
                return True
        elif user_input.strip().lower() == correct_answer.strip().lower():
            return True
        else:
            return False

    def incorrect_message(self, correct_answer):
        character_print(
            f"Incorrect! The correct answer was: {correct_answer}\n")

# --------------------------------------------------------------------------------------------------


def main():
    quiz = Quiz("../Text_Files/QuestionBank.txt")
    quiz.welcome_message()
    quiz.ask_questions(
        character_input("Would you like multiple choice questions? (y/n): "), quiz.choose_question_type())


if __name__ == "__main__":
    main()
