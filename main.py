# This Python file uses the following encoding: utf-8
import sys
import requests
from PySide6.QtWidgets import QApplication, QWidget, QPushButton,QStackedWidget,QSpacerItem,QFileDialog,QHeaderView
from PySide6.QtGui import QPalette,QStandardItemModel,QStandardItem
from PySide6.QtCore import Qt, QThread, Signal,QDate
from urllib import parse
import base64
from bs4 import BeautifulSoup
from PySide6.QtGui import QPixmap
from os import system as CmdCommand
from pathlib import Path
# 导入编译后的主UI和子UI类
from ui_py.ui_form import Ui_mian
from ui_py.ui_userInfo import Ui_userInfo
from ui_py.ui_login import Ui_login
from ui_py.ui_selfPrint import Ui_selfPrint
from ui_py.ui_examSearch import Ui_examSearch
from ui_py.ui_classSchedule import Ui_classSchedule
#配置
baseUrl = "http://jwxt.ahut.edu.cn/jsxsd/"
loginSuf = "xk/LoginToXk"
userImgUrlSuf = "framework/student/images/zp.jpg"
cheakLoginStateUrlSuf = "framework/main_index_loadkb.jsp"
userInfoSuf = "framework/xsMain_new.jsp"
loginBgUrlSuf = "framework/student/images/xs_bg.jpg"
semesterUrlSuf = "xsks/xsksap_query"
examListSuf1 = "xsks/xsksap_list"
examListSuf2 = "xsks/xsstk_list"
printListSuf = "view/cjgl/zzdy_list.jsp"
classScheduleUrlSuf = "framework/main_index_loadkb.jsp"
session = requests.Session()
session.headers.update({"X-Requested-With" : "XMLHttpRequest"})
toolButtonNameList = ["userInfo_button",
                      "selfPrint_button",
                      "examSearch_button",
                      "classSchedule_button",
                      "robClasses_button",
                      "settings_button",
                      "appInfo_button"]
userId = ""
userpwd = ""
logined = False
userName = ""
userDepartment = ""
userMajor = ""
userClass = ""
userAvatar = None
semester = ""
currDate = QDate.currentDate().toString("yyyy-MM-dd")


#主界面
class Main(QWidget):
    global logined
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_mian()
        self.ui.setupUi(self)
        #加载所有子ui
        self.subWidget = QStackedWidget(self)
        self.ui.subWidget.layout().addWidget(self.subWidget)
        self.ui_login_widget = Ui_login_widget()
        self.ui_userInfo_widget = Ui_userInfo_widget()
        self.ui_selfPrint_widget = Ui_selfPrint_widget()
        self.ui_examSearch_widget = Ui_examSearch_widget()
        self.ui_classSchedule_widget = Ui_classSchedule_widget()
        self.subWidget.addWidget(self.ui_login_widget)
        self.subWidget.addWidget(self.ui_userInfo_widget)
        self.subWidget.addWidget(self.ui_selfPrint_widget)
        self.subWidget.addWidget(self.ui_examSearch_widget)
        self.subWidget.addWidget(self.ui_classSchedule_widget)
        #连接登录成功信号
        self.ui_login_widget.loginSuccess.connect(lambda state,message:self.on_login_result(state,message))
        #登录失效信号
        self.ui_userInfo_widget.loginExpiredSignal.connect(lambda message:self.loginExpired(message))

        #绑定工具栏的按钮事件
        self.ui.userInfo_button.clicked.connect(lambda :self.enable_Ui_userInfo_widget())
        self.ui.selfPrint_button.clicked.connect(lambda :self.enable_Ui_selfPrint_widget())
        self.ui.examSearch_button.clicked.connect(lambda :self.enable_Ui_examSearch_widget())
        self.ui.classSchedule_button.clicked.connect(lambda :self.enable_Ui_classSchedule_widget())
    
    def on_login_result(self, state:bool, message:str):
        if state:
            self.subWidget.setCurrentWidget(self.ui_userInfo_widget)
            self.ui_userInfo_widget.getUserInfo()

    def loginExpired(self, message:str = ""):
        restoreAllToolButton(self)
        self.subWidget.setCurrentWidget(self.ui_login_widget)
        self.ui_login_widget.setMessageShow(message,color=Qt.red)
    
    #侧边栏 用户信息被点击
    def enable_Ui_userInfo_widget(self):
        print("侧边栏用户信息按钮被点击\n")
        restoreAllToolButton(self)
        self.ui.userInfo_button.setEnabled(False)
        self.subWidget.setCurrentWidget(self.ui_userInfo_widget)

    #侧边栏 自助打印被点击
    def enable_Ui_selfPrint_widget(self):
        print("侧边栏自助打印按钮被点击\n")
        if logined:
            restoreAllToolButton(self)
            self.ui.selfPrint_button.setEnabled(False)
            self.subWidget.setCurrentWidget(self.ui_selfPrint_widget)
        else:
            self.loginExpired("你还没有登录哦~")

    #侧边栏 考试查询被点击
    def enable_Ui_examSearch_widget(self):
        print("侧边栏考试查询按钮被点击\n")
        if logined:
            restoreAllToolButton(self)
            self.ui.examSearch_button.setEnabled(False)
            self.subWidget.setCurrentWidget(self.ui_examSearch_widget)
        else:
            self.loginExpired("你还没有登录哦~")

    #侧边栏 课程表查询被点击
    def enable_Ui_classSchedule_widget(self):
        print("侧边栏课程表按钮被点击\n")
        if logined:
            restoreAllToolButton(self)
            self.ui.classSchedule_button.setEnabled(False)
            self.subWidget.setCurrentWidget(self.ui_classSchedule_widget)
        else:
            self.loginExpired("你还没有登录哦~")

