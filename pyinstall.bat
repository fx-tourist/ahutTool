pyinstaller "main.py" -F --noconsole --name "Ahut Tool 2.1" --distpath .\  --clean ^
--exclude-module unittest --exclude-module matplotlib ^
-i ".\img_src\icon_256.png" ^
--noconfirm

pause