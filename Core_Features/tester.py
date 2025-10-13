choices = []

with open('Text_Files/QuestionBank.txt', 'r') as f:
    for line in f:
        if ',' in line:
            parts = line.strip().split(',', 3)
            category, text, raw_choices, answer = parts
            choices.append(raw_choices.split('|'))
            print(text)