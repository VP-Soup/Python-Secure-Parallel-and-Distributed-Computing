"""
Name: Vicente James Perez
Date: 1/09/2020
Assignment: Module 1: Secret Code
Due Date: 1/10/2020
About this project: Using a dict structure, take user input and translate to "coded" version
Assumptions:NA
All work below was performed by Vicente James Perez
"""
import string

# create reverse alphabet for populating secret code dict
alphabet_reversed = string.ascii_uppercase[::-1]
# declare blank dict
secret_code = {}
# populate dict with alphabet mapped to reverse alphabet
for key in string.ascii_uppercase:
    for value in alphabet_reversed:
        secret_code[key] = value
        alphabet_reversed = alphabet_reversed[1:]
        break

# user prompt
input_string = input("Please input a string (alphabet characters only): ")
# validation
while input_string.isspace() or (input_string == ""):
    input_string = input("Error: invalid string, please enter a new string: ")

# declare new coded string bucket
coded_string = ""
# iterate through each char in input and concatenate val into coded_sgring
for char in input_string:
    if char.isalpha():
        coded_string += secret_code[char.upper()]
    else:
        coded_string += char
print(coded_string)
