# File: GenerateRandomSentences.py
# --------------------------------
# This file exports a program that reads in a grammar file and
# then prints three randomly generated sentences

from filechooser import chooseInputFile
from random import choice
# Function: readGrammar
# Opens and reads in the grammar file.
def readGrammar(filename):
   with open(filename) as file:
      non_terminal = ''
      grammar = dict()
      # Check each line in the file
      for line in file:
         try:
            # Do not check the lines that contain integers since we do not want
            # that in the output
            x = int(line)
            continue
         except ValueError as e:
            pass
         # If the line has no text, then reset the non-terminal
         if line == '\n':
            non_terminal = ''
         # If the current non-terminal is empty, it is the first non-terminal
         elif non_terminal == '':
            non_terminal = line.strip()
            grammar[non_terminal] = []
         else:
            grammar[non_terminal].append(line.strip())
   return grammar

# Function: generateRandomSentence
# Given the grammar file, generates a random sentence. Starts with the <start>
# non-terminal, finds the next non-terminal and then replaces it with a randomized
# choice.
def generateRandomSentence(grammar):
   sentence = choice(grammar['<start>'])
   non_terminal = next_non_terminal(sentence, grammar)
   while len(non_terminal) > 0:
      random_choice = choice(grammar[non_terminal])
      sentence = sentence.replace(non_terminal, random_choice)
      non_terminal = next_non_terminal(sentence, grammar)
   return sentence

# Function: next_non_terminal
# Finds the next non_terminal by looking at the grammar
def next_non_terminal(sentence, grammar):
   for keyword in grammar:
      if keyword in sentence:
         return keyword
   return ''

def GenerateRandomSentences():
   filename = chooseInputFile("grammars")
   grammar = readGrammar(filename)
   # Produces the three random sentences and prints it
   for i in range(3):
      print(generateRandomSentence(grammar))

if __name__ == "__main__":
   GenerateRandomSentences()
