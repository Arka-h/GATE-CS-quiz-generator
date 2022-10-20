import os
from os import system, name
from time import sleep
import csv
import random
from itertools import chain
from collections import Counter
import time
import pickle
from read_pdf import getQ
from datetime import datetime as dt
import multiprocessing as mp

# Always set this before running script
testing = False
show_pg_no = False
show_timing = True


def timer(q, start):
    global show_timing
    while True:
        stop = q.qsize()
        diff = dt.now() - start
        ms = diff.microseconds//10**4
        min, sec = divmod(diff.seconds, 60)
        if show_timing:
            print(f"Time Taken {min}:{sec}:{ms}", end="\r")
        if stop:
            q.get()
            q.put(diff)
            return


def countdown(t, string):
    while t:
        _, secs = divmod(t, 60)
        timer = f'{string} {secs:02d} s'
        print(timer, end="\r")
        time.sleep(1)
        t -= 1


def clear():
    if name == "nt":
        _ = system("cls")
    else:
        _ = system("clear")


def setupMeta(vol):
    meta = {}
    if os.path.exists(f"vol{vol}/csv/meta.csv"):
        with open(f"vol{vol}/csv/meta.csv", 'r') as f:
            for row in csv.reader(f):
                print(f"{row[0]}. {row[1]}    \t({row[2]})")
                meta[int(row[0])] = [row[1], int(row[2]), 0]
    else:
        print(f"Add a meta file for {vol}!!")
        exit()
    return meta


def get_section_count(vol, show_statistics=True):
    S = list(map(int, [s.strip()
                       for s in input("Which section(s)?\n").split(',')]))
    # Verify if all the sections exist in the volume.
    while(not all([s in meta for s in S])):
        S = list(map(int, [s.strip()
                           for s in input("Enter valid section numbers only\nWhich section(s)?\n").split(',')]))
    # Total questions statistics
    section_count = {}  # total number of questions in each section
    for s in S:
        lot = {}
        # Check if there's an existing lot
        # If lot exists, get it
        if os.path.exists(f"vol{vol}/data/section{s}.lot"):
            with open(f'vol{vol}/data/section{s}.lot', 'rb') as f:
                lot = pickle.load(f)
                section_count[s] = sum([len(lot[subsection])
                                        for subsection in lot.keys()])
        else:
            section_count[s] = meta[s][1]
        # Open section for statistics
        if show_statistics:
            print(f"Section{s}: total remaining questions: {section_count[s]}")
    return section_count


def get_question_subsections(total, meta):
    # Checking if it "m" (#questions) satisfies constraints
    S = list(total.keys())
    while True:
        m = int(input("Enter the number of questions: "))
        if m == 0:
            exit()
        section_order = random.choices(S, weights=[meta[s][1] for s in S], k=m)
        dist = dict(Counter(section_order))  # distribution of questions.
        bal = 0
        for s in total:
            diff = ((total[s]-dist[s]) if s in dist else total[s])
            meta[s][2] = diff  # Save the diff
            bal += diff
        if bal >= 0:
            break
        print("Please enter different number of questions")
    count_neg = - sum([meta[s][2] if meta[s][2] < 0 else 0 for s in S])
    # Pick count_neg number of questions from the +ve sections
    for s in dist:
        if meta[s][2] > 0:  # distribute the diffs into dist. to adjust the questions
            if count_neg - meta[s][2] > 0:
                dist[s] += meta[s][2]
            else:
                dist[s] += count_neg
                break
        elif meta[s][2] < 0:
            dist[s] += meta[s][2]  # getting rid of the impossible dist
    section_dist = list(chain.from_iterable(
        [[k]*dist[k] for k in dist.keys()]))
    return section_dist  # list of [sections*frequencies,] to choose from


def load_question_lot(vol, data, s, subSections):
    lot = {}
    # Check if there's an existing lot
    # If lot exists, get it
    if os.path.exists(f"vol{vol}/data/section{s}.lot"):
        with open(f'vol{vol}/data/section{s}.lot', 'rb') as f:
            lot = pickle.load(f)
    else:  # Build the first lot
        lot = {sub_section: set([*range(int(data[sub_section][1]))])
               for sub_section in subSections}
    return lot


def load_section_data(vol, s):
    data = {}
    with open(f"vol{vol}/csv/section{s}.csv", 'r') as f:
        for row in csv.reader(f):
            if len(row):
                data[row[0]] = row[1:]  # data['1.1'] = ['Balls in Bins',3]
    return data


