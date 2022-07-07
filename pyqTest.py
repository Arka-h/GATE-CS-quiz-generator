import os
import csv
import random
from datetime import datetime
from itertools import chain
from collections import Counter
import time
import pickle
from read_pdf import getQ

# {sequence number: [0: Name of the subsection , 1: Number of questions]}
n = input("Enter Volume#: ")
vol = f"vol{n}"
m = 0
meta = {}
if os.path.exists(f"{vol}/md/meta.md"):
    with open(f"{vol}/md/meta.md", 'r') as f:
        for row in csv.reader(f):
            print(f"{row[0]}. {row[1]}    \t({row[2]})")
            meta[int(row[0])] = [row[1], int(row[2]), 0]
else:
    print(f"Add a meta file for {vol}!!")
    exit()

S = list(map(int, [s.strip()
                   for s in input("Which section(s)?\n").split(',')]))
while True:
    m = int(input("Enter the number of questions: "))
    section_order = random.choices(S, weights=[meta[s][1] for s in S], k=m)
    dist = dict(Counter(section_order))  # distribution
    bal = 0
    for s in S:  # For each section, check if the number is feasible
        lot = {}
        # Check if there's an existing lot
        # If lot exists, get it
        if os.path.exists(f"{vol}/data/section{s}.lot"):
            with open(f'{vol}/data/section{s}.lot', 'rb') as f:
                lot = pickle.load(f)
                total = sum([len(lot[subsection])
                             for subsection in lot.keys()])
        else:  # Build the first lot
            total = meta[s][1]
        print(f"Section{s}: total remaining questions: {total}")
        diff = ((total-dist[s]) if s in dist else total)
        meta[s][2] = diff  # Save the diff
        bal += diff
    if bal >= 0:
        break
    print("Please enter different number of questions")
count_neg = - sum([meta[s][2] if meta[s][2] < 0 else 0 for s in S])
# Pick count_neg number of questions from the +ve sections
for s in dist:
    if meta[s][2] > 0:  # distribute the diffs into dist.
        if count_neg - meta[s][2] > 0:
            dist[s] += meta[s][2]
        else:
            dist[s] += count_neg
            break
    elif meta[s][2] < 0:
        dist[s] += meta[s][2]  # getting rid of the impossible dist
dt = datetime.now().strftime("%d-%m-%Y_%H%M")
with open(f"{vol}/log/{dt}.log", 'w') as log:
    paper_start = time.time()
    counter = 0
    for s in random.sample(list(chain.from_iterable([[k]*dist[k] for k in dist.keys()])), m):
        counter += 1
        data = {}
        lot = {}
        with open(f"{vol}/md/section{s}.md", 'r') as f:
            for row in csv.reader(f):
                data[row[0]] = row[1:]  # get the data into data
        # Extract from data
        subSections = list(data.keys())  # dict keys type => list type
        # Check if there's an existing lot
        # If lot exists, get it
        if os.path.exists(f"{vol}/data/section{s}.lot"):
            with open(f'{vol}/data/section{s}.lot', 'rb') as f:
                lot = pickle.load(f)
        else:  # Build the first lot
            lot = {sub_section: set([*range(int(data[sub_section][1]))])
                   for sub_section in subSections}
        # sections weighted acc to the number of remaining questions
        weights = [len(lot[sub_section]) for sub_section in subSections]
        q_pool = []  # pool of questions to be attempted from the chosen sub_section
        while(not len(q_pool)):
            sub_section = random.choices(subSections, weights=weights, k=1)[0]
            q_pool = list(lot[sub_section])
        q = random.choice(q_pool)
        # 0 indexed to 1 indexed
        print(
            f"{counter}. Solve Section{s} question on {data[sub_section][0]}, qno {sub_section}.{q+1}")
        print(f"Page no {getQ(n, f'{sub_section}.{q+1}')}")
        start = time.time()
        c = input("next?")
        if c == '' or c == 'y' or c == 'Y':
            lot[sub_section].remove(q)
            stop = time.time()
            delta = time.strftime("%M:%S", time.gmtime(stop-start))
            print("Time taken: ", delta)
            log.write(f's{s} Q {sub_section}.{q+1}: {delta}\n')
        # Saving the lot
        with open(f'{vol}/data/section{s}.lot', 'wb') as f:
            pickle.dump(lot, f)
    paper_end = time.time()
    delta = time.strftime("%H:%M:%S",
                          time.gmtime(paper_end-paper_start))
    avg_delta = time.strftime("%M:%S",
                              time.gmtime((paper_end-paper_start)/m))
    print('Total time taken', delta)
    log.write(f'Total time taken: {delta}\n')
    print('Avg time per question', avg_delta)
    log.write(f'Avg time per question: {avg_delta}\n')
