pyinstaller "main.py" -F --distpath .\  --clean ^
--exclude-module unittest --exclude-module matplotlib ^
--hidden-import=tkinter --hidden-import=tkinter.ttk ^
-i ".\favicon.ico" ^
--noconfirm

pause