#登录子界面
class Ui_login_widget(QWidget):
    loginSuccess = Signal(bool, str)
    def __init__(self, parent:type = None):
        super().__init__(parent)
        self.ui_login = Ui_login()
        self.ui_login.setupUi(self)
        self.ui_login.login_button.clicked.connect(self.on_login_button_clicked)
        self.loginThread = None
        self.getLoginBgThread = None
        print("ui_login_widget实例已创建\n")
        self.getLoginBg()

    def setMessageShow(self, message:str, color:Qt.GlobalColor = Qt.red):
        paletter = QPalette()
        paletter.setColor(QPalette.WindowText, color)
        self.ui_login.messageShow.setPalette(paletter)
        self.ui_login.messageShow.setText(message)
    
    def on_login_button_clicked(self):
        global userId, userpwd,semester
        print("登录按钮被点击\n")
        semester = ""
        userId = self.ui_login.login_idInput.text()
        userpwd = self.ui_login.login_pwdInput.text()
        if not userId or not userpwd:
            self.setMessageShow("请输入用户名和密码",color=Qt.red)
            return
        
        if not self.ui_login.used_accept.isChecked():
            self.setMessageShow("请勾选同意协议",color=Qt.red)
            return

        self.setMessageShow("正在登录...",color=Qt.yellow)
        self.ui_login.login_button.setEnabled(False)
        login(self, self.login_returnFunction)
        
    def login_returnFunction(self,state:bool,message:str):
        if state:
            self.setMessageShow(message,color=Qt.green)
            self.loginSuccess.emit(state,message)
        else:
            self.setMessageShow(message,color=Qt.red)
        self.ui_login.login_button.setEnabled(True)
    
    def getLoginBg(self):
        print("正在获取登录界面背景...\n")
        loginBgUrl = parse.urljoin(baseUrl, loginBgUrlSuf)
        try:
            if not self.getLoginBgThread:
                self.getLoginBgThread = GetRequestThread(url=loginBgUrl, timeout=5)
                self.getLoginBgThread.resultSignal.connect(self.fillLoginBg)
            if not self.getLoginBgThread.isRunning():
                self.getLoginBgThread.start()
        except Exception as e:
            print("获取登录界面背景异常:" + str(e) + "\n")
            self.setMessageShow("获取登录界面背景异常:" + str(e),color=Qt.red)
    
    def fillLoginBg(self,state:bool = False,message:str = "",response:requests.Response = None):
        if not state:
            print(message + "\n")
            self.setMessageShow(message,color=Qt.red)
            return
        loginBgData = response.content
        pixmap = QPixmap()
        pixmap.loadFromData(loginBgData)
        self.ui_login.loginBg.setPixmap(pixmap)
        print("登录界面背景获取成功!\n")

