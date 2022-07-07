import os
from PyPDF2 import PdfFileReader
from pathlib import Path
import subprocess

vscode = Path(
    'C:/Users/aurko/AppData/Local/Programs/Microsoft VS Code/Code.exe')

text = ''
i = int(input("Enter the volume: "))
with open(f'vol{i}/Volume-{i}.pdf', 'rb') as f:
    pdf = PdfFileReader(f)
    s, e = list(map(int, input("Enter the start and end pg no: ").split()))
    for p in range(s-1, e):
        text += pdf.getPage(p).extractText()
with open(f'vol{i}/md/meta_index.md', 'w') as f:
    f.write(text)
path = Path(f'vol{i}/md/meta_index.md')
print("Done")
subprocess.call([vscode, path])  # open the file with text processor
