import re
import mysql.connector
import csv


# CONNECT TO MYSQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="JustFor12345!",
    database="acp"
)
cursor = conn.cursor()


# FILE PATH
file_path = r"%\Course Directory_SAS.csv"


# READ CSV FILE
with open(file_path, newline='', encoding='utf-8') as file:
    reader = csv.reader(file)

    next(reader)  # skip header

    for cols in reader:
        try:
            if len(cols) < 7:
                continue

        
            # BASIC FIELDS
            course_code_raw = cols[1].strip()
            course_name = cols[2].strip()
            credits = float(cols[3].strip())
            faculty = cols[4].strip()
            term = cols[5].strip()

            prereq_text = cols[6].strip() if len(cols) > 6 else None
            antireq_text = cols[7].strip() if len(cols) > 7 else None
            course_desc = cols[8].strip() if len(cols) > 8 else None
            ger_category = cols[9].strip() if len(cols) > 9 else None
            schedule_text = cols[-1].strip()

           
            # COURSE CODE
            code_match = re.search(r"([A-Z]{3}\d+)", course_code_raw)
            if not code_match:
                continue
            course_code = code_match.group(1)


            # PREREQUISITES
            if prereq_text:
                prereq_clean = re.sub(r"\[.*?\]", "", prereq_text)
                prereq_clean = prereq_clean.replace("OR", " OR ")
                prereq_clean = re.sub(r"\s+", " ", prereq_clean).strip()
            else:
                prereq_clean = None


            # ANTIREQUISITES
            if antireq_text and antireq_text.lower() != "none":
                antireq_clean = re.sub(r"\[.*?\]", "", antireq_text)
                antireq_clean = re.sub(r"\s+", " ", antireq_clean).strip()
            else:
                antireq_clean = None


            # COURSE DESCRIPTION
            if course_desc:
                course_desc = course_desc.replace("View/Print Outline", "")
                course_desc = re.sub(r"\s+", " ", course_desc).strip()
            else:
                course_desc = None

 
            # GER CATEGORY
            if ger_category:
                if ger_category.lower() == "not applicable":
                    ger_category = None
                else:
                    ger_category = ger_category.strip()
            else:
                ger_category = None


            # INSERT INTO COURSES
            cursor.execute("""
                INSERT IGNORE INTO course
                (course_code, course_name, credits, faculty, term,
                 prerequisites, antirequisites, course_description,
                 ger_category, school)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                course_code,
                course_name,
                credits,
                faculty,
                term,
                prereq_clean,
                antireq_clean,
                course_desc,
                ger_category,
                "SAS"
            ))

            # EXTRACT SCHEDULE
            schedule_pattern = r"(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+\[(\d{2}:\d{2}) to (\d{2}:\d{2})\].*?\[(\d{2}-\d{2}-\d{4}) to (\d{2}-\d{2}-\d{4})\]"
            schedules = re.findall(schedule_pattern, schedule_text)

            section_matches = re.findall(r"Section\s*(\d+)", schedule_text)
            sections = [int(s) for s in section_matches] if section_matches else [1]


            # INSERT INTO schedule_g
            for i, (day, st, et, csd, ced) in enumerate(schedules):
                section = sections[i] if i < len(sections) else sections[0]

                cursor.execute("""
                    INSERT INTO schedule_g
                    (course_code, section, csd, ced, d, st, et)
                    VALUES (%s, %s,
                            STR_TO_DATE(%s,'%d-%m-%Y'),
                            STR_TO_DATE(%s,'%d-%m-%Y'),
                            %s, %s, %s)
                """, (
                    course_code,
                    section,
                    csd,
                    ced,
                    day,
                    st,
                    et
                ))

            print(f"INSERTED: {course_code}")

        except Exception as e:
            print("ERROR:", e)


# COMMIT & CLOSE
conn.commit()
cursor.close()
conn.close()