#用户信息子界面
class Ui_userInfo_widget(QWidget):
    loginExpiredSignal = Signal(str)

    def __init__(self, parent:type = None):
        super().__init__(parent)
        self.Ui_userInfo = Ui_userInfo()
        self.Ui_userInfo.setupUi(self)
        self.loginThread = None
        #绑定退出登录按钮事件
        self.Ui_userInfo.loginOut_button.clicked.connect(self.loginOut)
        self.getUserInfoThread = None
        self.getuserAvatarThread = None
        self.getsemesterThread = None


    def loginExpired(self, state:bool = False,message:str = ""):
        if not state:
            self.loginExpiredSignal.emit(message)
        
    def showEvent(self, event):
        super().showEvent(event)
        if not logined:
            self.loginExpired(False, "你还没有登录哦~")
            return
        login(self, self.loginExpired)
        print("Ui_userInfo_widget显示事件被触发\n")

        #获取当前学期
        if semester == "":
            print("正在获取当前学期...\n")
            self.setMessageShow("正在获取当前学期...",color=Qt.yellow)
            if not self.getsemesterThread:
                self.getsemesterThread = GetRequestThread(parse.urljoin(baseUrl, semesterUrlSuf))
                self.getsemesterThread.resultSignal.connect(self.fillSemester)
            if not self.getsemesterThread.isRunning():
                self.getsemesterThread.start()
        return

    def fillSemester(self,state:bool = False,message:str = "",response:requests.Response = None):
        if not state:
            self.setMessageShow(message,color=Qt.red)
            print(message + "\n")
            return
        global semester
        soup = BeautifulSoup(response.text, "lxml")
        semester = soup.find("option", selected=True)
        if not semester:
            self.setMessageShow("获取当前学期失败",color=Qt.red)
            print("获取当前学期失败\n")
            return
        semester = semester.get("value","")
        self.setMessageShow("当前学期:" + semester,color=Qt.green)
        print("当前学期:" + semester + "\n")

    def loginOut(self):
        global userName
        global session, logined
        session.cookies.clear()
        logined = False
        userName = ""
        self.loginExpired(False, "你已退出登录~")

    def getUserInfo(self):
        #获取用户信息
        print("正在获取用户信息...\n")
        self.setMessageShow("正在获取用户信息...",color=Qt.yellow)
        userInfoUrl = parse.urljoin(baseUrl, userInfoSuf)
        try:
            if not self.getUserInfoThread:
                self.getUserInfoThread = GetRequestThread(url=userInfoUrl, timeout=5)
                self.getUserInfoThread.resultSignal.connect(self.fillUserInfo)
            if not self.getUserInfoThread.isRunning():
                self.getUserInfoThread.start()
        except Exception as e:
            self.setMessageShow("获取用户信息异常:" + str(e),color=Qt.red)
            print("获取用户信息异常:" + str(e) + "\n")
        
        #获取用户头像
        print("正在获取用户头像...\n")
        self.setMessageShow("正在获取用户头像...",color=Qt.yellow)
        userAvatarUrl = parse.urljoin(baseUrl, userImgUrlSuf)
        try:
            if not self.getuserAvatarThread:
                self.getuserAvatarThread = GetRequestThread(url=userAvatarUrl, timeout=5)
                self.getuserAvatarThread.resultSignal.connect(self.fillUserAvatar)
            if not self.getuserAvatarThread.isRunning():
                self.getuserAvatarThread.start()
        except Exception as e:
            self.setMessageShow("获取用户头像异常:" + str(e),color=Qt.red)
            print("获取用户头像异常:" + str(e) + "\n")

    #回调:解析用户头像并填入界面
    def fillUserAvatar(self,state:bool = False,message:str = "",response:requests.Response = None):
        if not state:
            self.setMessageShow(message,color=Qt.red)
            print(message + "\n")
            return
        global userAvatar
        userAvatar = response.content
        pixmap = QPixmap()
        pixmap.loadFromData(userAvatar)
        self.Ui_userInfo.userAvatar.setPixmap(pixmap)
        self.setMessageShow("用户头像获取成功!",color=Qt.green)
        print("用户头像获取成功!\n")

    #回调:解析用户信息并填入界面
    def fillUserInfo(self,state:bool = False,message:str = "",response:requests.Response = None):
        #print(f"{type(response)}\n")
        if not state:
            self.setMessageShow(message,color=Qt.red)
            print(message + "\n")
            return
        self.setMessageShow("填入用户信息中...",color=Qt.green)
        global userName, userDepartment, userMajor, userClass, userId
        soup = BeautifulSoup(response.text, "lxml")
        try:
            userInfoList = soup.find_all("div",class_ = "middletopdwxxcont")
            userName = userInfoList[1].text.strip()
            userId = userInfoList[2].text.strip()
            userDepartment = userInfoList[3].text.strip()
            userMajor = userInfoList[4].text.strip()
            userClass = userInfoList[5].text.strip()
            self.Ui_userInfo.userName.setText(userName)
            self.Ui_userInfo.userId.setText(userId)
            self.Ui_userInfo.userDepartment.setText(userDepartment)
            self.Ui_userInfo.userMajor.setText(userMajor)
            self.Ui_userInfo.userClass.setText(userClass)
            self.setMessageShow("用户信息获取成功!",color=Qt.green)
            print("用户信息获取成功!\n")
        except Exception as e:
            self.setMessageShow("解析用户信息异常:" + str(e),color=Qt.red)
            print("解析用户信息异常:" + str(e) + "\n")

    def setMessageShow(self, message:str, color:Qt.GlobalColor = Qt.red):
        paletter = QPalette()
        paletter.setColor(QPalette.WindowText, color)
        self.Ui_userInfo.messageShow.setPalette(paletter)
        self.Ui_userInfo.messageShow.setText(message)

