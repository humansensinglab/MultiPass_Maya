@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM =============================================================================
REM  Universal Maya Script Installer (Documents/OneDrive aware)
REM  Usage:
REM    installer.bat [source_folder] [maya_version] [target_name]
REM
REM    - source_folder: path to your tool folder (e.g., ...\maya_renderer or ...\MultiPass)
REM                     If omitted, tries ".\maya_renderer" then "." (the .bat's folder).
REM    - maya_version:  e.g., 2025. If omitted, auto-detects highest version under Documents\maya\20??
REM    - target_name:   subfolder under scripts (default: MultiPass)
REM
REM  Installs to:  <Documents>\maya\<version>\scripts\<target_name>\
REM =============================================================================

set "SCRIPT_DIR=%~dp0"

REM ---- 1) Resolve source folder ------------------------------------------------
if "%~1"=="" (
  if exist "%SCRIPT_DIR%maya_renderer\" (
    set "SRC=%SCRIPT_DIR%maya_renderer"
  ) else (
    set "SRC=%SCRIPT_DIR%"
  )
) else (
  set "SRC=%~1"
)

REM If user passed a repo root that *contains* maya_renderer, normalize it
if exist "%SRC%\maya_renderer\" set "SRC=%SRC%\maya_renderer"

if not exist "%SRC%\" (
  echo [ERROR] Source folder not found:
  echo         "%SRC%"
  echo Supply a valid source folder or put ^maya_renderer^ next to this .bat.
  pause
  exit /b 1
)

REM ---- 2) Resolve Documents path (OneDrive-aware via registry) ----------------
for /f "usebackq delims=" %%D in (`
  powershell -NoProfile -Command ^
    "[Environment]::ExpandEnvironmentVariables((Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders').Personal)"
`) do set "DOCS_DIR=%%D"

if not exist "%DOCS_DIR%\" (
  REM Fallbacks, just in case
  if exist "%OneDrive%\Documents\" (
    set "DOCS_DIR=%OneDrive%\Documents"
  ) else (
    set "DOCS_DIR=%USERPROFILE%\Documents"
  )
)

REM ---- 3) Resolve Maya version -------------------------------------------------
set "MAYA_VER=%~2"
if "%MAYA_VER%"=="" (
  set "MAYA_VER="
  for /f "delims=" %%V in ('dir /b /ad "%DOCS_DIR%\maya\20??" 2^>nul ^| sort') do set "MAYA_VER=%%~nxV"
  if "%MAYA_VER%"=="" set "MAYA_VER=2025"
)

REM ---- 4) Resolve target name --------------------------------------------------
set "TARGET_NAME=%~3"
if "%TARGET_NAME%"=="" set "TARGET_NAME=MultiPass"

REM ---- 5) Compose targets ------------------------------------------------------
set "TARGET_SCRIPTS=%DOCS_DIR%\maya\%MAYA_VER%\scripts"
set "TARGET_DIR=%TARGET_SCRIPTS%\%TARGET_NAME%"

echo === Universal Maya Installer ===
echo Source:       "%SRC%"
echo Documents:    "%DOCS_DIR%"
echo Maya version: %MAYA_VER%
echo Target:       "%TARGET_DIR%"
echo.

REM ---- 6) Ensure target base exists -------------------------------------------
if not exist "%TARGET_SCRIPTS%\" (
  echo Creating: "%TARGET_SCRIPTS%"
  mkdir "%TARGET_SCRIPTS%" >nul 2>&1
)

REM ---- 7) Clean + mirror copy --------------------------------------------------
if exist "%TARGET_DIR%\" (
  echo Removing existing target...
  rmdir /S /Q "%TARGET_DIR%"
)
echo Creating target...
mkdir "%TARGET_DIR%" >nul 2>&1

echo Copying files (mirror)...
robocopy "%SRC%" "%TARGET_DIR%" /MIR /R:1 /W:1
set "RC=%ERRORLEVEL%"
echo Robocopy exit code: %RC%
echo.

if %RC% GEQ 8 (
  echo [ERROR] Copy failed (robocopy code %RC%). Aborting.
  pause
  exit /b 1
)

REM ---- 8) Verify and list ------------------------------------------------------
if exist "%TARGET_DIR%\" (
  echo [OK] Installed to:
  echo      "%TARGET_DIR%"
  echo.
  dir "%TARGET_DIR%" /B /S
) else (
  echo [ERROR] Target directory was not created.
  pause
  exit /b 1
)

echo.
echo Done. Launch Maya %MAYA_VER%.
echo.
pause
exit /b 0
