*** Settings ***
Library   pylib.MobileOpLibShare
Library   pylib.MobileOpLibAdmin
Library   pylib.ApiSchoolClassLib

Variables   cfg.py

Suite Setup  open_mobile
Suite Teardown  close_mobile

*** Test Cases ***
vcode登录1 - tc006001

    ${ret}  ${info}    vcode_login   xxxxxx

    should be true   $ret==False
    should be true   $info=='登录失败 : vcode format error:1'



vcode登录2 - tc006002

    [Setup]    reset app
    ${ret}  ${info}    vcode_login   ${g_vcode}

    should be true   $ret==True


    ${ret}  ${info}    haveClassInSystem
    should be true   $ret==False
    should be true   $info=='该学校还没有班级，点击刷新'



    ${ret}  ${info}    haveTeacherInSystem
    should be true   $ret==False
    should be true   $info=='该学校还没有老师，点击刷新'

    [Teardown]    reset app



添加班级1 - tc006101
    [Setup]    run keywords   reset app   AND  vcode_login   ${g_vcode}

    ${retInfo}=   addClass   测试班级    1     60
    should be true    $retInfo.startswith('添加成功')

    ${classID}=   evaluate  $retInfo.split('\\n')[1].split('：')[1]
    ${invitecode}=  evaluate  $retInfo.split('：')[-1]

    ${ret}  ${list}    getAllClassesInSystem
    should be true   $ret==True
    should be true   $list==['七年级:测试班级', 'id：${classID}\xa0学生人数：0\xa0人数上限：60']


#列出班级，检验一下
    ${ret2}=    list school class
    ${retlist}=   evaluate   $ret2['retlist']
    classlist should contain   ${retlist}
    ...  测试班级  七年级    ${invitecode}   60   0   ${classID}

    [Teardown]    run keywords   reset app   AND   delete_school_class   ${classID}