#自助打印界面
class Ui_selfPrint_widget(QWidget):
    def __init__(self, parent:type = None):
        super().__init__(parent)
        self.ui_selfPrint = Ui_selfPrint()
        self.ui_selfPrint.setupUi(self)
        self.getPrintListThreading = None
        self.downloadPrintFile = None
    
    def getPrintList(self):
        printListUrl = parse.urljoin(baseUrl, printListSuf)
        if not self.getPrintListThreading:
            self.getPrintListThreading = GetRequestThread(printListUrl)
            self.getPrintListThreading.resultSignal.connect(self.fillPrintList)
        if not self.getPrintListThreading.isRunning():
            self.getPrintListThreading.start()
    
    def fillPrintList(self,state:bool = False,message:str = "",response:requests.Response = None):
        try:
            if not state:
                self.setMessageShow(message,color=Qt.red)
                return

            while self.ui_selfPrint.printListArea.widget().layout().count() > 0:
                topBox = self.ui_selfPrint.printListArea.widget().layout().takeAt(0)
                button = topBox.widget()
                if button:
                    button.deleteLater()
                else:
                    del topBox
            items = BeautifulSoup(response.text,"lxml").find_all("input",type = "button",class_ = "button el-button")
            for item in items:
                buttonName = item.get("value")
                if not buttonName:
                    continue
                buttonUrlSuf = item.get("onclick").replace("zzdy('","").replace("')","").strip()#获取的链接有多余
                print("添加按钮:" + buttonName + "  " + buttonUrlSuf,end="\n")
                btn = QPushButton(buttonName)
                self.ui_selfPrint.printListArea.widget().layout().addWidget(btn)
                btn.clicked.connect(lambda clicked,name = buttonName,UrlSuf=buttonUrlSuf:self.printButtonClicked(name,UrlSuf))
            space = QSpacerItem(40, 20)
            self.ui_selfPrint.printListArea.widget().layout().addItem(space)

        except Exception as e:
            print("解析打印列表异常:" + str(e) + "\n")
            self.setMessageShow("解析打印列表异常:" + str(e),color=Qt.red)
    
    def printButtonClicked(self,ButtonName:str,linkUrlSuf:str = None):
        if not linkUrlSuf:
            print(f"打印按钮{ButtonName}被点击，但链接为空\n")
            self.setMessageShow(f"打印按钮{ButtonName}被点击，但链接为空",color=Qt.red)
            return
        printUrl = parse.urljoin(baseUrl, linkUrlSuf)
        print(f"打印按钮{ButtonName}被点击，链接为{printUrl}\n")
        try:
            if not self.downloadPrintFile:
                self.downloadPrintFile = GetRequestThread(printUrl)
                self.downloadPrintFile.resultSignal.connect(self.savePrintFile)
            if self.downloadPrintFile.isRunning():
                self.setMessageShow("已经有一个下载任务了，请稍后再试")
                return
            
            self.setMessageShow(f"请选择保存路径",color=Qt.yellow)
            self.destPath = QFileDialog.getExistingDirectory(
                self,
                f"选择文件夹以保存 {ButtonName}.pdf",
                None,
                QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
            )

            # 判断用户是否选择了文件夹（点击取消则返回空字符串）
            if self.destPath:
                print(f"选中的文件夹路径：{self.destPath}")
            else:
                print("用户取消了选择")
                self.setMessageShow("您取消了选择",color=Qt.yellow)
                return

            self.downloadPrintFile.start()
            self.setMessageShow(f"正在下载{ButtonName}的打印文件...",color=Qt.yellow)
            print(f"正在下载{ButtonName}的打印文件...\n")
            self.fileName = ButtonName + ".pdf"
        except Exception as e:
            self.setMessageShow(f"打开打印页面异常:" + str(e),color=Qt.red)
            print(f"打开打印页面异常:" + str(e) + "\n")
            raise

    def savePrintFile(self,state:bool = False,message:str = "",response:requests.Response = None):
        self.downloadPrintFile.deleteLater()
        self.downloadPrintFile = None
        if not state:
            self.setMessageShow(message,color=Qt.red)
            print(message + "\n")
            return
        
        if response.status_code != 200:
            self.setMessageShow(f"下载{self.fileName}失败，状态码为{response.status_code},你可能没有相关成绩!",color=Qt.red)
            print(f"下载{self.fileName}失败，状态码为{response.status_code},你可能没有相关成绩!\n")
            return
        
        try:
            dest = self.destPath + "/" + self.fileName
            with open(dest, "wb") as f:
                f.write(response.content)
        except Exception as e:
            self.setMessageShow(f"保存打印文件异常:" + str(e),color=Qt.red)
            print(f"保存打印文件异常:" + str(e) + "\n")
            return
        self.setMessageShow(f"{dest} 保存成功!",color=Qt.green)
        print(f"{dest} 保存成功!\n")
       
    def showEvent(self, event):
        super().showEvent(event)
        self.getPrintList()
        return
    
    def setMessageShow(self, message:str, color:Qt.GlobalColor = Qt.red):
        paletter = QPalette()
        paletter.setColor(QPalette.WindowText, color)
        self.ui_selfPrint.messageShow.setPalette(paletter)
        self.ui_selfPrint.messageShow.setText(message)

