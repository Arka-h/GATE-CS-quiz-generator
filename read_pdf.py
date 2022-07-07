import os
import re
import pickle
from PyPDF2 import PdfFileReader

pg = {}  # {'q.n.o': pg_no}


def is_greater(vset1, vset2):
    # Comparison: returns (True if vset1 > vest2; False if val1 <= val2)
    vset1, vset2 = vset1[0], vset2[0]
    # Unpacking|conversion for digit-wise comparison
    x1, y1, z1 = [int(i) for i in vset1]
    x2, y2, z2 = [int(i) for i in vset2]

    if x1 == x2:
        if y1 == y2:
            return z1 > z2
        return y1 > y2
    return x1 > x2


def find_q(pdf, pg_no):
    return re.findall('([0-9]+)\.([0-9]+)\.([0-9]+).*☛.*https://gateoverflow.in/[0-9]+\n(?:\n|[^-])[^-]',
                      pdf.getPage(pg_no).extractText())


def binSearch(pdf, l, r, vset, debug):
    global pg
    q_no = '.'.join(vset[0])
    if q_no in pg:
        return pg[q_no]
    p = (l+r)//2  # Pick the middle
    if l == p:
        return p
    pset = find_q(pdf, p)  # returns the all the matches on the page
    if debug:
        print(f"l: {l+1}, r: {r+1}, p: {p+1} : pset {pset}")
    t1 = t2 = p
    tset1 = tset2 = pset
    while(t1 >= l and (not len(tset1))):  # left arr => tset1
        t1 -= 1
        tset1 = find_q(pdf, t1)
    while(t2 < r and not len(tset2)):  # right arr => tset2
        t2 += 1
        tset2 = find_q(pdf, t2)
    if debug:
        print(f"\tt1: pg{t1+1}; set:{tset1}")
        print(f"\tt2: pg{t2+1}; set:{tset2}")
    # Definitely have a working t at this point
    # Save the searches
    for q in tset1:  # Each q is a tuple
        pg['.'.join(q)] = t1
    if is_greater(tset2, tset1):  # since t2 > t1
        for q in tset2:  # Each q is a tuple
            pg['.'.join(q)] = t2
    if len(tset1) and is_greater(tset1, vset):  # t1 is greater than target
        # But not equal to
        return binSearch(pdf, l, t1+(0 if t1 == p else 1), vset, debug)
    else:  # t is equal to or lesser than
        return binSearch(pdf, t2, r, vset, debug)


def getQ(vol, question):
    global pg
    pg_no, debug = 0, False

    if os.path.exists(f'vol{vol}/data/pg_no.dir'):
        with open(f'vol{vol}/data/pg_no.dir', 'rb') as f:
            pg = pickle.load(f)  # load the directory if exists
    with open(f'vol{vol}/Volume-{vol}.pdf', 'rb') as f:
        pdf = PdfFileReader(f)
        n = pdf.getNumPages()
        # Prepare the vset
        vset = re.findall('([0-9]+)\.([0-9]+)\.([0-9]+)', question)
        # Apply binary Search + DP
        pg_no = binSearch(pdf, 0, n, vset, debug)+1

    with open(f'vol{vol}/data/pg_no.dir', 'wb') as f:
        pickle.dump(pg, f)  # QuickSave after the search
    return pg_no


if __name__ == '__main__':
    i = int(input("Enter the volume: "))
    question = input("Enter the question number: ")
    print("page no", getQ(i, question))
