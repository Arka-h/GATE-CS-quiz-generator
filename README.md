# GATE-CS-quiz-generator
Multi-section quiz generator based on [GO's 3 volumes of PYQs](https://gatecse.in/gate-overflow-book-qa-only-previous-gate-tifr/) <br>
1. Takes in volume no., section no.(s) & no. of questions. to generate the question paper
2. The generated paper๐, simulates GATE q distribution [Uses distribution of questions per section and sub-section]. 
3. Reduces cognitive load on reaching the goal ๐ฉ of finishing all PYQs, gamifies ๐ฎ your attempts.
4. It is currently a CLI quiz generator, so it displays the question to attempt, and also tracks attempt timeโ.
5. Keeps track of the questions attempted โ, and never repeats a previously attempted question (customisable, explained below).
6. You can add/remove the questions from the 'lot' of unattempted questions using the `updateLots` utility.
7. Implements binary search on pdf to find and display question's page no. [saves seen pages' question nos too ๐]
8. Generates reports in log files ๐, having the questions attempted and attempt times, along with other statistics ๐
9. Code is flexible and can be changed to suit one's needs. For ex. different pdfs, different exam; just need to change some csv files having meta information 

#### NOTE : The pdf search can also be used to find the question. *Beware*, as it may lead you straight to the "answer key" page/ "pyq answer"

## Usage
<br>

Install the  pypdf2 package, if using the search utility [Optional]

> ```$ pip install PyPDF2```


Simply run the `pyqTest` in terminal 

> ```$ python pyqTest.py```


#### NOTE : The search utility is by default off. Turn it on by changing line 16 in `pyqTest` to this:
> ``` show_pg_no = True ```


<br>

![image](https://user-images.githubusercontent.com/47897466/177963432-60b60bf9-227c-4358-82e2-fa829e5f0862.png)
![image](https://user-images.githubusercontent.com/47897466/177963447-0c234260-163e-4174-9f6c-e604abe02477.png)

<br>

- Only press Enter to goto the next question, and log the time taken
- The log files can be found at `./vol{x}/log/{DATE}_{TIME}.log`
<br>

![image](https://user-images.githubusercontent.com/47897466/177963495-2c7192d6-e84e-4440-af83-3d6a6e6c1601.png)

This can be further used to write notes related to specific questions, and performing analysis

## File Structure
    .
    โโโ vol1                    # Folder with saved data, logs and the vol1 pdf
    |    โโโ data               # Folder with .dir files (saved page_no searches), and .lot files (the lot of remaining q's to pick from)
    |    โโโ log                # Folder with saved logs having question number attempted, and timing
    |    โโโ csv                # Contains all meta information about sections and sub-sections
    |    โโโVolume-1.pdf        # GO PYQ Volume1 pdf 
    โโโ vol2                    # Folder with saved data, logs and the vol2 pdf
    |    ...                    # Same as for vol1
    |    โโโVolume-2.pdf        
    โโโ vol3                    # Folder with saved data, logs and the vol3 pdf
    |    ...                    # Same as for vol1/2
    |    โโโVolume-3.pdf        
    โโโ __init__.py             # For using read_pdf module 
    โโโ extract_meta.py         # Used to extract index page text (meta_index.txt) and open with word processor (preferably vscode)
    โโโ pyqTest.py              # The main test setter, uses the meta.csv and sectionx.csv for q distribution
    โโโ read_pdf.py             # Contains search utility to search for a question's page no. from pdf/ saved dictionary
    โโโ regex_test.py           # Test file to test out the regex [for question(s) extraction from pdf text]
    โโโ updateLots.py           # For adding/removing questions that you've attempted and don't want in the paper/ want to add to unattempted questions
    โโโ README.md
