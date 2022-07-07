# GATE-CS-quiz-generator
Multi-section quiz generator based on [GO's 3 volumes of PYQs](https://gatecse.in/gate-overflow-book-qa-only-previous-gate-tifr/) <br>
1. Takes in volume no., section no.(s) & no. of questions.
2. Randomly generates paper📄, simulates GATE q distribution [Uses distribution of questions per section/sub-section]. 
3. Reduces cognitive load on reaching the goal 🚩 of finishing all PYQs, gamifies 🎮 your attempt.
4. Since it is a CLI quiz generator, currently it displays the question to attempt, and tracks attempt time⌛.
5. Keeps track of the questions attempted ✅, and never repeats a previously attempted question.
5. Implements binary search on pdf to find and display question's page no. [saves seen pages' question nos for faster🕔 access]
6. Generates reports in log files 📝, having the questions attempted and attempt times, along with other statistics 📈
7. Code is flexible and can be changed to suit one's needs. For ex. different pdfs, different exam; just need to change some csv files having meta information 

## Usage
<br>

> ```$ python pyqTest.py```
<br>

![WindowsTerminal_LbMX0oeVaQ](https://user-images.githubusercontent.com/47897466/177864786-417e0069-38d8-4963-ab92-a13af5aade73.png)
![image](https://user-images.githubusercontent.com/47897466/177864996-8bd85175-7980-45b8-8ea5-da4fa8722210.png)
<br>

The log file of this test run with all the stats.
<br>

![Code_PWMCGxreVm](https://user-images.githubusercontent.com/47897466/177865271-13a71e6c-5d01-4e1b-8cbd-620323b69793.png)

This can be further used to write notes related to specific questions, and performing analysis

## File Structure
    .
    ├── vol1                    # Folder with saved data, logs and the vol1 pdf
    |    ├── data               # Folder with .dir files (saved page_no searches), and .lot files (the lot of remaining q's to pick from)
    |    ├── log                # Folder with saved logs having question number attempted, and timing
    |    ├── csv                # Contains all meta information about sections and sub-sections
    |    └──Volume-1.pdf        # GO PYQ Volume1 pdf 
    ├── vol2                    # Folder with saved data, logs and the vol2 pdf
    |    ...                    # Same as for vol1
    |    └──Volume-2.pdf        
    ├── vol3                    # Folder with saved data, logs and the vol3 pdf
    |    ...                    # Same as for vol1/2
    |    └──Volume-3.pdf        
    ├── __init__.py             # For using read_pdf module 
    ├── extract_meta.py         # Used to extract index page text (meta_index.txt) and open with word processor (preferably vscode)
    ├── pyqTest.py              # The main test setter, uses the meta.csv and sectionx.csv for q distribution
    ├── read_pdf.py             # Contains search utility to search for a question's page no. from pdf/ saved dictionary
    ├── regex_test.py           # Test file to test out the regex [for question(s) extraction from pdf text]
    └── README.md
