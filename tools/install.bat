set app=aeon3yw
set basedir="%APPDATA%\PyWriter"
if not exist %basedir% md %basedir%
set appdir="%APPDATA%\PyWriter\%app%"
if not exist %appdir% md %appdir%
copy %app%.pyw %appdir%

set cnfdir="%APPDATA%\PyWriter\%app%\config"
if not exist %cnfdir% md %cnfdir%

copy /Y sample\aeon3yw.ini %cnfdir%

rem set aeon3dir="%LOCALAPPDATA%\Scribble Code\Aeon Timeline 3\Templates"
rem if exist %aeon3dir% copy /Y sample\yWriter.xml %aeon3dir%

if exist %USERPROFILE%\Desktop\%app%.lnk goto :end

@echo off
cls
echo The %app% program is installed.
echo Now create a shortcut on your desktop. 
echo For this, hold down the Alt key on your keyboard and then drag and drop %app%.pyw to your desktop. 
@echo off
explorer "%APPDATA%\PyWriter\%app%\"
pause

:end