#考试查询界面
class Ui_examSearch_widget(QWidget):
    def __init__(self, parent:type = None):
        super().__init__(parent)
        self.ui_examSearch = Ui_examSearch()
        self.ui_examSearch.setupUi(self)
        self.getExamListThreading1 = None
        self.getExamListThreading2 = None
        self.DataModel1 = QStandardItemModel()
        self.ui_examSearch.examTable1.setModel(self.DataModel1)
        self.DataModel2 = QStandardItemModel()
        self.ui_examSearch.examTable2.setModel(self.DataModel2)

    def getExamList(self):
        self.DataModel1.setRowCount(0)
        self.DataModel2.setRowCount(0)
        if not self.getExamListThreading1:
            self.getExamListThreading1 = PostRequestThread(parse.urljoin(baseUrl, examListSuf1),data={"xnxqid":semester})
            self.getExamListThreading1.resultSignal.connect(self.fillExamList1)
        if not self.getExamListThreading1.isRunning():
            self.getExamListThreading1.start()
        if not self.getExamListThreading2:
            self.getExamListThreading2 = PostRequestThread(parse.urljoin(baseUrl, examListSuf2),data={"xnxqid":semester})
            self.getExamListThreading2.resultSignal.connect(self.fillExamList2)
        if not self.getExamListThreading2.isRunning():
            self.getExamListThreading2.start()
        
    def fillExamList1(self,state:bool = False,message:str = "",response:requests.Response = None):
        try:
            if not state:
                self.setMessageShow(message,color=Qt.red)
                print(message + "\n")
                return
            soup = BeautifulSoup(response.text, "lxml")
            examList = soup.find("table",class_ = "Nsb_r_list Nsb_table")
            if not examList:
                self.setMessageShow1("获取考试列表1失败",color=Qt.red)
                print("获取考试列表1失败\n")
                return

            examList = examList.find_all("tr")
            self.colCnt = len(examList[0].find_all("th"))
            self.DataModel1.setColumnCount(self.colCnt)
            self.DataModel1.setHorizontalHeaderLabels([str(item.text.strip()) for item in examList[0].find_all("th")])

            if len(examList[1].find_all("td")) == 1:
                print("暂无集中考试\n")
                self.setMessageShow1("暂无集中考试↑",color=Qt.green)
                return
            else:
                self.setMessageShow1("集中考试↑",color=Qt.yellow)

            for items in examList[1:]:
                self.DataModel1.appendRow([QStandardItem(str(item.text.strip())) for item in items.find_all("td")])
            self.ui_examSearch.examTable1.setModel(self.DataModel1)
        except Exception as e:
            print("解析考试列表1异常:" + str(e) + "\n")
            self.setMessageShow("解析考试列表异常1:" + str(e),color=Qt.red)
    
    def fillExamList2(self,state:bool = False,message:str = "",response:requests.Response = None):
        try:
            if not state:
                self.setMessageShow(message,color=Qt.red)
                print(message + "\n")
                return
            soup = BeautifulSoup(response.text, "lxml")
            examList = soup.find("table",class_ = "Nsb_r_list Nsb_table")
            if not examList:
                self.setMessageShow("获取考试列表2失败",color=Qt.red)
                print("获取考试列表2失败\n")
                return
            else:
                self.setMessageShow("分散考试↑",color=Qt.yellow)

            examList = examList.find_all("tr")
            self.colCnt = len(examList[0].find_all("th"))
            self.DataModel2.setColumnCount(self.colCnt)
            self.DataModel2.setHorizontalHeaderLabels([str(item.text.strip()) for item in examList[0].find_all("th")])

            if len(examList[1].find_all("td")) == 1:
                self.setMessageShow("暂无分散考试↑",color=Qt.green)
                print("暂无分散考试\n")
                return

            for items in examList[1:]:
                self.DataModel2.appendRow([QStandardItem(str(item.text.strip())) for item in items.find_all("td")])
            self.ui_examSearch.examTable2.setModel(self.DataModel2)
        except Exception as e:
            print("解析考试列表2异常:" + str(e) + "\n")
            self.setMessageShow("解析考试列表异常2:" + str(e),color=Qt.red)
    

    def showEvent(self, event):
        super().showEvent(event)
        if semester == "":
            self.setMessageShow("当前学期获取失败,请尝试重新登录",color=Qt.red)
            return
        self.getExamList()
        return
    
    def setMessageShow(self, message:str, color:Qt.GlobalColor = Qt.red):
        paletter = QPalette()
        paletter.setColor(QPalette.WindowText, color)
        self.ui_examSearch.messageShow.setPalette(paletter)
        self.ui_examSearch.messageShow.setText(message)
    
    def setMessageShow1(self, message:str, color:Qt.GlobalColor = Qt.red):
        paletter = QPalette()
        paletter.setColor(QPalette.WindowText, color)
        self.ui_examSearch.messageShow1.setPalette(paletter)
        self.ui_examSearch.messageShow1.setText(message)

