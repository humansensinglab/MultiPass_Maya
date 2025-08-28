@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM =============================================================================
REM  Universal Maya Script Uninstaller (Documents/OneDrive aware)
REM  Usage:
REM    uninstall.bat [maya_version] [target_name]
REM
REM    - maya_version: e.g., 2025. If omitted, auto-detects highest under Documents\maya\20??
REM    - target_name : subfolder under scripts (default: MultiPass)
REM
REM  Removes: <Documents>\maya\<version>\scripts\<target_name>\
REM =============================================================================

REM ---- 1) Resolve Documents path (OneDrive-aware via registry)
for /f "usebackq delims=" %%D in (`
  powershell -NoProfile -Command ^
    "[Environment]::ExpandEnvironmentVariables((Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders').Personal)"
`) do set "DOCS_DIR=%%D"

if not exist "%DOCS_DIR%\" (
  if exist "%OneDrive%\Documents\" (
    set "DOCS_DIR=%OneDrive%\Documents"
  ) else (
    set "DOCS_DIR=%USERPROFILE%\Documents"
  )
)

REM ---- 2) Resolve Maya version
set "MAYA_VER=%~1"
if "%MAYA_VER%"=="" (
  set "MAYA_VER="
  for /f "delims=" %%V in ('dir /b /ad "%DOCS_DIR%\maya\20??" 2^>nul ^| sort') do set "MAYA_VER=%%~nxV"
  if "%MAYA_VER%"=="" set "MAYA_VER=2025"
)

REM ---- 3) Resolve target name
set "TARGET_NAME=%~2"
if "%TARGET_NAME%"=="" set "TARGET_NAME=MultiPass"

REM ---- 4) Compose target path
set "TARGET_SCRIPTS=%DOCS_DIR%\maya\%MAYA_VER%\scripts"
set "TARGET_DIR=%TARGET_SCRIPTS%\%TARGET_NAME%"

echo === Universal Maya Uninstaller ===
echo Documents:    "%DOCS_DIR%"
echo Maya version: %MAYA_VER%
echo Target:       "%TARGET_DIR%"
echo.

if not exist "%TARGET_DIR%\" (
  echo [INFO] Nothing to uninstall. Folder not found.
  pause
  exit /b 0
)

choice /C YN /M "Remove this folder and everything inside? (Y/N)"
if errorlevel 2 (
  echo Aborted.
  pause
  exit /b 0
)

echo Deleting...
rmdir /S /Q "%TARGET_DIR%"
echo.

if exist "%TARGET_DIR%\" (
  echo [ERROR] Could not delete the folder (permissions or in use?).
  echo Close Maya and try again.
  pause
  exit /b 1
) else (
  echo [OK] Removed: "%TARGET_DIR%"
  echo.
  pause
  exit /b 0
)
