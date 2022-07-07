
from PyPDF2 import PdfFileReader
import re
vol = 1
p = 289
with open(f'vol{vol}/Volume-{vol}.pdf', 'rb') as f:
    pdf = PdfFileReader(f)
    for p in range(283, 321):
        txt = pdf.getPage(p).extractText()
        # print(txt)
        print(f"p{p}", re.findall('([0-9]+)\.([0-9]+)\.([0-9]+).*☛.*https://gateoverflow.in/[0-9]+\n(?:\n|[^-])[^-]',
                                  txt))

"""

Date: 08-07-22; 01:06

Params:
>>   vol = 1
>>   p = 289

Link: https://regex101.com/
Regex: ([0-9]+)\.([0-9]+)\.([0-9]+).*☛.*https://gateoverflow.in/[0-9]+\n(?:\n|[^-])[^-]
Test String: 
7.4.1 ☛https://gateoverflow.in/1455

-- suraj ( 4.8k points)



7.4.2 ☛https://gateoverflow.in/1068

-- Arjun Suresh ( 328k points)


7.4.3 ☛https://gateoverflow.in/979

7.4.3 ☛https://gateoverflow.in/979



"""
