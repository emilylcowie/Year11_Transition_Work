# #####################################################
# Date:             01/09/2025                        #
# Time Started:     16:57                             #
# To Do:            Let the user choose a category    #
#######################################################

import random
import sys
import signal
import time
import csv

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
        csv_edit = CSVEdit(filepath)
        return csv_edit.get_questions()

    def filter_questions_by_category(self):
        while True:
            choice = character_input(
                f"\nPlease choose a category from the following:\n - {'\n - '.join(self.categories)}   : ").lower()
            if choice not in [cat.lower() for cat in self.categories]:
                character_print("Invalid category. Please try again.")
            else:
                self.categories.remove(choice.title())
                break
        return [qu for qu in self.questions if qu.category.lower() == choice]


# -------------------- GameSession Class --------------------

class Game:
    def __init__(self, quiz):
        self.quiz = quiz
        self.score = 0
        self.total = 0

    def run(self):
        character_print("\nWelcome to this general knowledge quiz!")
        user = character_input("\nWhat is your name? ")

        question_type = character_input(
            "\nWould you like multiple choice questions? (y/n): ")
        questions = self.choose_question_type()
        self.ask_questions(question_type, questions)

    def choose_question_type(self):
        while True:
            choice = character_input(
                "\nWould you like to (a) choose a category or (b) shuffle the questions?    ")
            if choice.lower() == 'a':
                return self.quiz.filter_questions_by_category()
            elif choice.lower() == 'b':
                character_print("The questions will be shuffled!\n")
                return self.quiz.questions.copy()
            else:
                character_print("Invalid choice. Please try again.\n")

    def ask_questions(self, question_type, questions):
        pool = questions.copy()
        while len(pool) > 0:
            question = self.get_random_question(pool)
            self.ask_question(question, question_type)
            if not self.prompt_continue():
                break
        character_print("Congrats for finishing one category!")
        if character_input("Press Enter to continue or press 'q' to quit.") == 'q':
            exit(
                f'Thank you for playing, your final score was {self.display_score()}')
        else:
            self.change_category()

    def change_category(self):
        self.quiz.filter_questions_by_category()

    def get_random_question(self, pool):
        q = random.choice(pool)
        pool.remove(q)
        return q

    def ask_question(self, question, question_type):
        character_print(f"\n\n{self.total + 1}. {question.text}\n")
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
            self.check_if_high_score(self.score)
            exit("Thank you for playing!")
        character_print("Next question...\n")
        return True

    def check_if_high_score(self, score):
        print(score)

# -------------------- CSVedit Class -------------------


class CSVEdit:
    def __init__(self, filename):
        self.questionList = []
        with open(filename, "r", encoding="latin1") as f:
            datareader = csv.reader(f, delimiter=',')
            for row in datareader:
                self.questionList.append(row)

    def get_questions(self):
        questions = []
        for row in self.questionList:
            if len(row) >= 6:
                category = row[0]
                text = row[1]
                choices = row[2:6]
                answer = row[6] if len(row) > 6 else ""
                questions.append(Question(category, text, choices, answer))
        return questions


# -------------------- Main Program --------------------

def main():
    quiz = Quiz('Questions.csv')
    session = Game(quiz)
    session.run()


if __name__ == "__main__":
    main()
