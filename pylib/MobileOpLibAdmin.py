
from pylib.MobileOpLibShare import Mobile_SHARE,open_mobile
import time

class MobileOpLibAdmin:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def vcode_login(self,vcode):

        code = 'new UiSelector().text("请输入vcode")'
        ele = Mobile_SHARE.wd.find_element_by_android_uiautomator(code)
        ele.send_keys(vcode)


        code = 'new UiSelector().text("登录")'
        ele = Mobile_SHARE.wd.find_element_by_android_uiautomator(code)
        ele.click()


        Mobile_SHARE.wd.implicitly_wait(2)
        eles = Mobile_SHARE.wd.find_elements_by_id('android:id/alertTitle')
        Mobile_SHARE.wd.implicitly_wait(10)
        # 找到报错窗口，登录失败
        if eles:
            errInfo = Mobile_SHARE.wd.find_element_by_id('android:id/message').text
            print(errInfo)
            return False,errInfo

        return True,''

    def haveClassInSystem(self):
        Mobile_SHARE.wd.find_element_by_accessibility_id(
            'tabnav-classes'
        ).click()

        Mobile_SHARE.wd.implicitly_wait(2)
        warnings = Mobile_SHARE.wd.find_elements_by_accessibility_id(
            'no-class-warning'
        )

        Mobile_SHARE.wd.implicitly_wait(10)


        if warnings:
            return False,warnings[0].text

        return True,''



    def haveTeacherInSystem(self):
        Mobile_SHARE.wd.find_element_by_accessibility_id(
            'tabnav-teachers'
        ).click()

        Mobile_SHARE.wd.implicitly_wait(2)
        warnings = Mobile_SHARE.wd.find_elements_by_accessibility_id(
            'no-teacher-warning'
        )

        Mobile_SHARE.wd.implicitly_wait(10)


        if warnings:
            return False,warnings[0].text

        return True,''


    def  getAllClassesInSystem(self):
        hasClass,msg = self.haveClassInSystem()
        if not hasClass:
            return hasClass,msg


        Mobile_SHARE.wd.find_element_by_accessibility_id(
            'refresh-class-list'
        ).click()

        time.sleep(2)

        scrollView = Mobile_SHARE.wd.find_element_by_accessibility_id(
            'detail-class-list'
        )




        navteacher = Mobile_SHARE.wd.find_element_by_accessibility_id(
            'tabnav-teachers'
        )
        location = navteacher.location

        x = location['x']

        y1 = location['y'] - 200
        y2 = y1 - 300

        classInfoList = []
        while True:
            tvs = scrollView.find_elements_by_class_name(
                "android.widget.TextView")

            # 处理一屏文本内容
            addNew = False
            for tv in tvs:
                text =tv.text.replace(' ','')
                if len(text) <2:
                    continue

                if text not in classInfoList:
                    classInfoList.append(text)
                    addNew = True

            # 一屏处理完后，看看是否有新增内容
            # 如果没有，表示已经到底部了，退出循环

            if not addNew:
                break

            Mobile_SHARE.wd.swipe(start_x=x,
                                  start_y=y1,
                                  end_x=x,
                                  end_y=y2,
                                  duration=500)


        print(classInfoList)

        return True, classInfoList



    def  getAllTeachersInSystem(self):
        hasTeacher,msg = self.haveTeacherInSystem()
        if not hasTeacher:
            return hasTeacher,msg


        Mobile_SHARE.wd.find_element_by_accessibility_id(
            'refresh-teacher-list'
        ).click()

        time.sleep(2)

        scrollView = Mobile_SHARE.wd.find_element_by_accessibility_id(
            'detail-teacher-list'
        )


        navteacher = Mobile_SHARE.wd.find_element_by_accessibility_id(
            'tabnav-teachers'
        )
        location = navteacher.location

        x = location['x']

        y1 = location['y'] - 200
        y2 = y1 - 300

        teacherInfoList = []
        while True:
            xpath = './/android.widget.TextView[position()=2 or position()=3]'
            tvs = scrollView.find_elements_by_xpath(xpath)

            # 处理一屏文本内容
            addNew = False
            for tv in tvs:
                text =tv.text.replace(' ','')

                if text not in teacherInfoList:
                    teacherInfoList.append(text)
                    addNew = True

            # 一屏处理完后，看看是否有新增内容
            # 如果没有，表示已经到底部了，退出循环

            if not addNew:
                break

            Mobile_SHARE.wd.swipe(start_x=x,
                                  start_y=y1,
                                  end_x=x,
                                  end_y=y2,
                                  duration=500)


        print(teacherInfoList)

        return True, teacherInfoList


    def addClass(self,className,gradeId,studentLimit):
        # 确保进入班级标签页
        Mobile_SHARE.wd.find_element_by_accessibility_id(
            'tabnav-classes'
        ).click()


        # 点击添加图标
        Mobile_SHARE.wd.find_element_by_accessibility_id(
            'IconAddClass'
        ).click()

        time.sleep(1)

        # 输入班级 信息
        code = 'new UiSelector().text("班级名称").className("android.widget.EditText")'
        ele = Mobile_SHARE.wd.find_element_by_android_uiautomator(code)
        ele.send_keys(className)



        code = 'new UiSelector().text("年级ID").className("android.widget.EditText")'
        ele = Mobile_SHARE.wd.find_element_by_android_uiautomator(code)
        ele.send_keys(str(gradeId))

        code = 'new UiSelector().text("人数上限").className("android.widget.EditText")'
        ele = Mobile_SHARE.wd.find_element_by_android_uiautomator(code)
        ele.send_keys(str(studentLimit))

        # 点击添加按钮
        code = 'new UiSelector().text("添加").className("android.widget.TextView")'
        Mobile_SHARE.wd.find_element_by_android_uiautomator(code).click()

        #获取添加结果
        retInfo = Mobile_SHARE.wd.find_element_by_id('android:id/message').text

        # 点击ok
        Mobile_SHARE.wd.find_element_by_id("android:id/button1").click()

        return retInfo



    def addTeacher(self,username,
                   realname,
                   subjectid,
                   classlist,
                   phonenumber,
                   email,
                   idcardnumber,
                   goback=True):
        # 确保进入老师标签页
        Mobile_SHARE.wd.find_element_by_accessibility_id(
            'tabnav-teachers'
        ).click()


        # 点击添加图标
        Mobile_SHARE.wd.find_element_by_accessibility_id(
            'IconAddTeacher'
        ).click()

        time.sleep(1)


        code = 'new UiSelector().text("老师真实姓名").className("android.widget.EditText")'
        ele = Mobile_SHARE.wd.find_element_by_android_uiautomator(code)
        ele.send_keys(realname)


        code = 'new UiSelector().text("登录名").className("android.widget.EditText")'
        ele = Mobile_SHARE.wd.find_element_by_android_uiautomator(code)
        ele.send_keys(username)


        code = 'new UiSelector().text("学科ID号").className("android.widget.EditText")'
        ele = Mobile_SHARE.wd.find_element_by_android_uiautomator(code)
        ele.send_keys(str(subjectid))


        code = 'new UiSelector().textContains("班级ID号").className("android.widget.EditText")'
        ele = Mobile_SHARE.wd.find_element_by_android_uiautomator(code)
        ele.send_keys(str(classlist))


        code = 'new UiSelector().text("电话号码").className("android.widget.EditText")'
        ele = Mobile_SHARE.wd.find_element_by_android_uiautomator(code)
        ele.send_keys(phonenumber)


        code = 'new UiSelector().text("邮箱").className("android.widget.EditText")'
        ele = Mobile_SHARE.wd.find_element_by_android_uiautomator(code)
        ele.send_keys(email)

        code = 'new UiSelector().text("身份证号").className("android.widget.EditText")'
        ele = Mobile_SHARE.wd.find_element_by_android_uiautomator(code)
        ele.send_keys(idcardnumber)



        # 点击添加按钮
        code = 'new UiSelector().text("添加").className("android.widget.TextView")'
        Mobile_SHARE.wd.find_element_by_android_uiautomator(code).click()

        #获取添加结果
        retInfo = Mobile_SHARE.wd.find_element_by_id('android:id/message').text

        # 点击ok
        Mobile_SHARE.wd.find_element_by_id("android:id/button1").click()

        if goback:
            # 点击返回按钮
            code = 'new UiSelector().text("返回").className("android.widget.TextView")'
            Mobile_SHARE.wd.find_element_by_android_uiautomator(code).click()


        return retInfo



if __name__ == '__main__':
    open_mobile()
    ma = MobileOpLibAdmin()
    ma.getAllTeachersInSystem()