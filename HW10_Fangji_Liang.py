'''
HW10 School's Repository includes student, instructor, majors and Repository
Fangji Liang
'''

import os
from collections import defaultdict
from prettytable import PrettyTable


class BadDataException(Exception):
    pass


class Major:
    '''Class major inlude name, required, elective'''

    def __init__(self, name='NA'):
        self.name = name
        self.r = []
        self.e = []


class Student:
    '''
    Student class cwid is demanded parameter. 
    name, major and email are default parameters.
    '''

    def __init__(self, cwid='NA', name='NA', major='NA'):
        '''__init__ magic method'''
        self.cwid = cwid
        self.name = name
        self.major = major
        self.grades = defaultdict(str)

    def add_course(self, course, grade='NA'):
        '''add course and grade to a student's grades'''
        self.grades[course] = grade

    def get_completed_courses(self):
        ''' get student's completed courses'''
        # sort here
        result = sorted(
            [c for c, g in self.grades.items() if g.upper() != 'F'])
        return None if len(result) == 0 else result

    def get_remaining_required(self, l):
        ''' get student's remaining required courses'''
        if self.get_completed_courses() != None:
            result = sorted(
                [c for c in l if c not in self.get_completed_courses()])
        else:
            result = l
        return None if len(result) == 0 else result

    def get_remaining_elective(self, l):
        ''' get student's remaining elective courses'''
        if self.get_completed_courses() != None:
            if len([c for c in l if c in self.get_completed_courses()]) != 0:
                return None
            else:
                return sorted(l)
        else:
            return sorted(l)

    def pretty_print(self):
        '''print one student's information'''
        pt = PrettyTable(
            field_names=['CWID', 'Name', 'Major', 'Course', 'Grade'])
        for cour, grad in self.grades.items():
            pt.add_row([self.cwid, self.name, self.major, cour, grad])
        return pt


class Instructor:
    '''Instructor class include cwid, name, department'''

    def __init__(self, cwid='NA', name='NA', dep='NA'):
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
    '''repository to store students, instrutors, majors'''

    def __init__(self, dir_path, suffix='.txt'):
        '''__init__ magic method'''
        self.dir_path = dir_path
        self.suffix = suffix
        self.students = defaultdict(Student)
        self.instructors = defaultdict(Instructor)
        self.majors = defaultdict(Major)
        # catch exception
        try:
            self.read_majors()
            self.read_inst()
            self.read_stu()
            self.read_gra()
            print(self.print_pre_stu())
            print(self.print_pre_inst())
            print(self.print_pre_maj())
        except FileNotFoundError as e:
            print(e)
        except OSError as e:
            print(e)
        except BadDataException as e:
            print(e)
        except ValueError as e:
            print(e)

        # change warn to catch and print all bad data

    def file_read(self, path, fields, header=False, sep=' '):
        '''A method read file line by line
        file_path, data_fields, header, separator
        '''
        try:
            os.chdir(self.dir_path)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"{self.dir_path} --  Can't find or locate this dir_path")
        except OSError:
            raise OSError(f"{self.dir_path} -- illegal dir_path")
        try:
            fp = open(path, 'r')
        except FileNotFoundError:
            raise FileNotFoundError(f"{path} -- Can't find or open this file")
        with fp:
            if header:
                next(enumerate(fp, 1))
            for index, line in enumerate(fp, 1):
                temp = line.strip('\n').split(sep)
                if temp == list():
                    continue
                elif len(temp) != fields:
                    raise BadDataException(
                        f'line{index} in {path}:{line} -- Missing data, supposed fields{fields}')
                else:
                    yield index, temp

    def read_inst(self):
        '''read insturctors file'''
        file_name = 'instructors' + self.suffix
        for index, line in self.file_read(file_name, 3, True, '|'):
            self.instructors[line[0]] = Instructor(line[0], line[1], line[2])

    def read_stu(self):
        '''read students file'''
        file_name = 'students' + self.suffix
        for index, line in self.file_read(file_name, 3, True, ';'):
            self.students[line[0]] = Student(line[0], line[1], line[2])

    def read_gra(self):
        '''read grades file'''
        file_name = 'grades' + self.suffix
        for index, line in self.file_read(file_name, 4, True, '|'):
            if line[0] in self.students.keys():
                self.students[line[0]].add_course(line[1], line[2])
            else:
                raise BadDataException(
                    f"line{index} in {file_name} -- Unidentified student's grades")
            if line[-1] in self.instructors.keys():
                self.instructors[line[-1]].add_student(line[1])
            else:
                raise BadDataException(
                    f"line{index} in {file_name} -- Unidentified instructor's grades")

    def read_majors(self):
        '''read majors file'''
        file_name = 'majors' + self.suffix
        for index, line in self.file_read(file_name, 3, True, '\t'):
            if str(line[1]).upper() == 'R':
                self.majors[line[0]].r.append(line[2])
            elif str(line[1]).upper() == 'E':
                self.majors[line[0]].e.append(line[2])
            else:
                raise BadDataException(
                    f"line{index} in {file_name} -- Unidentified type of course")

    def print_pre_stu(self):
        '''print students summary'''
        if len(self.students) > 0:
            print("Students Summary:")
            pt = PrettyTable(
                field_names=['CWID', 'Name', 'Completed Courses', 'Remaining Required', 'Remaining Reuired'])
            for cwid, stu in self.students.items():
                pt.add_row([cwid, stu.name, stu.get_completed_courses(),
                            stu.get_remaining_required(
                                self.majors[stu.major].r),
                            stu.get_remaining_elective(self.majors[stu.major].e)])
            return pt
        else:
            raise ValueError("No data in students flies.")

    def print_pre_inst(self):
        '''print insturctors summary'''
        if len(self.students) > 0:
            print("Instructors Summary:")
            pt = PrettyTable(
                field_names=['CWID', 'Name', 'Dept', 'Course', 'Students'])
            # for cwid, inst in sorted(self.instructors.items(), key=lambda x:x[0]):
            for cwid, inst in self.instructors.items():
                for cour, num in inst.teach.items():
                    pt.add_row([cwid, inst.name, inst.dep, cour, num])
            return pt
        else:
            raise ValueError("No data in instructors flies.")

    def print_pre_maj(self):
        '''print Majors Summary'''
        if len(self.students) > 0:
            print("Majors Summary:")
            pt = PrettyTable(
                field_names=['Dept', 'Required', 'Electives'])
            # for cwid, inst in sorted(self.instructors.items(), key=lambda x:x[0]):
            for name, major in self.majors.items():
                pt.add_row([name, sorted(major.r), sorted(major.e)])
            return pt
        else:
            raise ValueError("No data in instructors flies.")


def main():
    '''test file'''
    _ = Repository('C:/Users/70753/Desktop/MouseWithoutBorders/ScreenCaptures')


if __name__ == "__main__":
    main()
