; LinkShift Installer for Windows
; Build: ISCC setup.iss /DArch=x64
#define MyAppName "文件迁移工具"
#define MyAppShortName "LinkShift"
#define MyAppPublisher "yukitakasama"
#define MyAppURL "https://github.com/yukitakasama/LinkShift"
#define MyAppVersion "1.2"

#ifndef Arch
  #define Arch "x64"
#endif

#if Arch == "x64"
  #define MyArchSuffix "x64"
  #define MyOutputName "LinkShift-v1.2-Windows-x64-Setup"
  #define MyDefaultDir "C:\Program Files\LinkShift"
  #define MyExeSource "..\dist\文件迁移工具.exe"
#else
  #define MyArchSuffix "x86"
  #define MyOutputName "LinkShift-v1.2-Windows-x86-Setup"
  #define MyDefaultDir "C:\Program Files (x86)\LinkShift"
  #define MyExeSource "..\dist\文件迁移工具.exe"
#endif

[Setup]
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={#MyDefaultDir}
DefaultGroupName={#MyAppName}
OutputDir=..\out
OutputBaseFilename={#MyOutputName}
Compression=lzma2/ultra64
SolidCompression=yes
UninstallDisplayIcon={app}\文件迁移工具.exe
UninstallDisplayName={#MyAppName}
PrivilegesRequired=admin
AllowUNCPath=False
ArchitecturesInstallIn64BitMode={#Arch == "x64" ? "x64compatible" : ""}
SetupIconFile=..\app_icon.ico
DisableProgramGroupPage=no
ShowLanguageDialog=yes
LanguageDetectionMethod=uilanguage

[Languages]
Name: "en"; MessagesFile: "compiler:Default.isl"
Name: "chinesesimplified"; MessagesFile: "ChineseSimplified.isl"

[CustomMessages]
; English
en.AppName={#MyAppName}
en.AdditionalTasks=Additional tasks:
en.CreateDesktopIcon=Create a desktop shortcut
en.StartMenuEntry={#MyAppShortName}
; Chinese Simplified
chinesesimplified.AppName={#MyAppName}
chinesesimplified.AdditionalTasks=附加任务:
chinesesimplified.CreateDesktopIcon=创建桌面快捷方式
chinesesimplified.StartMenuEntry={#MyAppShortName}

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalTasks}"; Flags: unchecked

[Files]
Source: "{#MyExeSource}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{cm:StartMenuEntry}"; Filename: "{app}\文件迁移工具.exe"
Name: "{group}\{cm:UninstallProgram,{cm:AppName}}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{cm:StartMenuEntry}"; Filename: "{app}\文件迁移工具.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\文件迁移工具.exe"; Description: "{cm:LaunchProgram,{cm:AppName}}"; Flags: nowait postinstall skipifsilent

[UninstallRun]
