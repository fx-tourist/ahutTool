# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout

# 导入编译后的主UI和子UI类
from ui_py.ui_form import Ui_mian
from ui_py.ui_userInfo import Ui_userInfo
from ui_py.ui_login import Ui_login

class mian(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_mian()
        self.ui.setupUi(self)
        
        # 初始化子UI容器属性（避免后续判断报错）
        self.subWidge = None
        self.subWidge_ui = None

        # 调用通用挂载方法（传入userInfo的UI类）
        self.loadSubWidge(Ui_login)
        self.loadSubWidge(Ui_userInfo)

    # 通用子UI挂载方法（支持传入任意UI类）
    def loadSubWidge(self, Ui_class):
        # 第一步：先销毁已挂载的子UI（避免重复叠加）
        self.destroySubWidge()
        
        # 第二步：校验传入的UI类是否合法
        if not Ui_class:
            print("错误：传入的UI类为空")
            return
        
        # 第三步：创建子UI容器并加载UI
        self.subWidge = QWidget()
        self.subWidge_ui = Ui_class()
        self.subWidge_ui.setupUi(self.subWidge)

        # 第四步：挂载到subwidge（带完整容错）
        if hasattr(self.ui, "subWidge"):
            # 获取subwidge的布局，无布局则自动创建
            sub_layout = self.ui.subWidge.layout()
            if not sub_layout:
                sub_layout = QVBoxLayout(self.ui.subWidge)
                sub_layout.setContentsMargins(0, 0, 0, 0)
                print("提示：subWidge未设置布局，已自动创建QVBoxLayout")
            
            sub_layout.addWidget(self.subWidge)
            print(f"提示：{Ui_class.__name__} 子UI已成功挂载")
        else:
            print("错误：主UI中未找到subWidge控件，请检查objectName")

    # 通用子UI销毁方法
    def destroySubWidge(self):
        # 检查是否有已挂载的子UI
        if self.subWidge and hasattr(self.ui, "subWidge"):
            # 1. 从布局移除子UI容器
            sub_layout = self.ui.subWidge.layout()
            if sub_layout:
                sub_layout.removeWidget(self.subWidge)
            # 2. 销毁控件（Qt推荐的安全销毁方式）
            self.subWidge.deleteLater()
            # 3. 清空属性（避免空引用）
            self.subWidge = None
            self.subWidge_ui = None
            print("提示：已销毁当前挂载的子UI")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = mian()
    widget.show()
    sys.exit(app.exec())