import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from mysql import connector
import os
import time
from enum import Enum

class Roles(Enum):
    MEMBER = 0
    PRESIDENT = 1
    VICE_PRESIDENT = 2
    SECRETARY = 3
    FINANCE_TEAM = 4
    RESEARCH_TEAM = 5
    PR_TEAM = 6
    WEB_TEAM = 7
    MEDIA_TEAM = 8


def null_prevention(raw_answer: str):
    raw_answer = str(raw_answer)
    if not raw_answer.strip() == '':
        return raw_answer
    else:
        return None

class Database:


    def __init__(self):
        load_dotenv()

        self.db = connector.connect(
            host=os.getenv('DB_IP'),
            port=os.getenv('DB_PORT'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
        )

        self.cursor = self.db.cursor()

        print('Conntected to Database')



    def insert_into_students_from_sheets(self, row):

        uni_id = int(row['University ID'])

        first_name = null_prevention(row['First Name'])

        last_name = null_prevention(row['Last Name'])

        email = null_prevention(row['University Email Address'])

        phone = '+' + null_prevention(row['Phone Number'])

        gender = null_prevention(row['Gender'])

        faculty = null_prevention(row['What is your faculty?'])

        major = null_prevention(row['What is your major? (eg. Computer Engineering)'])

        year_str = null_prevention(row['What year are you in?'])
        year = year_str[0]

        ai_familiarity = int(row['How familiar are you with AI'])

        hours_passed = int(row['Credit Hours Passed'])

        linkedin = null_prevention(row['LinkedIn (Optional)'])

        git_hub = null_prevention(row['GitHub (Optional)'])

        communities = null_prevention(row['Which community are you a part of? (Optional)'])

        AAAI_member = False
        IEEE_member = False

        if communities:
            if 'AAAI' in communities:
                AAAI_member = True
            if 'IEEE' in communities:
                IEEE_member = True

        interested_activities = null_prevention(row['Which activity are you likely to join'])

        remarks = ''

        if interested_activities:
            remarks = remarks + 'Interested in : ' + interested_activities
        sql = '''
           CALL insert_student_from_sheets(
           %s, %s, %s, %s, %s, 
           %s, %s, %s, %s, %s, 
           %s, %s, %s, %s, %s,
           %s
           )
           '''

        values = (
            uni_id,
            first_name,
            last_name,
            email,
            phone,
            gender,
            faculty,
            major,
            year,
            ai_familiarity,
            hours_passed,
            linkedin,
            git_hub,
            AAAI_member,
            IEEE_member,
            remarks
        )

        self.cursor.execute(sql, values)


    def insert_rows_from_sheets(self):

        insertion_time = time.time()

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        creds = Credentials.from_service_account_file(
            '../' + os.getenv('CREDENTIALS_PATH'),
            scopes=scopes
        )

        gc = gspread.authorize(creds)

        sheet = gc.open(os.getenv('SHEET_APPLICATION_NAME')).sheet1

        print('Connected to Google Sheets')

        row_values = sheet.get_all_records()

        self.cursor.execute('SELECT student_id FROM students')
        existing_student_ids = set(row[0] for row in self.cursor.fetchall())

        for row in row_values:
            uni_id = int(row['University ID'])
            if uni_id in existing_student_ids:
                print(f'skipped {uni_id}')
                continue
            self.insert_into_students_from_sheets(row)

        self.db.commit()

        insertion_time = time.time() - insertion_time

        print(f'[FINISHED] : time taken = {insertion_time:.2f} seconds')

    def delete_students(self):
        sql = '''
        DELETE FROM students;
        '''
        self.cursor.execute(sql)
        self.db.commit()

        print('Deleted students')

    def close(self):
        self.cursor.close()
        self.db.close()

        print('Closesd Database')

    def change_role(self, student_id, role):
        sql = f'''
                UPDATE students
                SET role_id = {role.value}
                WHERE student_id = {student_id};
                '''
        self.cursor.execute(sql)
        self.db.commit()

        print(f'Changed role {student_id} to {role.name}')

    def make_admin(self, student_id, role):
        sql = f'''
                INSERT INTO team_leaders
                VALUES (%s, %s);
                '''

        values = (student_id,
                  role.value)

        self.cursor.execute(sql, values)
        self.db.commit()

        print(f'Made {student_id} leader of {role.name}')

    def get_info(self, student_id):
        sql = f'''
                SELECT concat(first_name, ' ', last_name) as name, email, phone_number, git_hub, linkedin
                FROM students
                where student_id = {student_id};
                '''
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    def get_comunity_members(self, AAAI = False, IEEE = False):
        sql = f'''
                SELECT student_id 
                FROM students
                WHERE AAAI_member = %s AND IEEE_member = %s;
                '''
        values = (AAAI,
                  IEEE)

        self.cursor.execute(sql, values)
        ids = self.cursor.fetchall()
        data = []
        for student in ids:
            d = self.get_info(student[0])
            data.append(d[0])

        return data

    def update_comunities_membership(self,student_id, AAAI = False, IEEE = False):
        sql = f'''
                UPDATE students
                SET AAAI_member = %s, IEEE_member = %s
                WHERE student_id = {student_id};
                '''

        values = (AAAI, IEEE)
        self.cursor.execute(sql, values)
        self.db.commit()
        print(f'Updated {student_id} membership : {AAAI = }, {IEEE = }')

