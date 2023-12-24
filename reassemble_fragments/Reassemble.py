# File: Reassemble.py
# -------------------
# This file exports a program that reads in a large number
# of text fragments from a file you choose, and then reconstructs
# the original text so it can be printed out.

from filechooser import chooseInputFile

# Function: extractFragments
# Reads the file and splits the fragments based on '{'. Removes the
# bracket and filters out empty fragments
def extractFragments(filename):
   data = open(filename).read().split('{')
   fragments = []
   for item in data:
      new_data = item.split("}")[0]
      if len(new_data) > 0:
         fragments.append(new_data)
   return fragments

# Function: find_overlap
# Takes in two fragments and finds the overlapping letters between the
# two. Checks if the fragments are included in each other, finds the
# maximum possible overlap, checks if there is an overlap, and returns the
# result.
def find_overlap(frag1, frag2):
   if frag1 in frag2:
      return len(frag1), frag2, frag2
   if frag2 in frag1:
      return len(frag2), frag1, frag1
   max_overlap = min(len(frag1), len(frag2)) - 1
   for overlap in range(max_overlap, 0, -1):
      if frag1[:overlap] == frag2[-overlap:]:
         merge = frag2 + frag1[overlap:]
         return overlap, frag1[:overlap], merge
      if frag2[:overlap] == frag1[-overlap:]:
         merge = frag1 + frag2[overlap:]
         return overlap, frag2[:overlap], merge
   # If no overlap is found
   return 0, "", ""

# Function: reconstruct
# Takes in the fragments and merges them to produce the final reassembled fragment
def reconstruct(fragments):
   while len(fragments) > 1:
      largest_overlap_position = [0, 0]
      largest_overlap_size = 0
      largest_overlap = ''
      merge = ''
      # Compares the fragment pairs to find the largest overlap
      for i in range(len(fragments) - 1):
         for j in range(i + 1, len(fragments)):
            # When the length of the fragment string is less than the longest common string, it does not need to be checked
            if len(fragments[i]) < largest_overlap_size or len(fragments[j]) < largest_overlap_size:
               continue
            overlap_size, common_word, merged = find_overlap(fragments[i], fragments[j])
            if overlap_size > largest_overlap_size:
               largest_overlap_position = [i, j]
               largest_overlap = common_word
               largest_overlap_size = overlap_size
               merge = merged
      # Updates the fragments based on the largest overlap that was found
      if largest_overlap_size > 0:
         fragments[largest_overlap_position[0]] = merge
      else:
         fragments[largest_overlap_position[0]] += fragments[largest_overlap_position[1]]
      # Remove the entries that are not the first
      fragments.pop(largest_overlap_position[1])
   return fragments[0]

def Reassemble():
   filename = chooseInputFile("reassemble-files")
   if filename == "":
      print("User canceled file selection. Quitting!")
      return
   fragments = extractFragments(filename)
   if fragments == None:
      print("File didn't respect reassemble file format. Quitting!")
      return
   reconstruction = reconstruct(fragments)
   print(reconstruction)

if __name__ == "__main__":
   Reassemble()