#课程表界面
class Ui_classSchedule_widget(QWidget):
    def __init__(self, parent:type = None):
        super().__init__(parent)
        self.ui_classSchedule = Ui_classSchedule()
        self.ui_classSchedule.setupUi(self)
        self.ui_classSchedule.dateEdit.setDate(QDate.currentDate())
        self.getClassScheduleThreading = None

        #绑定查询按钮
        self.ui_classSchedule.search.clicked.connect(self.getClassSchedule)
        #绑定tableview
        self.tableModel = QStandardItemModel()

    def getClassSchedule(self):
        selectDate = self.ui_classSchedule.dateEdit.date().toString("yyyy-MM-dd")
        if self.getClassScheduleThreading:
            if self.getClassScheduleThreading.isRunning():
                self.setMessageShow("已经有一个查询任务了，请稍后再试",color=Qt.red)
                print("已经有一个查询任务了，请稍后再试\n")
                return
            else:
                self.getClassScheduleThreading.deleteLater()
        self.getClassScheduleThreading = PostRequestThread(parse.urljoin(baseUrl, classScheduleUrlSuf),data = {"rq" : selectDate})
        self.getClassScheduleThreading.resultSignal.connect(self.fillClassSchedule)
        self.getClassScheduleThreading.start()
        self.setMessageShow("正在查询课程表..." + selectDate,color=Qt.yellow)
        print("正在查询课程表...\n")
        
    def fillClassSchedule(self,state:bool = False,message:str = "",response:requests.Response = None):
        try:
            if not state:
                self.setMessageShow(message,color=Qt.red)
                print(message + "\n")
                return
            
            soup = BeautifulSoup(response.text.replace("<br>","\n").replace("</br>","\n").replace("<br/>","\n"), "lxml")
            items = soup.find_all("tr")
            colCnt = len(items[0].find_all("th"))
            self.tableModel.setColumnCount(colCnt)
            self.tableModel.setRowCount(0)
            self.tableModel.setHorizontalHeaderLabels([str(item.text.strip()) for item in items[0].find_all("th")])

            if len(items) == 1:
                self.setMessageShow("暂无课程信息",color=Qt.green)
                print("暂无课程信息\n")
                return

            showDetail = self.ui_classSchedule.showDetail.isChecked()

            for item in items[1:]:
                if showDetail:
                    self.tableModel.appendRow([QStandardItem( str( td.text if td.find("p") == None else td.find("p").get("title","")).replace("\n\n","\n").strip() ) for td in item.find_all("td")])
                else:
                    self.tableModel.appendRow([QStandardItem( str( td.text if td.find("p") == None else td.find("p").text).replace(" ","").strip() ) for td in item.find_all("td")])
            self.ui_classSchedule.classScheduleTable.setModel(self.tableModel)

            self.setMessageShow("解析课程表成功!",color=Qt.green)
            print("解析课程表成功!\n")
        except Exception as e:
            print("解析课程表异常:" + str(e) + "\n")
            self.setMessageShow("解析课程表异常:" + str(e),color=Qt.red)
    
    def setMessageShow(self, message:str, color:Qt.GlobalColor = Qt.red):
        paletter = QPalette()
        paletter.setColor(QPalette.WindowText, color)
        self.ui_classSchedule.messageShow.setPalette(paletter)
        self.ui_classSchedule.messageShow.setText(message)
            
