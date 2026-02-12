# This Python file uses the following encoding: utf-8
import sys
import requests
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout,QStackedWidget
from PySide6.QtGui import QPalette
from PySide6.QtCore import Qt, QThread, Signal
from urllib import parse
import base64,json,time
from bs4 import BeautifulSoup
from PySide6.QtGui import QPixmap
# 导入编译后的主UI和子UI类
from ui_py.ui_form import Ui_mian
from ui_py.ui_userInfo import Ui_userInfo
from ui_py.ui_login import Ui_login
from ui_py.ui_scoreSearch import Ui_scoreSearch
#配置
baseUrl = "http://jwxt.ahut.edu.cn/jsxsd/"
loginSuf = "xk/LoginToXk"
userImgUrlSuf = "framework/student/images/zp.jpg"
cheakLoginStateUrlSuf = "framework/main_index_loadkb.jsp"
userInfoSuf = "framework/xsMain_new.jsp"
loginBgUrlSuf = "framework/student/images/xs_bg.jpg"
session = requests.Session()
session.headers.update({"X-Requested-With" : "XMLHttpRequest"})
toolButtonNameList = ["userInfo_button",
                      "scoreSearch_button",
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
        self.ui_scoreSearch_widget = Ui_scoreSearch_widget()
        self.subWidget.addWidget(self.ui_login_widget)
        self.subWidget.addWidget(self.ui_userInfo_widget)
        self.subWidget.addWidget(self.ui_scoreSearch_widget)
        #连接登录成功信号
        self.ui_login_widget.loginSuccess.connect(lambda state,message:self.on_login_result(state,message))
        #登录失效信号
        self.ui_userInfo_widget.loginExpiredSignal.connect(lambda message:self.loginExpired(message))

        #绑定工具栏的按钮事件
        self.ui.userInfo_button.clicked.connect(lambda :self.enable_Ui_userInfo_widget())
        self.ui.scoreSearch_button.clicked.connect(lambda :self.enable_Ui_scoreSearch_widget())
    
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

    #侧边栏 成绩查询被点击
    def enable_Ui_scoreSearch_widget(self):
        print("侧边栏成绩查询按钮被点击\n")
        restoreAllToolButton(self)
        self.ui.scoreSearch_button.setEnabled(False)
        self.subWidget.setCurrentWidget(self.ui_scoreSearch_widget)

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
        global userId, userpwd
        print("登录按钮被点击\n")
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
        return

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

#成绩查询子界面
class Ui_scoreSearch_widget(QWidget):
    def __init__(self, parent:type = None):
        super().__init__(parent)
        self.ui_scoreSearch = Ui_scoreSearch()
        self.ui_scoreSearch.setupUi(self)

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