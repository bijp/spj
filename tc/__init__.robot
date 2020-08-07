*** Settings ***
Library    pylib.ApiSchoolClassLib
Library    pylib.ApiTeacherLib
Library    pylib.ApiStudentLib


Suite Setup     Run Keywords    delete all students   AND
                ...  delete all teachers   AND
                ...  delete all school classes
