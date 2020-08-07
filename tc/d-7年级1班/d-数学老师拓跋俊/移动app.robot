*** Settings ***
Library   pylib.MobileOpLibShare
Library   pylib.MobileOpLibAdmin
Variables   cfg.py

Suite Setup  open_mobile
Suite Teardown  close_mobile

*** Test Cases ***



vcode登录3 - tc006003

    [Setup]    reset app
    ${ret}  ${info}    vcode_login   ${g_vcode}

    should be true   $ret==True

    ${ret}  ${list}    getAllClassesInSystem
    should be true   $ret==True
    should be true   $list==['七年级:1班', 'id：${suite_g7c1_classid}\xa0学生人数：0\xa0人数上限：60']

    ${ret}  ${list}    getAllTeachersInSystem
    should be true   $ret==True
    should be true   $list==['拓跋俊', 'id：${suite_math_teacher_id}\xa0登录名：tuobajun\xa0手机：13100000001\xa0邮箱：1301@g.com\xa0身份证：320520001\xa0']


    [Teardown]    reset app


