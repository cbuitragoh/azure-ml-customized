@echo off
:: BatchGotAdmin
::-------------------------------------
REM  --> Check for permissions
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

REM --> If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    set params = %*:"="
    echo UAC.ShellExecute "cmd.exe", "/c %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"
::--------------------------------------

:: This script download data from kaggle datasets (with credentials) in Windows CMD
:: pre-installation of the Kaggle API from https://pypi.org/project/kaggle/

kaggle datasets download -d nelgiriyewithana/top-spotify-songs-2023 -p ./experimentation/data

# unzip in experimentation/data/

cd .\experimentation\data
tar -xf top-spotify-songs-2023.zip

# delete original .zip file
del "top-spotify-songs-2023.zip"

# Optional rename-file
ren spotify-2023.csv training.csv 