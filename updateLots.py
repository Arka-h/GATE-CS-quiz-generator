import os
import csv
import random
from datetime import datetime
from itertools import chain
from collections import Counter
import time
import pickle
import re
# from read_pdf import getQ

# {sequence number: [0: Name of the subsection , 1: Number of questions]}
n = input("Enter Volume#: ")
vol = f"vol{n}"
m = 0
meta = {}
if os.path.exists(f"{vol}/csv/meta.csv"):
    with open(f"{vol}/csv/meta.csv", 'r') as f:
        for row in csv.reader(f):
            print(f"{row[0]}. {row[1]}    \t({row[2]})")
            meta[int(row[0])] = [row[1], int(row[2]), 0]
else:
    print(f"Add a meta file for {vol}!!")
    exit()
Q = {}

for x in [re.findall("([0-9]+)\.([0-9]+)\.([0-9]+)", s.strip())[0]
          for s in input("Enter question number(s)?\n").split(',')]:
    s, ss, q = int(x[0]), int(x[1]), int(x[2])
    if s in Q:
        Q[s].append((ss, q))
    else:
        Q[s] = [(ss, q)]

S = Q.keys()
# print("Q", Q)
# print("S", S)
c = ''

while not(c == 'a' or c == 'r'):
    c = input(
        "Do you want to add/remove the questions to the lot? (a-add, r-remove)\n")
print()
for s in S:  # For each section, check if the number is feasible
    data = {}
    lot = {}
    with open(f"{vol}/csv/section{s}.csv", 'r') as f:
        for row in csv.reader(f):
            data[row[0]] = row[1:]  # data['1.1'] = ['Balls in Bins',3]
    # Extract from data
    subSections = list(data.keys())  # subSections = ['1.1', '1.2', '1.3']
    # Check if there's an existing lot
    # If lot exists, get it
    if os.path.exists(f"{vol}/data/section{s}.lot"):
        with open(f'{vol}/data/section{s}.lot', 'rb') as f:
            lot = pickle.load(f)
            # print(lot)
            total = sum([len(lot[subsection])
                         for subsection in lot.keys()])
    else:  # Build the first lot
        lot = {sub_section: set([*range(int(data[sub_section][1]))])
               for sub_section in subSections}
        total = meta[s][1]
    print(f"Section{s}: remaining questions: {total}")
    # print(lot)
    for ss, q in Q[s]:
        if c == 'a':
            lot[f'{s}.{ss}'].add(q-1)  # Convert to 0 indexed
            print(f"added Q {s}.{ss}.{q}")
        elif c == 'r':
            lot[f'{s}.{ss}'].remove(q-1)  # Convert to 0 indexed
            print(f"removed Q {s}.{ss}.{q}")
    total = sum([len(lot[subsection])
                 for subsection in lot.keys()])
    print(f"Revised total for section{s} : {total}")
    print('Saving revised lot\n')
    with open(f'{vol}/data/section{s}.lot', 'wb') as f:
        pickle.dump(lot, f)
