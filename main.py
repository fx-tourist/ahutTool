# This Python file uses the following encoding: utf-8
import sys
import requests
from PySide6.QtWidgets import QApplication, QWidget, QPushButton,QStackedWidget,QSpacerItem,QFileDialog
from PySide6.QtGui import QPalette,QStandardItemModel,QStandardItem,QMovie
from PySide6.QtCore import Qt, QThread, Signal,QDate, QRunnable, QThreadPool,Slot,QObject
from PySide6.QtGui import QPixmap,QIcon
from urllib import parse
import base64 
from bs4 import BeautifulSoup
import os,json
from time import sleep as time_sleep
# 导入编译后的主UI和子UI类
from ui_py.ui_form import Ui_main
from ui_py.ui_userInfo import Ui_userInfo
from ui_py.ui_login import Ui_login
from ui_py.ui_selfPrint import Ui_selfPrint
from ui_py.ui_examSearch import Ui_examSearch
from ui_py.ui_classSchedule import Ui_classSchedule
from ui_py.ui_appInfo import Ui_appInfo
from ui_py.ui_loading import Ui_loading
from ui_py.ui_robClasses import Ui_robClasses
#导入资源文件
from img_py.img_icon import *
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
appInfoMessageUrl = "http://127.0.0.1:9999/"
robClassesUrl = "http://127.0.0.1:10000/robclasses"
session = requests.Session()
session.headers.update({"X-Requested-With" : "XMLHttpRequest"})
toolButtonNameList = ["userInfo_button",
                      "selfPrint_button",
                      "examSearch_button",
                      "classSchedule_button",
                      "robClasses_button",
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
appVersion = "2.0"
appDataDes = os.path.join(os.getenv("APPDATA"),"ahutTool")
loginOptionsData = {}
app = QApplication(sys.argv)
threadPool = QThreadPool.globalInstance()

#主界面
class Main(QWidget):
    global logined
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_main()
        self.ui.setupUi(self)
        self.setWindowTitle("Ahut Tool 2.0")
        self.setWindowIcon(QIcon(":/icon/icon_256.svg"))
        #加载所有子ui
        self.subWidget = QStackedWidget(self)
        self.ui.subWidget.layout().addWidget(self.subWidget)
        self.ui_login_widget = Ui_login_widget()
        self.ui_userInfo_widget = Ui_userInfo_widget()
        self.ui_selfPrint_widget = Ui_selfPrint_widget()
        self.ui_examSearch_widget = Ui_examSearch_widget()
        self.ui_classSchedule_widget = Ui_classSchedule_widget()
        self.ui_appInfo_widget = Ui_appInfo_widget()
        self.ui_loading_widget = Ui_loading_widget()
        self.ui_robClasses_widget = Ui_robClasses_widget()
        self.subWidget.addWidget(self.ui_login_widget)
        self.subWidget.addWidget(self.ui_userInfo_widget)
        self.subWidget.addWidget(self.ui_selfPrint_widget)
        self.subWidget.addWidget(self.ui_examSearch_widget)
        self.subWidget.addWidget(self.ui_classSchedule_widget)
        self.subWidget.addWidget(self.ui_appInfo_widget)
        self.subWidget.addWidget(self.ui_loading_widget)
        self.subWidget.addWidget(self.ui_robClasses_widget)
        #连接登录成功信号
        self.ui_login_widget.loginSuccess.connect(lambda state,message:self.on_login_result(state,message))
        #登录失效信号
        self.ui_userInfo_widget.loginExpiredSignal.connect(lambda message:self.loginExpired(message))

        #初始化抢课模块
        self.ui_robClasses_widget.setUiClass(self.ui_robClasses_widget)
        self.ui_robClasses_widget.setLoadingProgress.connect(self.setLoadingProgress)
        self.ui_robClasses_widget.showLoding.connect(self.loadingShow)
        self.ui_robClasses_widget.setLoadingMessage.connect(self.setLoadingMessage)

        #绑定工具栏的按钮事件
        self.ui.userInfo_button.clicked.connect(lambda :self.enable_Ui_userInfo_widget())
        self.ui.selfPrint_button.clicked.connect(lambda :self.enable_Ui_selfPrint_widget())
        self.ui.examSearch_button.clicked.connect(lambda :self.enable_Ui_examSearch_widget())
        self.ui.classSchedule_button.clicked.connect(lambda :self.enable_Ui_classSchedule_widget())
        self.ui.appInfo_button.clicked.connect(lambda :self.enable_Ui_appInfo_widget())
        self.ui.robClasses_button.clicked.connect(lambda :self.enable_Ui_robClasses_widget())
    
    def setLoadingMessage(self,message:str,color:Qt.GlobalColor):
        self.ui_loading_widget.setMessageShow(message,color)

    def setLoadingProgress(self,value:int):
        self.ui_loading_widget.setProgress(value)

    def loadingShow(self):
        self.subWidget.setCurrentWidget(self.ui_loading_widget)
    
    def returnUi(self,ui:QWidget):
        self.subWidget.setCurrentWidget(ui)

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

    #侧边栏 关于软件查询被点击
    def enable_Ui_appInfo_widget(self):
        print("侧边栏关于软件按钮被点击\n")
        restoreAllToolButton(self)
        self.ui.appInfo_button.setEnabled(False)
        self.subWidget.setCurrentWidget(self.ui_appInfo_widget)

    #侧边栏 抢课按钮被点击
    def enable_Ui_robClasses_widget(self):
        print("侧边栏抢课按钮被点击\n")
        if logined:
            restoreAllToolButton(self)
            self.ui.robClasses_button.setEnabled(False)
            self.subWidget.setCurrentWidget(self.ui_robClasses_widget)
        else:
            self.loginExpired("你还没有登录哦~")
            return
        self.subWidget.setCurrentWidget(self.ui_robClasses_widget)


    def closeEvent(self, event):
        print("主界面关闭事件被触发,正在保存数据\n")
        with open(os.path.join(appDataDes,"loginOptions.fx"),"w",encoding="utf-8") as f:
            global loginOptionsData
            json.dump(loginOptionsData,f)

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
        self.loginThreadIsRunning = False
        self.getLoginBgThreadIsRunning = False
        print("ui_login_widget实例已创建\n")
        self.getLoginBg()
        
        self.ui_login.autoLogin.setEnabled(False)
        self.ui_login.used_accept.stateChanged.connect(lambda state: self.used_acceptChecked(state))
        self.ui_login.autoLogin.stateChanged.connect(lambda state: self.autoLoginChecked(state))

        if not appDataDes:
            print("APPDATA环境变量未设置,无法保存登录信息\n")
            self.setMessageShow("APPDATA环境变量未设置,无法保存登录信息",color=Qt.red)
        
        if not os.path.exists(appDataDes):
            os.makedirs(appDataDes)

        print("软件数据路径:" + appDataDes + "\n")
        global loginOptionsData
        try:
            loginOptionsDes = os.path.join(appDataDes,"loginOptions.fx")
            with open(loginOptionsDes,"r",encoding="utf-8") as f:
                loginOptionsData = json.load(f)
                print("登录选项数据:" + str(loginOptionsData) + "\n")
        except FileNotFoundError as e:
            print("暂无登录选项数据,使用默认值\n")
            loginOptionsData["autoLogin"] = False
            loginOptionsData["pwd"] = ""
            loginOptionsData["id"] = ""
        except Exception as e:
            print("读取登录选项数据异常:" + str(e) + "\n")
            self.setMessageShow("读取登录选项数据异常:" + str(e),color=Qt.red)
            loginOptionsData["autoLogin"] = False
            loginOptionsData["pwd"] = ""
            loginOptionsData["id"] = ""

        self.ui_login.autoLogin.setChecked(loginOptionsData["autoLogin"])
        self.ui_login.login_idInput.setText(loginOptionsData["id"])
        self.ui_login.login_pwdInput.setText(loginOptionsData["pwd"])

        if self.ui_login.autoLogin.isChecked():
            self.ui_login.used_accept.setChecked(True)
            time_sleep(0.5)
            self.on_login_button_clicked()
        
    def autoLoginChecked(self,state:bool):
        if not state:
            print("取消自动登录\n")
            loginOptionsData["autoLogin"] = False
            loginOptionsData["pwd"] = ""
            loginOptionsData["id"] = ""
        else:
            loginOptionsData["autoLogin"] = True
            print("开启自动登录\n")

    def used_acceptChecked(self,state:bool):
        if not state:
            self.ui_login.autoLogin.setChecked(False)
            self.ui_login.autoLogin.setEnabled(False)
        else:
            self.ui_login.autoLogin.setEnabled(True)

    def setMessageShow(self, message:str, color:Qt.GlobalColor = Qt.red):
        paletter = QPalette()
        paletter.setColor(QPalette.WindowText, color)
        self.ui_login.messageShow.setPalette(paletter)
        self.ui_login.messageShow.setText(message)
    
    def on_login_button_clicked(self):
        global userId, userpwd,semester,loginOptionsData
        print("登录按钮被点击\n")
        self.ui_login.used_accept.setEnabled(False)
        self.ui_login.login_button.setEnabled(False)
        semester = ""
        userId = self.ui_login.login_idInput.text()
        userpwd = self.ui_login.login_pwdInput.text()
        if self.ui_login.autoLogin.isChecked():
            loginOptionsData["id"] = userId
            loginOptionsData["pwd"] = userpwd
        print("登录信息:" + userId + " " + userpwd + "\n")
        if not userId or not userpwd:
            self.login_returnFunction(False,"请输入用户名和密码")
            return
        
        if not self.ui_login.used_accept.isChecked():
            self.login_returnFunction(False,"请阅读并同意用户协议")
            return

        self.setMessageShow("正在登录...",color=Qt.darkYellow)

        login(self, self.login_returnFunction)

    def login_returnFunction(self,state:bool,message:str):
        if state:
            self.setMessageShow(message,color=Qt.darkGreen)
            self.loginSuccess.emit(state,message)
        else:
            self.setMessageShow(message,color=Qt.red)
        self.ui_login.login_button.setEnabled(True)
        self.ui_login.used_accept.setEnabled(True)
        self.loginThreadIsRunning = False
    
    def getLoginBg(self):
        print("正在获取登录界面背景...\n")
        loginBgUrl = parse.urljoin(baseUrl, loginBgUrlSuf)
        try:
            if not self.getLoginBgThreadIsRunning:
                self.getLoginBgThread = GetRequestThread(url=loginBgUrl, timeout=5)
                self.getLoginBgThread.resultSignal.connect(self.fillLoginBg)
                threadPool.start(self.getLoginBgThread)
                self.getLoginBgThreadIsRunning = True
        except Exception as e:
            print("获取登录界面背景异常:" + str(e) + "\n")
            self.setMessageShow("获取登录界面背景异常:" + str(e),color=Qt.red)
    
    def fillLoginBg(self,state:bool = False,message:str = "",response:requests.Response = None):
        self.getLoginBgThreadIsRunning = False
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
        self.loginThreadIsRunning = False
        self.getUserInfoThreadIsRunning = False
        self.getuserAvatarThreadIsRunning = False
        self.getsemesterThreadIsRunning = False

    def loginExpired(self, state:bool = False,message:str = ""):
        if not state:
            self.loginExpiredSignal.emit(message)
        self.loginThreadIsRunning = False
        
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
            self.setMessageShow("正在获取当前学期...",color=Qt.darkYellow)
            if not self.getsemesterThreadIsRunning:
                self.getsemesterThread = GetRequestThread(parse.urljoin(baseUrl, semesterUrlSuf))
                self.getsemesterThread.resultSignal.connect(self.fillSemester)
                threadPool.start(self.getsemesterThread)
                self.getsemesterThreadIsRunning = True
        return

    def fillSemester(self,state:bool = False,message:str = "",response:requests.Response = None):
        self.getsemesterThreadIsRunning = False
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
        self.setMessageShow("当前学期:" + semester,color=Qt.darkGreen)
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
        self.setMessageShow("正在获取用户信息...",color=Qt.darkYellow)
        userInfoUrl = parse.urljoin(baseUrl, userInfoSuf)
        try:
            if not self.getUserInfoThreadIsRunning:
                self.getUserInfoThread = GetRequestThread(url=userInfoUrl, timeout=5)
                self.getUserInfoThread.resultSignal.connect(self.fillUserInfo)
                threadPool.start(self.getUserInfoThread)
                self.getUserInfoThreadIsRunning = True

        except Exception as e:
            self.setMessageShow("获取用户信息异常:" + str(e),color=Qt.red)
            print("获取用户信息异常:" + str(e) + "\n")
        
        #获取用户头像
        print("正在获取用户头像...\n")
        self.setMessageShow("正在获取用户头像...",color=Qt.darkYellow)
        userAvatarUrl = parse.urljoin(baseUrl, userImgUrlSuf)
        try:
            if not self.getuserAvatarThread:
                self.getuserAvatarThread = GetRequestThread(url=userAvatarUrl, timeout=5)
                self.getuserAvatarThread.resultSignal.connect(self.fillUserAvatar)
                threadPool.start(self.getuserAvatarThread)
                self.getuserAvatarThreadIsRunning = True
        except Exception as e:
            self.setMessageShow("获取用户头像异常:" + str(e),color=Qt.red)
            print("获取用户头像异常:" + str(e) + "\n")

    #回调:解析用户头像并填入界面
    def fillUserAvatar(self,state:bool = False,message:str = "",response:requests.Response = None):
        self.getuserAvatarThreadIsRunning = False
        if not state:
            self.setMessageShow(message,color=Qt.red)
            print(message + "\n")
            return
        global userAvatar
        userAvatar = response.content
        pixmap = QPixmap()
        pixmap.loadFromData(userAvatar)
        self.Ui_userInfo.userAvatar.setPixmap(pixmap)
        self.setMessageShow("用户头像获取成功!",color=Qt.darkGreen)
        print("用户头像获取成功!\n")

    #回调:解析用户信息并填入界面
    def fillUserInfo(self,state:bool = False,message:str = "",response:requests.Response = None):
        self.getUserInfoThreadIsRunning = False
        if not state:
            self.setMessageShow(message,color=Qt.red)
            print(message + "\n")
            return
        self.setMessageShow("填入用户信息中...",color=Qt.darkGreen)
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
            self.setMessageShow("用户信息获取成功!",color=Qt.darkGreen)
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
        self.getPrintListThreadingIsRunning = False
        self.downloadPrintFileIsRunning = False
    
    def getPrintList(self):
        printListUrl = parse.urljoin(baseUrl, printListSuf)
        if not self.getPrintListThreadingIsRunning:
            self.getPrintListThreading = GetRequestThread(printListUrl)
            self.getPrintListThreading.resultSignal.connect(self.fillPrintList)
            threadPool.start(self.getPrintListThreading)
            self.getPrintListThreadingIsRunning = True

    
    def fillPrintList(self,state:bool = False,message:str = "",response:requests.Response = None):
        self.getPrintListThreadingIsRunning = False
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
                btn.setStyleSheet("font-size:11pt;")
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
            if not self.downloadPrintFileIsRunning:
                self.downloadPrintFile = GetRequestThread(printUrl,timeout = 20)
                self.downloadPrintFile.resultSignal.connect(self.savePrintFile)
                threadPool.start(self.downloadPrintFile)
                self.downloadPrintFileIsRunning = True
            else:
                self.setMessageShow("已经有一个下载任务了，请稍后再试")
                return
            
            self.setMessageShow(f"请选择保存路径",color=Qt.darkYellow)
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
                self.setMessageShow("您取消了选择",color=Qt.darkYellow)
                return

            self.downloadPrintFile.start()
            self.setMessageShow(f"正在下载{ButtonName}的打印文件...",color=Qt.darkYellow)
            print(f"正在下载{ButtonName}的打印文件...\n")
            self.fileName = ButtonName + ".pdf"
        except Exception as e:
            self.setMessageShow(f"打开打印页面异常:" + str(e),color=Qt.red)
            print(f"打开打印页面异常:" + str(e) + "\n")
            raise

    def savePrintFile(self,state:bool = False,message:str = "",response:requests.Response = None):
        self.downloadPrintFileIsRunning = False
        if not state:
            self.setMessageShow(message,color=Qt.red)
            print(message + "\n")
            return
        
        if not response.headers.get("Content-Disposition",None):
            self.setMessageShow(f"下载{self.fileName}失败,你可能没有相关成绩!",color=Qt.red)
            print(f"下载{self.fileName}失败,你可能没有相关成绩!\n")
            return
        
        try:
            dest = self.destPath + "/" + self.fileName
            with open(dest, "wb") as f:
                f.write(response.content)
        except Exception as e:
            self.setMessageShow(f"保存打印文件异常:" + str(e),color=Qt.red)
            print(f"保存打印文件异常:" + str(e) + "\n")
            return
        self.setMessageShow(f"{dest} 保存成功!",color=Qt.darkGreen)
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
        self.getExamListThreading1IsRunning = False
        self.getExamListThreading2IsRunning = False
        self.DataModel1 = QStandardItemModel()
        self.ui_examSearch.examTable1.setModel(self.DataModel1)
        self.DataModel2 = QStandardItemModel()
        self.ui_examSearch.examTable2.setModel(self.DataModel2)

    def getExamList(self):
        self.DataModel1.setRowCount(0)
        self.DataModel2.setRowCount(0)
        if not self.getExamListThreading1IsRunning:
            self.getExamListThreading1 = PostRequestThread(parse.urljoin(baseUrl, examListSuf1),data={"xnxqid":semester})
            self.getExamListThreading1.resultSignal.connect(self.fillExamList1)
            threadPool.start(self.getExamListThreading1)
            self.getExamListThreading1IsRunning = True

        if not self.getExamListThreading2IsRunning:
            self.getExamListThreading2 = PostRequestThread(parse.urljoin(baseUrl, examListSuf2),data={"xnxqid":semester})
            self.getExamListThreading2.resultSignal.connect(self.fillExamList2)
            threadPool.start(self.getExamListThreading2)
            self.getExamListThreading2IsRunning = True
        
    def fillExamList1(self,state:bool = False,message:str = "",response:requests.Response = None):
        self.getExamListThreading1IsRunning = False
        try:
            if not state:
                self.setMessageShow1(message,color=Qt.red)
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
                self.setMessageShow1("暂无集中考试↑",color=Qt.darkGreen)
                return
            else:
                self.setMessageShow1("集中考试↑",color=Qt.darkYellow)

            for items in examList[1:]:
                self.DataModel1.appendRow([QStandardItem(" " * 5 + str(item.text.strip()) + " " * 5) for item in items.find_all("td")])
            self.ui_examSearch.examTable1.setModel(self.DataModel1)
            self.ui_examSearch.examTable1.resizeColumnsToContents()
            self.ui_examSearch.examTable1.resizeRowsToContents()
        except Exception as e:
            print("解析考试列表1异常:" + str(e) + "\n")
            self.setMessageShow1("解析考试列表异常1:" + str(e),color=Qt.red)
    
    def fillExamList2(self,state:bool = False,message:str = "",response:requests.Response = None):
        self.getExamListThreading2IsRunning = False
        try:
            if not state:
                self.setMessageShow2(message,color=Qt.red)
                print(message + "\n")
                return
            soup = BeautifulSoup(response.text, "lxml")
            examList = soup.find("table",class_ = "Nsb_r_list Nsb_table")
            if not examList:
                self.setMessageShow2("获取考试列表2失败",color=Qt.red)
                print("获取考试列表2失败\n")
                return
            else:
                self.setMessageShow2("分散考试↑",color=Qt.darkYellow)

            examList = examList.find_all("tr")
            self.colCnt = len(examList[0].find_all("th"))
            self.DataModel2.setColumnCount(self.colCnt)
            self.DataModel2.setHorizontalHeaderLabels([str(item.text.strip()) for item in examList[0].find_all("th")])

            if len(examList[1].find_all("td")) == 1:
                self.setMessageShow2("暂无分散考试↑",color=Qt.darkGreen)
                print("暂无分散考试\n")
                return

            for items in examList[1:]:
                self.DataModel2.appendRow([QStandardItem(" " * 5 + str(item.text.strip()) + " " * 5) for item in items.find_all("td")])
            self.ui_examSearch.examTable2.setModel(self.DataModel2)
            self.ui_examSearch.examTable2.resizeColumnsToContents()
            self.ui_examSearch.examTable2.resizeRowsToContents()
        except Exception as e:
            print("解析考试列表2异常:" + str(e) + "\n")
            self.setMessageShow2("解析考试列表异常2:" + str(e),color=Qt.red)
    

    def showEvent(self, event):
        super().showEvent(event)
        if semester == "":
            self.setMessageShow2("当前学期获取失败,请尝试重新登录",color=Qt.red)
            return
        self.getExamList()
        return
    
    def setMessageShow1(self, message:str, color:Qt.GlobalColor = Qt.red):
        paletter = QPalette()
        paletter.setColor(QPalette.WindowText, color)
        self.ui_examSearch.messageShow1.setPalette(paletter)
        self.ui_examSearch.messageShow1.setText(message)
    
    def setMessageShow2(self, message:str, color:Qt.GlobalColor = Qt.red):
        paletter = QPalette()
        paletter.setColor(QPalette.WindowText, color)
        self.ui_examSearch.messageShow2.setPalette(paletter)
        self.ui_examSearch.messageShow2.setText(message)

#课程表界面
class Ui_classSchedule_widget(QWidget):
    def __init__(self, parent:type = None):
        super().__init__(parent)
        self.ui_classSchedule = Ui_classSchedule()
        self.ui_classSchedule.setupUi(self)
        self.ui_classSchedule.dateEdit.setDate(QDate.currentDate())
        self.getClassScheduleThreading = None
        self.getClassScheduleThreadingIsRunning = False

        #绑定查询按钮
        self.ui_classSchedule.search.clicked.connect(self.getClassSchedule)
        #绑定tableview
        self.tableModel = QStandardItemModel()

        self.ui_classSchedule.nextWeek.clicked.connect(self.nextWeek)
        self.ui_classSchedule.lastWeek.clicked.connect(self.lastWeek)

    def getClassSchedule(self):
        selectDate = self.ui_classSchedule.dateEdit.date().toString("yyyy-MM-dd")
        if self.getClassScheduleThreadingIsRunning:
            self.setMessageShow("已经有一个查询任务了，请稍后再试",color=Qt.red)
            print("已经有一个查询任务了，请稍后再试\n")
            return
        self.getClassScheduleThreading = PostRequestThread(parse.urljoin(baseUrl, classScheduleUrlSuf),data = {"rq" : selectDate})
        self.getClassScheduleThreading.resultSignal.connect(self.fillClassSchedule)
        threadPool.start(self.getClassScheduleThreading)
        self.getClassScheduleThreadingIsRunning = True
        self.setMessageShow("正在查询课程表..." + selectDate,color=Qt.darkYellow)
        print("正在查询课程表...\n")
        
    def fillClassSchedule(self,state:bool = False,message:str = "",response:requests.Response = None):
        self.getClassScheduleThreadingIsRunning = False
        try:
            if not state:
                self.setMessageShow(message,color=Qt.red)
                print(message + "\n")
                return
            soup = BeautifulSoup(response.text.replace("\r","").replace("\n","").replace("\t","").replace("<br>","\n").replace("</br>","\n").replace("<br/>","\n"), "lxml")
            items = soup.find_all("tr")
            colCnt = len(items[0].find_all("th"))
            self.tableModel.setColumnCount(colCnt)
            self.tableModel.setRowCount(0)
            self.tableModel.setHorizontalHeaderLabels([str(item.text.strip()) for item in items[0].find_all("th")])

            curWeekContent = soup.find("script",type="text/javascript").text.split(";")
            for line in curWeekContent:
                if "main_text main_color" in line:
                    dirt = "$(\"#li_showWeek\").html(\"<span class=\\\"main_text main_color\\\">"
                    line = line.replace(dirt,"")
                    dirt = "\")"
                    line = line.replace(dirt,"")
                    dirt = "</span>"
                    line = line.replace(dirt,"")
                    self.ui_classSchedule.curWeekMessage.setText(line)
                    break

            if len(items) == 1:
                self.setMessageShow("暂无课程信息",color=Qt.darkGreen)
                print("暂无课程信息\n")
                return

            showDetail = self.ui_classSchedule.showDetail.isChecked()
        
            for item in items[1:]:
                if showDetail:
                    self.tableModel.appendRow([QStandardItem( str( td.text if td.find("p") == None else td.find("p").get("title","")).strip() ) for td in item.find_all("td")])
                else:
                    self.tableModel.appendRow([QStandardItem( str( td.text if td.find("p") == None else td.find("p").text).strip() ) for td in item.find_all("td")])
            self.ui_classSchedule.classScheduleTable.setModel(self.tableModel)
            self.ui_classSchedule.classScheduleTable.resizeColumnsToContents()
            self.ui_classSchedule.classScheduleTable.resizeRowsToContents()

            self.setMessageShow("解析课程表成功!",color=Qt.darkGreen)
            print("解析课程表成功!\n")
        except Exception as e:
            print("解析课程表异常:" + str(e) + "\n")
            self.setMessageShow("解析课程表异常:" + str(e),color=Qt.red)
    
    def setMessageShow(self, message:str, color:Qt.GlobalColor = Qt.red):
        paletter = QPalette()
        paletter.setColor(QPalette.WindowText, color)
        self.ui_classSchedule.messageShow.setPalette(paletter)
        self.ui_classSchedule.messageShow.setText(message)

    def nextWeek(self):
        curDate = self.ui_classSchedule.dateEdit.date()
        nextDate = curDate.addDays(7)
        self.ui_classSchedule.dateEdit.setDate(nextDate)
        self.getClassSchedule()
    
    def lastWeek(self):
        curDate = self.ui_classSchedule.dateEdit.date()
        lastDate = curDate.addDays(-7)
        self.ui_classSchedule.dateEdit.setDate(lastDate)
        self.getClassSchedule()

    def showEvent(self, event):
        super().showEvent(event)
        if self.ui_classSchedule.curWeekMessage.text() == "":
            self.getClassSchedule()
        return

#关于界面
class Ui_appInfo_widget(QWidget):
    def __init__(self, parent:type = None):
        super().__init__(parent)
        self.getAppInfoMessageThreadingIsRunning = False
        self.ui_appInfo = Ui_appInfo()
        self.ui_appInfo.setupUi(self)
        self.ui_appInfo.icon.setPixmap(QPixmap(":/icon/icon_256.svg"))
        self.getAppInfoMessageThreading = None
        self.getAppInfoMessage()

    def getAppInfoMessage(self):
        if self.getAppInfoMessageThreadingIsRunning:
            return
        self.getAppInfoMessageThreading = GetRequestThread(appInfoMessageUrl)
        self.getAppInfoMessageThreading.resultSignal.connect(self.fillAppInfoMessage)
        threadPool.start(self.getAppInfoMessageThreading)
        self.getAppInfoMessageThreadingIsRunning = True
    
    def fillAppInfoMessage(self,state:bool = False,message:str = "",response:requests.Response = None):
        self.getAppInfoMessageThreadingIsRunning = False
        try:
            if not state:
                self.setMessageShow(message,color=Qt.red)
                print(message + "\n")
                return
            print("正在填充appInfo\n")
            self.setMessageShow(response.text,color=Qt.darkGreen)
        except Exception as e:
            print("解析app信息异常:" + str(e) + "\n")
            self.setMessageShow("解析app信息异常:" + str(e),color=Qt.red)
    
    def setMessageShow(self, message:str, color:Qt.GlobalColor = Qt.red):
        paletter = QPalette()
        paletter.setColor(QPalette.Text, color)
        self.ui_appInfo.appInfoMessage.setPalette(paletter)
        self.ui_appInfo.appInfoMessage.setHtml(message)
        print("填充appInfo成功:" + message + "\n")

#加载界面
class Ui_loading_widget(QWidget):
    def __init__(self, parent:type = None):
        super().__init__(parent)
        self.ui_loading = Ui_loading()
        self.ui_loading.setupUi(self)
        # self.Player = QMovie(":/loading/loading2.gif")
        # self.Player.setCacheMode(QMovie.CacheAll)
        # self.ui_loading.loadingFrame.setMovie(self.Player)
        # self.Player.start()
    
    def setMessageShow(self, message:str, color:Qt.GlobalColor = Qt.red):
        paletter = QPalette()
        paletter.setColor(QPalette.WindowText, color)
        self.ui_loading.messageShow.setPalette(paletter)
        self.ui_loading.messageShow.setText(message)

    def setProgress(self, process:int):
        self.ui_loading.loadingProcess.setValue(process)

#抢课界面
class Ui_robClasses_widget(QWidget):
    showLoding = Signal()
    setLoadingProgress = Signal(int)
    setLoadingMessage = Signal(str,Qt.GlobalColor)
    returnUi = Signal(QWidget)

    def __init__(self, parent:type = None):
        super().__init__(parent)
        self.ui_robClass = Ui_robClasses()
        self.ui_robClass.setupUi(self)
        self.haveInit = 0
        self.initPregress = 0
        self.loadingMessage = ""
        self.loadingMessageColor = None
    
    def setMessageShow(self, message:str, color:Qt.GlobalColor = Qt.red):
        self.setLoadingMessage.emit(message,color)
    
    def showEvent(self, event):
        super().showEvent(event)
        if self.haveInit == 1:
            print("抢课模块未初始化完成")
            self.showLoding.emit()
            self.setLoadingProgress.emit(self.initPregress)
            self.setLoadingMessage.emit(self.loadingMessage,self.loadingMessageColor)
            return
        elif self.haveInit == 2:
            print("抢课模块初始化完成")
            return
        self.haveInit = 1
        print("正在初始化抢课模块")
        self.setLoadingProgress.emit(self.initPregress)
        self.showLoding.emit()

        self.setLoadingMessage.emit("正在连接服务器...",Qt.darkYellow)
        self.loadingMessage = "正在连接服务器..."
        self.loadingMessageColor = Qt.darkYellow
        self.connectRobClassesServerThread = connectRobClassesServer()
        self.connectRobClassesServerThread.resultSignal.connect(self.connectRobClassesServerResult)
        self.connectRobClassesServerThread.start()
    
    def connectRobClassesServerResult(self,state:bool,message:str):
        if not state:
            self.setLoadingMessage.emit(message,Qt.red)
            self.loadingMessage = message
            self.loadingMessageColor = Qt.red
            print(message + "\n")
            return
        print("连接服务器成功")
        self.loadingMessage = "连接服务器成功"
        self.loadingMessageColor = Qt.darkGreen
        self.setLoadingMessage.emit(self.loadingMessage,self.loadingMessageColor)
        print("收到服务器消息:" + message)


    def setUiClass(self, uiClass:type):
        self.uiClass = uiClass

#登录线程
class LoginThread(QRunnable): 
    global session, userId, userpwd
    def __init__(self):
        super().__init__()
        self.threadPoolSignals = threadPoolSignals()  # 定义一个信号，传递请求结果（成功与否和消息）
        self.result = self.threadPoolSignals.signal_bool_str  # 定义一个信号，传递请求结果（成功与否和消息）
    
    @Slot()
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
            #self.result.emit(False, "网络异常:" + str(e))
            self.result.emit(False, "网络异常:请检查网络连接或稍后再试")
            return False, "网络异常:请检查网络连接或稍后再试"
        
        #执行登录
        try:
            response = session.post(loginUrl, data=postData, timeout=5)
        except Exception as e:
            self.result.emit(False, "网络异常:请检查网络连接或稍后再试")
            return False, "网络异常:请检查网络连接或稍后再试"
        
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
            self.result.emit(False, "网络异常:请检查网络连接或稍后再试")
            return False, "网络异常:请检查网络连接或稍后再试"

#登录方法（在主线程调用，自动切换到登录线程执行，并通过回调函数返回结果）
def login(self,returnFunction:type = None):
    if not self.loginThreadIsRunning:
        self.loginThread = LoginThread()
        self.loginThread.result.connect(returnFunction)
        threadPool.start(self.loginThread)
        self.loginThreadIsRunning = True

#多线程get请求的通用方法（传入URL和回调函数，自动处理异常和结果回调）
class GetRequestThread(QRunnable):
    global session
    def __init__(self, url:str = "",params:dict = {},timeout:int = 5):
        super().__init__()
        self.url = url
        self.params = params
        self.timeout = timeout
        self.threadPoolSignals = threadPoolSignals()  # 定义一个信号，传递请求结果（成功与否和消息）
        self.resultSignal = self.threadPoolSignals.signal_int_str_resopnse  # 定义一个信号，传递请求结果（成功与否和消息）

    @Slot()
    def run(self):
        try:
            response = session.get(self.url, params=self.params, timeout=self.timeout)
            self.resultSignal.emit(1, "",response)
        except Exception as e:
            #self.resultSignal.emit(0, "网络异常:" + str(e),None)
            self.resultSignal.emit(0, "网络异常:请检查网络连接或稍后再试",None)

#多线程post请求的通用方法（传入URL、数据和回调函数，自动处理异常和结果回调）
class PostRequestThread(QRunnable):
    global session
    def __init__(self, url:str = "", data:dict = None,timeout:int = 5):
        super().__init__()
        self.url = url
        self.data = data
        self.timeout = timeout
        self.threadPoolSignals = threadPoolSignals()  # 定义一个信号，传递请求结果（成功与否和消息）
        self.resultSignal = self.threadPoolSignals.signal_int_str_resopnse  # 定义一个信号，传递请求结果（成功与否和消息）

    @Slot()
    def run(self):
        try:
            response = session.post(self.url, data=self.data, timeout=self.timeout)
            self.resultSignal.emit(1, "",response)
        except Exception as e:
            #self.resultSignal.emit(0, "网络异常:" + str(e),None)
            self.resultSignal.emit(0, "网络异常:请检查网络连接或稍后再试",None)

class connectRobClassesServer(QThread):
    resultSignal = Signal(bool, str)  # 定义一个信号，传递请求结果（成功与否和消息）
    def __init__(self, parent:type = None):
        super().__init__(parent)
    
    def run(self):
        global session, userId, userpwd
        while True:
            try:
                time_sleep(1)
                response = session.get("http://127.0.0.1:9999/robclasses/login", timeout=5)
                self.resultSignal.emit(1, response.text)
            except Exception as e:
                print("连接服务器异常:" + str(e))
                self.resultSignal.emit(0, "连接服务器异常:请检查网络连接,或者作者暂未开放服务")
                return

class threadPoolSignals(QObject):
    signal_bool_str = Signal(bool, str)
    signal_int_str_resopnse = Signal(int, str,requests.Response)

#恢复所有按钮为可点击状态
def restoreAllToolButton(mainWindow):
    for btnName in toolButtonNameList:
        mainWindow.ui.__getattribute__(btnName).setEnabled(True)

if __name__ == "__main__":
    widget = Main()
    widget.show()
    sys.exit(app.exec())