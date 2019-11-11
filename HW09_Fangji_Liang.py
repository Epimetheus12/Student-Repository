'''
HW09 School's Repositor includes student and instructor
Fangji Liang
'''

import os
from collections import defaultdict
from prettytable import PrettyTable
import warnings


class Student:
    '''
    Student class cwid is demanded parameter. 
    name, major and email are default parameters.
    '''

    def __init__(self, cwid, name='NA', major='NA', email='NA'):
        '''__init__ magic method'''
        self.cwid = cwid
        self.name = name
        self.major = major
        self.email = email
        self.grades = defaultdict(str)

    def add_course(self, course, grade='NA'):
        '''add course and grade to a student's grades'''
        self.grades[course] = grade

    def get_completed_courses(self):
        ''' get student's completed courses'''
        return [c for c, g in self.grades.items() if g.upper() != 'F']

    def pretty_print(self):
        '''print one student's information'''
        pt = PrettyTable(
            field_names=['CWID', 'Name', 'Major', 'Course', 'Grade'])
        for cour, grad in self.grades.items():
            pt.add_row([self.cwid, self.name, self.major, cour, grad])
        return pt


class Instructor:
    def __init__(self, cwid, name='NA', dep='NA', email='NA', warn_log=False):
        '''__init__ magic method'''
        self.cwid = cwid
        self.name = name
        self.dep = dep
        self.teach = defaultdict(int)

    def add_student(self, course):
        '''add a student to a instructor's grades'''
        self.teach[course] += 1

    def pretty_print(self):
        '''print one instructor's information'''
        pt = PrettyTable(
            field_names=['CWID', 'Name', 'Dept', 'Course', 'Students'])
        for cour, stu in self.teach.items():
            pt.add_row([self.cwid, self.name, self.dep, cour, stu])
        return pt


class Repository:
    def __init__(self, dir_path, suffix='.txt', r_warn=False):
        '''__init__ magic method'''
        self.dir_path = dir_path
        self.suffix = suffix
        self.students = defaultdict(Student)
        self.instructors = defaultdict(Instructor)
        self.r_warn = r_warn
        self.r_warnings = ''
        if self.file_list():
            self.read_inst()
            self.read_stu()
            self.read_gra()
        if self.r_warn:
            warnings.warn(f"{self.r_warnings}", UserWarning)

    def file_list(self):
        '''locate file's position'''
        try:
            os.chdir(self.dir_path)
            return True
        except FileNotFoundError:
            raise FileNotFoundError(
                f"{self.dir_path} -- Can't find this directory!")
        except OSError:
            raise OSError(
                f"{self.dir_path}-- Incorrect file name, directory name, or volume label syntax")
        else:
            return False

    def read_inst(self):
        '''read insturctors file'''
        os.chdir(self.dir_path)
        file_name = 'instructors' + self.suffix
        try:
            fp = open(file_name, 'r')
        except FileNotFoundError:
            raise FileNotFoundError(
                f"{file_name} -- Can't find this file!")
        else:
            with fp:
                for index, line in enumerate(fp, 1):
                    line = line.strip('\n').split()
                    if line == list():
                        self.r_warnings += f'File:{file_name} -- Line {index} is a empty line.\n'
                        continue
                    elif len(line) == 4:
                        self.instructors[line[0]] = Instructor(
                            line[0], ' '.join(line[1:3]), line[3])
                    else:
                        self.r_warnings += f'File:{file_name} -- Defective data in Line {index}, it is supposed to have 3 fields.\n'

    def read_stu(self):
        '''read students file'''
        file_name = 'students' + self.suffix
        try:
            fp = open(file_name, 'r')
        except FileNotFoundError:
            raise FileNotFoundError(
                f"{file_name} -- Can't find this file!")
        else:
            with fp:
                for index, line in enumerate(fp, 1):
                    line = line.strip('\n').split()
                    if line == list():
                        self.r_warnings += f'File:{file_name} -- Line {index} is a empty line.\n'
                        continue
                    elif len(line) == 4:
                        self.students[line[0]] = Student(
                            line[0], ' '.join(line[1:3]), line[3])
                    else:
                        self.r_warnings += f'File:{file_name} -- Defective data in Line {index}, it is supposed to have 3 fields.\n'

    def read_gra(self):
        '''read grades file'''
        file_name = 'grades' + self.suffix
        try:
            fp = open(file_name, 'r')
        except FileNotFoundError:
            raise FileNotFoundError(
                f"{file_name} -- Can't find this file!")
        else:
            with fp:
                for index, line in enumerate(fp, 1):
                    line = line.strip('\n').split()
                    if line == list():
                        self.r_warnings += f'File:{file_name} -- Line {index} is a empty line.\n'
                        continue
                    elif len(line) == 5:
                        if line[0] in self.students.keys():
                            self.students[line[0]].add_course(
                                ' '.join(line[1:3]), line[3])
                        if line[-1] in self.instructors.keys():
                            self.instructors[
                                line[-1]].add_student(' '.join(line[1:3]))
                    else:
                        self.r_warnings += f'File:{file_name} -- Defective data in Line {index}, it is supposed to have 3 fields.\n'

    def print_pre_stu(self):
        '''print students summary'''
        if len(self.students) > 0:
            print("Students Summary:")
            pt = PrettyTable(
                field_names=['CWID', 'Name', 'Completed Courses'])
            for cwid, stu in self.students.items():
                pt.add_row([cwid, stu.name, stu.get_completed_courses()])
            return pt
        else:
            raise ValueError("No data in students flies.")

    def print_pre_inst(self):
        '''print insturctors summary'''
        if len(self.students) > 0:
            print("Instructors Summary:")
            pt = PrettyTable(
                field_names=['CWID', 'Name', 'Dept', 'Course', 'Students'])
            for cwid, inst in self.instructors.items():
                for cour, num in inst.teach.items():
                    pt.add_row([cwid, inst.name, inst.dep, cour, num])
            return pt
        else:
            raise ValueError("No data in instructors flies.")


def main():
    '''test file'''
    test = Repository('/Users/70753/Desktop/MyPython/Test/', r_warn=True)
    print(test.print_pre_stu())
    print(test.print_pre_inst())


if __name__ == "__main__":
    main()