def pick_random_question(subSections, lot):
    # subsection weights acc. to #q in each subsection
    weights = [len(lot[sub_section]) for sub_section in subSections]
    q_pool = []  # pool of questions to possibly attempt from
    while(not len(q_pool)):
        sub_section = random.choices(  # Get the subsection, with Probability dist of weights
            subSections, weights=weights, k=1)[0]
        # Pool of unattempted qs, shouldn't be empty
        q_pool = list(lot[sub_section])
    # Pick a random index from question pool, return sub_section
    return random.choice(q_pool), sub_section


def save_status(lot, s, sub_section, q, c):
    global testing
    if not testing:
        with open(f'{vol}/data/section{s}.lot', 'wb') as f:
            if c == "n" or c == "q":  # Assumes you didn't attempt the latest question
                pickle.dump(lot, f)  # Save and quit
                return 1
            else:
                # Remove the question from the lot of unattempted questions
                lot[sub_section].remove(q)
                pickle.dump(lot, f)  # Save and continue
        print(
            "-----------------------------------------------------------------------------")
    else:
        print(
            "-----------------------------------TESTING-----------------------------------")
        if c == 'n' or c == 'q':  # Assumes you didn't attempt the latest question
            return 1
    return 0


def user_statistics(paper_start, paper_end, m):
    delta = time.strftime("%H:%M:%S",
                          time.gmtime(paper_end-paper_start))
    avg_delta = time.strftime("%M:%S",
                              time.gmtime((paper_end-paper_start)/m))
    return delta, avg_delta


def startAttempt(vol, section_dist, log=None):
    global testing, show_pg_no, show_timing
    if not testing:
        countdown(5, "Test starts in :")
    clear()
    paper_start = time.time()
    counter = 0
    m = len(section_dist)
    for s in random.sample(section_dist, m):
        diff = mp.Queue()
        counter += 1
        # data['1.1'] = ['Balls in Bins',3]
        section_data = load_section_data(vol, s)
        # subSections = ['1.1', '1.2', '1.3']
        subSections = list(section_data.keys())
        # List of pending question indexes in each subsection
        lot = load_question_lot(vol, section_data, s, subSections)
        # Pick a random question acc to subsection unattempted question dist
        q, sub_section = pick_random_question(subSections, lot)
        # 0 indexed to 1 indexed
        print(
            f"{counter}. Solve Section{s} question on {section_data[sub_section][0]}, qno {sub_section}.{q+1}\ncontinue?(y/n)")
        # Binary search for the question based on binary search [Can also use the pdf search option]
        if show_pg_no:
            pg_no = getQ(n, f'{sub_section}.{q+1}')
            print(f"Page no {pg_no}")
        # Not counted towards the question time
        start = dt.now()
        p = mp.Process(target=timer, args=(diff, start))
        p.start()  # Start the timer for solving the question
        c = input()  # Take input from user, if finished solving / want to stop the test early
        diff.put(True)
        p.join()  # Stop the timer thread
        delta = diff.get()
        min, sec = divmod(delta.seconds, 60)
        # Save the log file
        if log:
            log.write(f's{s} Q {sub_section}.{q+1} | t={min:02d}:{sec:02d}\n')

        # Saving the lot
        # Saves progress regardless if user wants to quit
        if save_status(lot, s, sub_section, q, c):
            break

    paper_end = time.time()
    delta, avg_delta = user_statistics(paper_start, paper_end, m)
    if log:
        log.write(f'Total time taken: {delta}\n')
        log.write(f'Avg time per question: {avg_delta}\n')
    if show_timing:
        print('Total time taken', delta)
        print('Avg time per question', avg_delta)
    print(
        "=============================================================================")


if __name__ == "__main__":
    # {sequence number: [0: Name of the subsection , 1: Number of questions]}
    save_logs = True
    if testing:
        print("""=============================================================================
TESTING MODE
=============================================================================""")
        save_logs = True if input(
            "Do you want to save the logs?(y/n) ").lower() == 'y' else False
    n = input("Enter Volume#: ")
    # get the meta information on volume and it's sections
    meta = setupMeta(n)  # Exits the program if "meta.csv" isn't found
    # "S" stores the sections and "total" contains the count of the sections
    section_count = get_section_count(n)
    # According to the selected sections, return subsection distribution and total #questions
    section_dist = get_question_subsections(section_count, meta)
    if save_logs:
        current_attempt = dt.now().strftime("%d-%m-%Y_%H%M")
        with open(f"vol{n}/log/{current_attempt}.log", 'w') as log:
            if testing:
                log.write(f"TESTING MODE\n")
            startAttempt(n, section_dist, log)
    else:
        startAttempt(n, section_dist)
