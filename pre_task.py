# 预处理脚本：将.ui文件转换为.py文件

import os

path_src = "./ui_src/"
path_des = "./ui_py/"

for file in os.listdir(path_src):
    if file.endswith(".ui"):
        file_name = os.path.splitext(file)[0]
        src_file = os.path.join(path_src, file)
        des_file = os.path.join(path_des, f"ui_{file_name}.py")
        command = f"pyside6-uic {src_file} -o {des_file}"
        os.system(command)

path_src = "./img_src/"
path_des = "./img_py/"
for file in os.listdir(path_src):
    if file.endswith(".qrc"):
        file_name = os.path.splitext(file)[0]
        src_file = os.path.join(path_src, file)
        des_file = os.path.join(path_des, f"img_{file_name}.py")
        command = f"pyside6-rcc {src_file} -o {des_file}"
        os.system(command)

os.system("taskkill /im WindowsTerminal.exe /f")