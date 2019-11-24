'''
HW11 School's Repository includes student, instructor, majors and Repository
read data from database
Fangji Liang
'''

import sqlite3
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/instructors')
def instructor_html():
    dp_path = 'C:/Users/70753/Desktop/MyPython/HW12_Fangji_Liang/HW12_Fangji_Liang.db'
    db = sqlite3.connect(dp_path)
    query = "select * from instructor_summary"

    data = [{'cwid': cwid, 'name': name, 'dept': dept,
             'course': course, 'students': stus}
            for cwid, name, dept, course, stus in
            db.execute(query)]

    return render_template(
        'instructors.html',
        title='Stevens Repository',
        table_title='Instructor Summary',
        instructors=data)


if __name__ == "__main__":
    app.run(debug=True)
