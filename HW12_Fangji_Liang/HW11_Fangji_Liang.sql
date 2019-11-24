SELECT NAME FROM instructors WHERE CWID=98763;
SELECT Dept, COUNT(*) AS cntInstructor FROM instructors GROUP BY Dept;
SELECT Grade, max(cnt) FROM (select Grade, COUNT(*) AS cnt FROM grades GROUP BY Grade);
SELECT students.CWID, students.Name, grades.Course, grades.Grade
    FROM students JOIN grades ON students.CWID = grades.StudentCWID;
SELECT Name FROM students JOIN grades ON students.CWID = grades.StudentCWID
    WHERE grades.Grade IS NOT NULL AND grades.Course = 'SSW 810';

DROP TABLE IF EXISTS instructor_summary;
CREATE TABLE instructor_summary(
    InstructorCWID TEXT,
	Name TEXT,
	Department TEXT,
	Course_Taught TEXT,
    Count_Students TEXT
);
INSERT INTO instructor_summary
    SELECT instructors.CWID, instructors.Name, instructors.Dept, grades.Course, count(grades.StudentCWID)
        From instructors join grades on instructors.CWID = grades.InstructorCWID
            GROUP BY grades.InstructorCWID, grades.Course;