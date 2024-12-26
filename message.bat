@echo off &chcp 1251 >nul

echo WScript.Quit(MsgBox(WScript.Arguments(1) ^& Chr(13) ^& WScript.Arguments(2) ^& Chr(13) ^& WScript.Arguments(3), vbExclamation+vbSystemModal+vbMsgBoxSetForeground+vbDefaultButton2,WScript.Arguments(0)))>"%temp%\MsgBox.vbs"
WScript "%temp%\MsgBox.vbs" "ÂÍÈÌÀÍÈÅ!" "ÄÎÑÒÈÃÍÓÒÎ ÍÓÆÍÎÅ ÊÎËÈ×ÅÑÒÂÎ!" "" "=============================================="

del /q "%temp%\MsgBox.vbs" 
::pause>nul