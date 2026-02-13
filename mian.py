# This Python file uses the following encoding: utf-8
import sys
import requests
from PySide6.QtWidgets import QApplication, QWidget, QPushButton,QStackedWidget,QSpacerItem,QFileDialog
from PySide6.QtGui import QPalette
from PySide6.QtCore import Qt, QThread, Signal
from urllib import parse
import base64,json,time
from bs4 import BeautifulSoup
from PySide6.QtGui import QPixmap
from os import system as CmdCommand
from pathlib import Path
# 导入编译后的主UI和子UI类
from ui_py.ui_form import Ui_mian
from ui_py.ui_userInfo import Ui_userInfo
from ui_py.ui_login import Ui_login
from ui_py.ui_selfPrint import Ui_selfPrint
#配置
baseUrl = "http://jwxt.ahut.edu.cn/jsxsd/"
loginSuf = "xk/LoginToXk"
userImgUrlSuf = "framework/student/images/zp.jpg"
cheakLoginStateUrlSuf = "framework/main_index_loadkb.jsp"
userInfoSuf = "framework/xsMain_new.jsp"
loginBgUrlSuf = "framework/student/images/xs_bg.jpg"
printListSuf = "view/cjgl/zzdy_list.jsp"
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
        self.subWidget.addWidget(self.ui_login_widget)
        self.subWidget.addWidget(self.ui_userInfo_widget)
        self.subWidget.addWidget(self.ui_selfPrint_widget)
        #连接登录成功信号
        self.ui_login_widget.loginSuccess.connect(lambda state,message:self.on_login_result(state,message))
        #登录失效信号
        self.ui_userInfo_widget.loginExpiredSignal.connect(lambda message:self.loginExpired(message))

        #绑定工具栏的按钮事件
        self.ui.userInfo_button.clicked.connect(lambda :self.enable_Ui_userInfo_widget())
        self.ui.selfPrint_button.clicked.connect(lambda :self.enable_Ui_selfPrint_widget())
    
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