*** Settings ***
Library   pylib.MobileOpLibShare
Library   pylib.MobileOpLibAdmin    WITH NAME   MobileLIB
Library   pylib.ApiTeacherLib
Library   pylib.WebOpLibTeacher
Library   pylib.WebOpLibShare

Variables   cfg.py

Suite Setup  run keywords  open_mobile  AND   open_browser
Suite Teardown  run keywords   close_mobile  AND   close_browser

*** Test Cases ***




添加班级1 - tc006201
    [Setup]    run keywords   reset app   AND  vcode_login   ${g_vcode}

    ${retInfo}=   MobileLIB.addTeacher   tuobaguang   拓跋光
        ...     ${g_subject_math_id}
        ...     ${suite_g7c1_classid}
        ...   13550000001   1350@g.com   320525187603030021


    should be true    $retInfo.startswith('添加成功')

    ${teacherID}=   evaluate  $retInfo.split('：')[-1]

# app 界面验证
    ${ret}  ${list}    getAllTeachersInSystem
    should be true   $ret==True
    should be true   $list==['拓跋光', 'id：${teacherID}\xa0登录名：tuobaguang\xa0手机：13550000001\xa0邮箱：1350@g.com\xa0身份证：320525187603030021\xa0']

# web 登录验证
    teacher login   tuobaguang   888888

    ${teacherinfo}=  get_teacher_homepage_info
    ${eteacherinfo}=  create list  松勤学院0001   拓跋光
                  ...  初中数学   0   0   0

    should be equal   ${teacherinfo}    ${eteacherinfo}


    ${classstudent}=  get_teacher_class_students_info
    should be true   $classstudent=={'七年级1班':[]}


    [Teardown]    run keywords   reset app   AND   delete_teacher   ${teacherID}
