; Mau-Mau NSIS Installer Script
; Copyright (C) 2024  mau-mau contributors
; SPDX-License-Identifier: GPL-3.0-or-later
;
; Requires NSIS 3.x  (https://nsis.sourceforge.io/)
; Build command: makensis installer/mau-mau.nsi

!define APP_NAME    "Mau-Mau"
!define APP_VERSION "1.0.0"
!define APP_EXE     "mau-mau.exe"
!define PUBLISHER   "mau-mau contributors"
!define INSTALL_DIR "$PROGRAMFILES64\${APP_NAME}"
!define UNINSTALLER "uninstall.exe"

; Installer output
OutFile "mau-mau-setup.exe"

; Require elevation so we can write to Program Files
RequestExecutionLevel admin

; Modern UI
!include "MUI2.nsh"

Name "${APP_NAME} ${APP_VERSION}"
InstallDir "${INSTALL_DIR}"
InstallDirRegKey HKLM "Software\${APP_NAME}" "InstallDir"

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "..\LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "English"

; ----- Installer sections -----

Section "Mau-Mau (required)" SecMain
  SectionIn RO

  SetOutPath "${INSTALL_DIR}"
  File "..\dist\${APP_EXE}"

  ; Start Menu shortcut
  CreateDirectory "$SMPROGRAMS\${APP_NAME}"
  CreateShortcut  "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" \
                  "${INSTALL_DIR}\${APP_EXE}"
  CreateShortcut  "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk" \
                  "${INSTALL_DIR}\${UNINSTALLER}"

  ; Registry info for Add/Remove Programs
  WriteRegStr HKLM \
    "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
    "DisplayName"    "${APP_NAME} ${APP_VERSION}"
  WriteRegStr HKLM \
    "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
    "UninstallString" "${INSTALL_DIR}\${UNINSTALLER}"
  WriteRegStr HKLM \
    "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
    "Publisher"    "${PUBLISHER}"
  WriteRegStr HKLM \
    "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" \
    "DisplayVersion" "${APP_VERSION}"

  WriteRegStr HKLM "Software\${APP_NAME}" "InstallDir" "${INSTALL_DIR}"

  WriteUninstaller "${INSTALL_DIR}\${UNINSTALLER}"
SectionEnd

; ----- Uninstaller -----

Section "Uninstall"
  Delete "${INSTALL_DIR}\${APP_EXE}"
  Delete "${INSTALL_DIR}\${UNINSTALLER}"
  RMDir  "${INSTALL_DIR}"

  Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
  Delete "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk"
  RMDir  "$SMPROGRAMS\${APP_NAME}"

  DeleteRegKey HKLM \
    "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
  DeleteRegKey HKLM "Software\${APP_NAME}"
SectionEnd
