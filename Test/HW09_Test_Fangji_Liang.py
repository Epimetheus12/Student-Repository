'''
Test cases for HW09
Fangji Liang
'''

import unittest
from HW09_Fangji_Liang import Repository, Student, Instructor


class TestHW09(unittest.TestCase):
    '''Test for HW09'''

    def test_student(self):
        '''Test for class:Student and part of its method'''
        t1 = ["ssw 1", "A"]
        t2 = ["ssw 2", "F"]
        s1 = Student("12345", "s1", "major")
        s1.add_course(t1[0], t1[1])
        s1.add_course(t2[0], t2[1])
        self.assertEqual(s1.grades, {"ssw 1": "A", "ssw 2": "F"})
        self.assertEqual(s1.get_completed_courses(), ["ssw 1"])

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
        with self.assertRaises(OSError):
            Repository(' ')
        with self.assertRaises(FileNotFoundError):
            Repository('desktop')
        with self.assertWarns(UserWarning):
            self.assr1 = Repository(
                '/Users/70753/Desktop/MyPython/Test/', r_warn=True)
        r2 = Repository('/Users/70753/Desktop/MyPython/Test/')
        self.assertEqual(len(r2.students), 1)
        for key, value in r2.students.items():
            self.assertEqual(key, "10103")
            self.assertEqual(value.name, "Baldwin, C")
            self.assertEqual(value.major, "SFEN")
            self.assertEqual(value.grades, {"SSW 564": 'A-'})
        self.assertEqual(len(r2.instructors), 1)
        for key, value in r2.instructors.items():
            self.assertEqual(key, "98764")
            self.assertEqual(value.name, "Feynman, R")
            self.assertEqual(value.dep, "SFEN")
            self.assertEqual(value.teach, {"SSW 564": 1})


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