#登录线程
class LoginThread(QThread): 
    global session, userId, userpwd
    result = Signal(bool, str)
    def __init__(self):
        super().__init__()
    def run(self):
        global logined
        try:
            cheakLoginStateUrl = parse.urljoin(baseUrl, cheakLoginStateUrlSuf)
            loginUrl = parse.urljoin(baseUrl, loginSuf)
            postData = {
                "userAccount": userId,
                "userPassword": "",
                "encoded" : base64.b64encode(userId.encode("utf-8")).decode("utf-8") + "%%%" + base64.b64encode(userpwd.encode("utf-8")).decode("utf-8")
            }
        except Exception as e:
            self.result.emit(False, "URL拼接异常:" + str(e))
            return False, "URL拼接异常:" + str(e)
        
        #判断是否登录过
        if userId == "":
            self.result.emit(False, "你还没有登录过哦~")
            return False, "你还没有登录过哦~"

        #检测是否已经登录
        try:
            response = session.get(cheakLoginStateUrl, timeout=5)
            if "星" in response.text:
                self.result.emit(True, "已登录,无需再次登录")
                return True, "已登录,无需再次登录"
        except Exception as e:
            self.result.emit(False, "网络异常:" + str(e))
            return False, "网络异常:" + str(e)
        
        #执行登录
        try:
            response = session.post(loginUrl, data=postData, timeout=5)
        except Exception as e:
            self.result.emit(False, "网络异常:" + str(e))
            return False, "网络异常:" + str(e)
        
        #检测是否已经登录
        try:
            response = session.get(cheakLoginStateUrl, timeout=5)
            if "星" in response.text:
                logined = True
                self.result.emit(True, "登录成功!")
                return True, "登录成功!"
            else:
                self.result.emit(False, "用户名或密码错误!")
                return False, "用户名或密码错误!"
        except Exception as e:
            self.result.emit(False, "网络异常:" + str(e))
            return False, "网络异常:" + str(e)

