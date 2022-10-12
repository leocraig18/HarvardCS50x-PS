# TODO
from cs50 import get_string

# Create functions to calculate the number of letters and scentences


def count_chars(text):
    letters = 0
    for i in text:
        if i.isalpha():
            letters = letters + 1
    return letters


def count_scentences(text):
    scentences = 0
    for i in text:
        if i == "." or i == "!" or i == "?":
            scentences = scentences + 1
    return scentences

# Prompt User for Input.


text = get_string("Text: ")

# Define variables for calculatina nd call functions.
letters = count_chars(text)
words = len(text.split())
scentences = count_scentences(text)

# Calculation for grading
calculation = float((0.0588 * letters / words * 100) - (0.296 * scentences / words * 100) - 15.8)
index = round(calculation)

# Conditions for print statement.

if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print(f"Grade {index}")