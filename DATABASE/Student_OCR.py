import pdfplumber
import re
import mysql.connector
import os

pdf_path = r"%\Course requirement for Enrolment Number AUXXXXXXX.pdf"

if not os.path.exists(pdf_path):
    print("FILE DOES NOT EXIST")
    exit()


# CONNECT TO MYSQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="JustFor12345!",
    database="acp"
)
cursor = conn.cursor()


# READ PDF
text = ""

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

#DEBUG
print("Extracted Text Preview")
print(text[:500])


# STUDENT EXTRACTION
e = re.search(r"Enrolment No:\s*(\w+)", text)
e_id = e.group(1) if e else None

name_match = re.search(r"Name:\s*(.+)", text)
s_name = name_match.group(1).strip() if name_match else None

prog_match = re.search(r"Programme\s*&\s*Major:\s*(.+)", text)
prog_major = prog_match.group(1).strip() if prog_match else ""

if "-" in prog_major:
    programme, major = prog_major.split("-", 1)
else:
    programme = prog_major
    major = prog_major

programme = programme.strip()
major = major.strip()

email = None
minor = None

#DEBUG
print("\nExtracted Values")
print("Enrolment ID:", e_id)
print("Name:", s_name)
print("Programme:", programme)
print("Major:", major)
#print("Minor:", minor)  IF APPLICABLE


# INSERT STUDENT
if e_id and s_name and programme and major:
    try:
        cursor.execute("""
            INSERT INTO students 
            (e_id, s_name, email, pwd, programme, major, minor)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (e_id, s_name, email, "default123", programme, major, minor))

        conn.commit()
        print("\nSTUDENT INSERTED")

    except mysql.connector.Error as err:
        print("\nDB Error:", err)

else:
    print("\nSTUDENT EXTRACTION FAILURE")


# COURSE EXTRACTION 
raw_courses = re.findall(r"\b([A-Z]{3}\d{3})\[", text)


raw_courses += re.findall(r"\b([A-Z]{3}\d{3})\b", text)

# Remove duplicates
course_codes = sorted(list(set(raw_courses)))

print("\nExtracted Course Codes")
print(course_codes)


#  INSERT INTO taken_c
if e_id and course_codes:
    for code in course_codes:
        try:
            cursor.execute("""
                INSERT IGNORE INTO taken_c (e_id, course_code)
                VALUES (%s, %s)
            """, (e_id, code))

        except mysql.connector.Error as err:
            print(f"ERROR INSERTING {code}:", err)

    conn.commit()
    print("\nCOURSES INSERTED")

else:
    print("\nNO COURSES FOUND/MISSING ID")


# CLOSE CONNECTION
cursor.close()
conn.close()