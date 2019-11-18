'''
Test cases for HW11
Fangji Liang
'''

import unittest
import os
from HW11_Fangji_Liang import Repository, Student, Instructor, Major, BadDataException


class TestHW09(unittest.TestCase):
    '''Test for HW09'''

    def test_student(self):
        '''Test for class:Student and part of its method'''
        t1 = ["ssw 1", "A"]
        t2 = ["ssw 2", "F"]
        s1 = Student("12345", "s1", "major")
        l1 = ['ssw 1', 'ssw 2']
        l2 = ['ssw 2', 'ssw 3']
        s1.add_course(t1[0], t1[1])
        s1.add_course(t2[0], t2[1])
        self.assertEqual(s1.grades, {"ssw 1": "A", "ssw 2": "F"})
        self.assertEqual(s1.get_completed_courses(), ["ssw 1"])
        self.assertEqual(s1.get_remaining_required(l1), ['ssw 2'])
        self.assertEqual(s1.get_remaining_elective(l1), None)
        self.assertEqual(s1.get_remaining_elective(l2), l2)

    def test_instructor(self):
        '''Test for class:Instructor and part of its method'''
        t1 = ["ssw 1", "A"]
        t2 = ["ssw 1", "F"]
        i1 = Instructor("12345", "i1", "dept")
        i1.add_student(t1[0])
        i1.add_student(t2[0])
        self.assertEqual(i1.teach, {"ssw 1": 2})

    def test_repository(self):
        '''Test for class:Repository and part of its method'''
        r2 = Repository(
            'C:/Users/70753/Desktop/MyPython/HW11-Test/HW11_SimpleTest')
        self.assertEqual(len(r2.students), 1)
        for key, value in r2.students.items():
            self.assertEqual(key, "10103")
            self.assertEqual(value.name, "Baldwin, C")
            self.assertEqual(value.major, "SFEN")
            self.assertEqual(value.grades, {"SSW 567": 'A'})
        self.assertEqual(len(r2.instructors), 1)
        for key, value in r2.instructors.items():
            self.assertEqual(key, "98765")
            self.assertEqual(value.name, "Einstein, A")
            self.assertEqual(value.dep, "SFEN")
            self.assertEqual(value.teach, {"SSW 567": 1})
        fr = ['SSW 540', 'SSW 564', 'SSW 555', 'SSW 567']
        fe = ['CS 501', 'CS 513', 'CS 545']
        yr = ['SYS 671', 'SYS 612', 'SYS 800']
        ye = ['SSW 810', 'SSW 565', 'SSW 540']
        self.assertEqual(r2.majors['SFEN'].r, fr)
        self.assertEqual(r2.majors['SFEN'].e, fe)
        self.assertEqual(r2.majors['SYEN'].r, yr)
        self.assertEqual(r2.majors['SYEN'].e, ye)

        r1 = Repository('C:/Users/70753/Desktop/MyPython/HW11-Test')
        l1 = ['98762', 'Hawking, S', 'CS', 'CS 501', '1', '98762', 'Hawking, S',
              'CS', 'CS 546', '1', '98762', 'Hawking, S', 'CS', 'CS 570', '1',
              '98763', 'Rowland, J', 'SFEN', 'SSW 555', '1', '98763', 'Rowland, J',
              'SFEN', 'SSW 810', '4', '98764', 'Cohen, R', 'SFEN', 'CS 546', '1']
        l2 = list()
        for row in r1.instructor_table_db(os.path.join(r1.dir_path, r1.db)):
            l2 += row
        self.assertEqual(l1, l2)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