#登录方法（在主线程调用，自动切换到登录线程执行，并通过回调函数返回结果）
def login(self,returnFunction:type = None):
    global session, userId, userpwd
    if not self.loginThread:
        self.loginThread = LoginThread()
        self.loginThread.result.connect(lambda state,message:returnFunction(state,message))

    if not self.loginThread.isRunning():
        self.loginThread.start()

#多线程get请求的通用方法（传入URL和回调函数，自动处理异常和结果回调）
class GetRequestThread(QThread):
    global session
    resultSignal = Signal(int, str, requests.Response)  # 定义一个信号，传递请求结果（成功与否和消息）
    def __init__(self, url:str = "",params:dict = {},timeout:int = 5):
        super().__init__()
        self.url = url
        self.params = params
        self.timeout = timeout

    def run(self):
        try:
            response = session.get(self.url, params=self.params, timeout=self.timeout)
            self.resultSignal.emit(1, "",response)
        except Exception as e:
            self.resultSignal.emit(0, "网络异常:" + str(e),None)

#多线程post请求的通用方法（传入URL、数据和回调函数，自动处理异常和结果回调）
class PostRequestThread(QThread):
    global session
    resultSignal = Signal(int, str,requests.Response)  # 定义一个信号，传递请求结果（成功与否和消息）
    def __init__(self, url:str = "", data:dict = None,timeout:int = 5):
        super().__init__()
        self.url = url
        self.data = data
        self.timeout = timeout

    def run(self):
        try:
            response = session.post(self.url, data=self.data, timeout=self.timeout)
            self.resultSignal.emit(1, "",response)
        except Exception as e:
            self.resultSignal.emit(0, "网络异常:" + str(e),None)

#恢复所有按钮为可点击状态
def restoreAllToolButton(mainWindow):
    for btnName in toolButtonNameList:
        mainWindow.ui.__getattribute__(btnName).setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Main()
    widget.show()
    sys.exit(app.exec())