# #####################################################
# Date:             01/09/2025                        #
# Time Started:     16:57                             #
# To Do:            Let the user choose a category    #
#######################################################

import random
import sys
import signal
import time


# -------------------- Utility Functions --------------------

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
    except Exception:
        print(info)


# -------------------- Question Class --------------------

class Question:
    def __init__(self, category, text, choices, answer):
        self.category = category
        self.text = text
        self.choices = choices
        self.answer = answer

    def is_correct(self, user_input):
        letter_to_index = {'a': 0, 'b': 1, 'c': 2, 'd': 3}
        if user_input in letter_to_index:
            return self.choices[letter_to_index[user_input]] == self.answer
        return user_input.strip().lower() == self.answer.strip().lower()


# -------------------- Quiz Class --------------------

class Quiz:
    def __init__(self, question_file):
        self.categories = ["80's Music", 'Coffee', 'David Bowie',
                           'Harry Potter', 'Houseplants', 'Language', 'Programming', 'Sport']
        self.questions = self.load_questions(question_file)

    def load_questions(self, filepath):
        question_list = []
        with open(filepath, 'r') as f:
            for line in f:
                if ',' in line:
                    parts = line.strip().split(',', 3)
                    category, text, raw_choices, answer = parts
                    choices = raw_choices.split('|')
                    question_list.append(
                        Question(category, text, choices, answer))
        return question_list

    def filter_questions_by_category(self):
        while True:
            choice = character_input(
                f"Please choose a category from the following:\n - {'\n - '.join(self.categories)}   : ").lower()
            if choice not in [cat.lower() for cat in self.categories]:
                character_print("Invalid category. Please try again.")
            else:
                break
        return [q for q in self.questions if q.category.lower() == choice]


# -------------------- GameSession Class --------------------

class GameSession:
    def __init__(self, quiz):
        self.quiz = quiz
        self.score = 0
        self.total = 0

    def run(self):
        character_print("Welcome to this general knowledge quiz!")
        user = character_input("What is your name? ")

        question_type = character_input(
            "Would you like multiple choice questions? (y/n): ")
        questions = self.choose_question_type()
        self.ask_questions(question_type, questions)

    def choose_question_type(self):
        while True:
            choice = character_input(
                "Would you like to (a) choose a category or (b) shuffle the questions?\n")
            if choice.lower() == 'a':
                return self.quiz.filter_questions_by_category()
            elif choice.lower() == 'b':
                character_print("The questions will be shuffled!\n")
                return self.quiz.questions.copy()
            else:
                character_print("Invalid choice. Please try again.\n")

    def ask_questions(self, question_type, questions):
        pool = questions.copy()
        while pool:
            question = self.get_random_question(pool)
            self.ask_question(question, question_type)
            if not self.prompt_continue():
                break

    def get_random_question(self, pool):
        q = random.choice(pool)
        pool.remove(q)
        return q

    def ask_question(self, question, question_type):
        character_print(f"{self.total + 1}. {question.text}\n")
        if question_type.lower() == 'y':
            for i, choice in enumerate(question.choices):
                character_print(f"{chr(97 + i)}: {choice}")
        user_input = self.get_user_answer()
        self.evaluate(question, user_input)

    def get_user_answer(self):
        character_print("You have 5 seconds to answer!")
        signal.signal(signal.SIGALRM, time_up)
        signal.alarm(5)
        try:
            answer = character_input("\nYour answer: ")
            signal.alarm(0)
        except TimeoutException as e:
            character_print(e)
            answer = ""
        return answer

    def evaluate(self, question, user_input):
        if question.is_correct(user_input):
            character_print("Correct!\n")
            self.score += 1
        else:
            character_print(
                f"Incorrect! The correct answer was: {question.answer}\n")
        self.total += 1
        self.display_score()

    def display_score(self):
        character_print(
            f"Score: {self.score / self.total * 100:.2f}% ({self.score}/{self.total})")

    def prompt_continue(self):
        choice = character_input("\nClick to continue, or 'n' to quit: ")
        if choice.lower() == 'n':
            character_print(
                f"Final score: {self.score / self.total * 100:.2f}% ({self.score}/{self.total})")
            return False
        character_print("Next question...\n")
        return True


# -------------------- Main Execution --------------------

def main():
    quiz = Quiz("Text_Files/QuestionBank.txt")
    session = GameSession(quiz)
    session.run()


if __name__ == "__main__":
    main()
