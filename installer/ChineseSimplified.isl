; *** Inno Setup version 6.x 简体中文翻译 ***
; Simplified Chinese translation for Inno Setup 6.x

[LangOptions]
LanguageName=Chinese Simplified
LanguageID=$0804
LanguageCodePage=936
DialogFontName=Microsoft YaHei
WelcomeFontName=Microsoft YaHei
TitleFontName=Microsoft YaHei

[Messages]

; *** Application titles
SetupAppTitle=安装
SetupWindowTitle=%1 安装
UninstallAppTitle=卸载
UninstallAppFullTitle=%1 卸载

; *** Misc. common
InformationTitle=信息
ConfirmTitle=确认
ErrorTitle=错误

; *** SetupLdr messages
SetupLdrStartupMessage=即将安装 %1，是否继续？
LdrCannotCreateTemp=无法创建临时文件。安装程序即将中止。
LdrCannotExecTemp=无法执行临时文件夹中的文件。安装程序即将中止。

; *** Startup error messages
LastErrorMessage=%1.%n%n错误 %2: %3
SetupFileMissing=找不到文件 %1。请解决此问题或获取新的安装程序。
SetupFileCorrupt=安装文件已损坏。请获取新的安装程序。
SetupFileCorruptOrWrongVer=安装文件已损坏或与此版本的安装程序不兼容。请解决此问题或获取新的安装程序。
InvalidParameter=命令行传入了无效参数:%n%n%1
SetupAlreadyRunning=安装程序已在运行中。
WindowsVersionNotSupported=此程序不支持您当前使用的 Windows 版本。
WindowsServicePackRequired=此程序需要 %1 Service Pack %2 或更高版本。
NotOnThisPlatform=此程序无法在 %1 上运行。
OnlyOnThisPlatform=此程序需要 %1。
OnlyOnTheseArchitectures=此程序只能安装在%n%n%1 处理器上的 Windows。
WinVersionTooLowError=此程序需要 %1 %2 或更高版本。
WinVersionTooHighError=此程序不支持 %1 %2 或更高版本。
AdminPrivilegesRequired=安装此程序需要管理员权限。
PowerUserPrivilegesRequired=安装此程序需要管理员或高级用户权限。
SetupAppRunningError=安装程序检测到 %1 正在运行。%n%n请关闭所有打开的应用程序，然后单击"确定"继续。单击"取消"退出安装程序。
UninstallAppRunningError=卸载程序检测到 %1 正在运行。%n%n请关闭所有打开的应用程序，然后单击"确定"继续。单击"取消"退出卸载程序。

; *** Startup questions
PrivilegesRequiredOverrideTitle=选择安装模式
PrivilegesRequiredOverrideInstruction=请选择安装模式
PrivilegesRequiredOverrideText1=%1 可以为所有用户安装（需要管理员权限），或仅为当前用户安装。
PrivilegesRequiredOverrideText2=%1 可以为当前用户安装，或为所有用户安装（需要管理员权限）。
PrivilegesRequiredOverrideAllUsers=为所有用户安装(&A)
PrivilegesRequiredOverrideAllUsersRecommended=为所有用户安装(&A)（推荐）
PrivilegesRequiredOverrideCurrentUser=为当前用户安装(&M)
PrivilegesRequiredOverrideCurrentUserRecommended=为当前用户安装(&M)（推荐）

; *** Misc. errors
ErrorCreatingDir=创建目录 %1 时出错。
ErrorTooManyFilesInDir=在目录 %1 中创建文件时出错。文件过多。

; *** Setup common messages
ExitSetupTitle=退出安装程序
ExitSetupMessage=安装尚未完成。如果现在退出，程序将不会被安装。%n%n以后可以再次运行安装程序来完成安装。%n%n是否退出安装程序？
AboutSetupMenuItem=关于安装程序(&A)
AboutSetupTitle=关于安装程序
AboutSetupMessage=%1 %2%n%3%n%n%1 主页:%n%4
AboutSetupNote=
TranslatorNote=简体中文翻译

; *** Buttons
ButtonBack=< 上一步(&B)
ButtonNext=下一步(&N) >
ButtonInstall=安装(&I)
ButtonOK=确定
ButtonCancel=取消
ButtonYes=是(&Y)
ButtonYesToAll=全部是(&A)
ButtonNo=否(&N)
ButtonNoToAll=全部否(&O)
ButtonFinish=完成(&F)
ButtonBrowse=浏览(&B)...
ButtonWizardBrowse=浏览(&R)...
ButtonNewFolder=新建文件夹(&M)

; *** "Select Language" dialog messages
SelectLanguageTitle=选择安装语言
SelectLanguageLabel=请选择安装过程中使用的语言。

; *** Common wizard text
ClickNext=单击"下一步"继续，或单击"取消"退出安装程序。
BeveledLabel=
BrowseDialogTitle=浏览文件夹
BrowseDialogLabel=请从列表中选择一个文件夹，然后单击"确定"。
NewFolderName=新建文件夹

; *** "Welcome" wizard page
WelcomeLabel1=欢迎使用 [name] 安装向导
WelcomeLabel2=此程序将在您的计算机上安装 [name/ver]。%n%n建议您在继续之前关闭所有其他应用程序。

; *** "Password" wizard page
WizardPassword=密码
PasswordLabel1=此安装程序受密码保护。
PasswordLabel3=请输入密码，然后单击"下一步"。密码区分大小写。
PasswordEditLabel=密码(&P):
IncorrectPassword=输入的密码不正确。请重新输入。

; *** "License Agreement" wizard page
WizardLicense=许可协议
LicenseLabel=请阅读以下重要信息，然后再继续。
LicenseLabel3=请阅读以下许可协议。要继续安装，您必须接受协议条款。
LicenseAccepted=我接受协议(&A)
LicenseNotAccepted=我不接受(&D)

; *** "Information" wizard pages
WizardInfoBefore=信息
InfoBeforeLabel=请阅读以下重要信息，然后再继续。
InfoBeforeClickLabel=单击"下一步"继续安装。
WizardInfoAfter=信息
InfoAfterLabel=请阅读以下重要信息，然后再继续。
InfoAfterClickLabel=单击"下一步"继续安装。

; *** "User Information" wizard page
WizardUserInfo=用户信息
UserInfoDesc=请输入您的用户信息。
UserInfoName=用户名(&U):
UserInfoOrg=组织(&O):
UserInfoSerial=序列号(&S):
UserInfoNameRequired=请输入用户名。

; *** "Select Destination Location" wizard page
WizardSelectDir=选择目标位置
SelectDirDesc=选择 [name] 的安装目录。
SelectDirLabel3=请指定 [name] 的安装目录，然后单击"下一步"。
SelectDirBrowseLabel=要继续，请单击"下一步"。如果要选择不同的文件夹，请单击"浏览"。
DiskSpaceGBLabel=此程序至少需要 [gb] GB 的磁盘空间。
DiskSpaceMBLabel=此程序至少需要 [mb] MB 的磁盘空间。
CannotInstallToNetworkDrive=无法安装到网络驱动器。
CannotInstallToUNCPath=无法安装到 UNC 路径。
InvalidPath=请输入完整的路径，包括驱动器号。%n%n例如: C:\APP%n%n或输入 UNC 路径。%n%n例如: \\server\share
InvalidDrive=指定的驱动器或 UNC 路径不存在或无法访问。请指定其他路径。
DiskSpaceWarningTitle=磁盘空间不足
DiskSpaceWarning=安装至少需要 %1 KB 磁盘空间，但所选驱动器仅有 %2 KB 可用空间。%n%n是否继续？
DirNameTooLong=驱动器名称或路径过长。
InvalidDirName=文件夹名称无效。
BadDirName32=文件夹名称中不能包含以下字符:%n%n%1
DirExistsTitle=文件夹已存在
DirExists=文件夹%n%n%1%n%n已存在。是否仍安装到此文件夹？
DirDoesntExistTitle=文件夹不存在
DirDoesntExist=文件夹%n%n%1%n%n不存在。是否创建新文件夹？

; *** "Select Components" wizard page
WizardSelectComponents=选择组件
SelectComponentsDesc=请选择要安装的组件。
SelectComponentsLabel2=请选择要安装的组件。取消选中不需要的组件。单击"下一步"继续。
FullInstallation=完整安装
CompactInstallation=紧凑安装
CustomInstallation=自定义安装
NoUninstallWarningTitle=现有组件
NoUninstallWarning=安装程序检测到以下组件已安装:%n%n%1%n%n取消选中这些组件不会卸载它们。%n%n是否继续？
ComponentSize1=%1 KB
ComponentSize2=%1 MB
ComponentsDiskSpaceGBLabel=当前选择至少需要 [gb] GB 磁盘空间。
ComponentsDiskSpaceMBLabel=当前选择至少需要 [mb] MB 磁盘空间。

; *** "Select Additional Tasks" wizard page
WizardSelectTasks=选择附加任务
SelectTasksDesc=请选择要执行的附加任务。
SelectTasksLabel2=请选择安装 [name] 时要执行的附加任务，然后单击"下一步"。

; *** "Select Start Menu Folder" wizard page
WizardSelectProgramGroup=选择开始菜单文件夹
SelectStartMenuFolderDesc=请选择程序快捷方式的创建位置。
SelectStartMenuFolderLabel3=安装程序将在以下开始菜单文件夹中创建程序快捷方式。
SelectStartMenuFolderBrowseLabel=要继续，请单击"下一步"。如果要选择不同的文件夹，请单击"浏览"。
MustEnterGroupName=请指定文件夹名称。
GroupNameTooLong=文件夹名称或路径过长。
InvalidGroupName=文件夹名称无效。
BadGroupName=文件夹名称中不能包含以下字符:%n%n%1
NoProgramGroupCheck2=不创建开始菜单文件夹(&D)

; *** "Ready to Install" wizard page
WizardReady=准备安装
ReadyLabel1=已准备好开始安装 [name]。
ReadyLabel2a=要继续安装，请单击"安装"。要查看或更改设置，请单击"上一步"。
ReadyLabel2b=要继续安装，请单击"安装"。
ReadyMemoUserInfo=用户信息:
ReadyMemoDir=安装目录:
ReadyMemoType=安装类型:
ReadyMemoComponents=所选组件:
ReadyMemoGroup=开始菜单文件夹:
ReadyMemoTasks=附加任务:

; *** TDownloadWizardPage wizard page and DownloadTemporaryFile
DownloadingLabel2=正在下载文件...
ButtonStopDownload=停止下载(&S)
StopDownload=确认停止下载？
ErrorDownloadAborted=下载已中止
ErrorDownloadFailed=下载失败: %1 %2
ErrorDownloadSizeFailed=获取大小失败: %1 %2
ErrorProgress=无效进度: %1 / %2
ErrorFileSize=无效文件大小: 预期 %1，实际 %2

; *** TExtractionWizardPage wizard page and ExtractArchive
ExtractingLabel=正在解压文件...
ButtonStopExtraction=停止解压(&S)
StopExtraction=确认停止解压？
ErrorExtractionAborted=解压已中止
ErrorExtractionFailed=解压失败: %1

; *** Archive extraction failure details
ArchiveIncorrectPassword=密码不正确
ArchiveIsCorrupted=压缩文件已损坏
ArchiveUnsupportedFormat=不支持的压缩格式

; *** "Preparing to Install" wizard page
WizardPreparing=准备安装
PreparingDesc=正在准备在您的计算机上安装 [name]。
PreviousInstallNotCompleted=上次的程序安装或删除未完成。需要重新启动计算机才能完成。%n%n重新启动后，请再次运行安装程序以完成 [name] 的安装。
CannotContinue=无法继续安装。请单击"取消"退出安装程序。
ApplicationsFound=以下应用程序正在使用安装程序需要更新的文件。建议让安装程序自动关闭这些应用程序。
ApplicationsFound2=以下应用程序正在使用安装程序需要更新的文件。建议让安装程序自动关闭这些应用程序。安装完成后，安装程序将尝试重新启动这些应用程序。
CloseApplications=自动关闭应用程序(&A)
DontCloseApplications=不关闭应用程序(&D)
ErrorCloseApplications=安装程序无法自动关闭所有应用程序。建议在继续之前，关闭所有正在使用需要更新文件的应用程序。
PrepareToInstallNeedsRestart=安装程序需要重新启动计算机。重新启动后，请再次运行安装程序以完成 [name] 的安装。%n%n是否立即重新启动？

; *** "Installing" wizard page
WizardInstalling=正在安装
InstallingLabel=正在将 [name] 安装到您的计算机上，请稍候...

; *** "Setup Completed" wizard page
FinishedHeadingLabel=完成 [name] 安装向导
FinishedLabelNoIcons=[name] 已安装在您的计算机上。
FinishedLabel=[name] 已安装在您的计算机上。要运行该程序，请选择安装的快捷方式。
ClickFinish=单击"完成"退出安装程序。
FinishedRestartLabel=要完成 [name] 的安装，必须重新启动计算机。是否立即重新启动？
FinishedRestartMessage=要完成 [name] 的安装，必须重新启动计算机。%n%n是否立即重新启动？
ShowReadmeCheck=显示自述文件(&R)
YesRadio=是，立即重新启动(&Y)
NoRadio=否，稍后手动重启(&N)
RunEntryExec=运行 %1
RunEntryShellExec=查看 %1

; *** "Setup Needs the Next Disk" stuff
ChangeDiskTitle=插入磁盘
SelectDiskLabel2=请插入磁盘 %1，然后单击"确定"。%n%n如果此磁盘上的文件不在下方显示的文件夹中，请输入正确的路径或单击"浏览"。
PathLabel=路径(&P):
FileNotInDir2=在 %2 中找不到文件 %1。请插入正确的磁盘，或指定其他文件夹。
SelectDirectoryLabel=请指定下一张磁盘所在的位置。

; *** Installation phase messages
SetupAborted=安装未完成。%n%n请解决问题后重新运行安装程序。
AbortRetryIgnoreSelectAction=请选择操作
AbortRetryIgnoreRetry=重试(&R)
AbortRetryIgnoreIgnore=忽略错误并继续(&I)
AbortRetryIgnoreCancel=取消安装
RetryCancelSelectAction=请选择操作
RetryCancelRetry=重试(&R)
RetryCancelCancel=取消

; *** Installation status messages
StatusClosingApplications=正在关闭应用程序...
StatusCreateDirs=正在创建目录...
StatusExtractFiles=正在解压文件...
StatusDownloadFiles=正在下载文件...
StatusCreateIcons=正在创建快捷方式...
StatusCreateIniEntries=正在设置 INI 文件...
StatusCreateRegistryEntries=正在设置注册表...
StatusRegisterFiles=正在注册文件...
StatusSavingUninstall=正在保存卸载信息...
StatusRunProgram=正在完成安装...
StatusRestartingApplications=正在重新启动应用程序...
StatusRollback=正在回滚更改...

; *** Misc. errors
ErrorInternal2=内部错误: %1
ErrorFunctionFailedNoCode=%1 错误
ErrorFunctionFailed=%1 错误: 代码 %2
ErrorFunctionFailedWithMessage=%1 错误: 代码 %2.%n%3
ErrorExecutingProgram=执行文件时出错:%n%1

; *** Registry errors
ErrorRegOpenKey=打开注册表项错误:%n%1\%2
ErrorRegCreateKey=创建注册表项错误:%n%1\%2
ErrorRegWriteKey=写入注册表项错误:%n%1\%2

; *** INI errors
ErrorIniEntry=INI 文件条目错误: 文件 %1

; *** File copying errors
FileAbortRetryIgnoreSkipNotRecommended=跳过此文件(&S)（不推荐）
FileAbortRetryIgnoreIgnoreNotRecommended=忽略错误并继续(&I)（不推荐）
SourceIsCorrupted=源文件已损坏。
SourceDoesntExist=源文件 %1 不存在。
SourceIsEncrypted=无法复制加密的文件。
SourceIsDirectory=无法将目录复制到文件。
DestIsDirectory=无法将文件复制到目录。
SourceIsInUse=正在被其他进程使用。请关闭所有其他应用程序，然后单击"重试"。
ErrorReadingSource=读取源文件时出错。
ErrorReadingSourceOld=读取要替换的文件时出错。
ErrorReadingDest=读取目标文件时出错。
ErrorCopying=复制文件时出错。
ErrorReplacingExistingFile=替换现有文件时出错。
ErrorRemovingExistingFile=删除现有文件时出错。
ErrorRestartingWindows=重新启动 Windows 时出错。
ErrorCreatingTempFile=创建临时文件时出错。
ErrorExecutingTempFile=执行临时文件时出错。
ErrorExecutingFile=执行文件 %1 时出错。

; *** File existing attributes
FileExistingTitle=文件已存在
FileExisting=目标文件已存在:%n%n%1%n%n请选择操作:
FileExistingSizeAndDate=大小/日期
FileExistingUnknown=未知
FileExistingModerAnswered=覆盖(&O)
FileExistingOverwrite=覆盖(&O)
FileExistingOverwriteNewer=覆盖(&O) (较新)
FileExistingNotModifed=不覆盖(&N)
FileExistingOverwriteOlder=覆盖(&O) (较旧)
FileExistingAppend=追加(&A)
FileExistingAppendAll=全部追加(&L)
FileExistingOverwriteAll=全部覆盖(&W)
FileExistingOverwriteNewerAll=全部覆盖(&W) (较新)
FileExistingNotModifedAll=全部不覆盖(&I)
FileExistingOverwriteOlderAll=全部覆盖(&W) (较旧)
FileExistingKeepAll=全部保留(&K)
FileExistingKeep=保留(&K)
FileExistingDelete=删除(&D)
FileExistingDeleteAll=全部删除(&D)
FileExistingMove=移动(&M)
FileExistingMoveAll=全部移动(&M)
FileExistingReadOnly=只读
FileExistingReadOnlyOverwrite=覆盖只读文件(&O)
FileExistingReadOnlyOverwriteAll=全部覆盖只读文件(&W)
FileExistingReadOnlySkip=跳过只读文件(&S)
FileExistingReadOnlySkipAll=全部跳过只读文件(&I)

; *** File overwrite warning
ErrorOverwritingExistingFile=覆盖现有文件时出错。请检查文件权限。

; *** Uninstall
UninstallStatusLabel=正在从您的计算机上删除 %1，请稍候...
UninstallStatusLabel2=正在扫描...
UninstallTotal=正在删除文件...
UninstallTotal2=%1 中的 %2 已完成
UninstallNotFound=未找到卸载日志文件。无法卸载。
UninstallOpenError=打开卸载日志文件时出错。无法卸载。
UninstallRunning=卸载程序正在运行...
UninstallOnlySupported=此版本仅支持卸载。
UninstallUnknownEntry=卸载日志中存在未知条目。
ConfirmUninstall=确实要完全删除 %1 及其所有组件吗？
ProgramManagerItem=开始菜单
TaskGroupItem=开始菜单快捷方式
TaskDesktopIcon=桌面快捷方式
TaskQuicklaunchIcon=快速启动栏快捷方式
UninstallTaskRunning=检测到 %1 正在运行。建议在卸载前关闭它。%n%n是否自动关闭并继续？
UninstallTaskRunningDontClose=正在运行 %1。请在继续之前关闭它。

; *** Uninstaller messages in [LangOptions], [Messages]
UninstallAppRunningError=卸载程序检测到 %1 正在运行。%n%n请关闭所有打开的应用程序，然后单击"确定"继续。单击"取消"退出卸载程序。
UninstallAppTitle=卸载
UninstallAppFullTitle=%1 卸载

; *** Common items
ProgramGroupEntry=文件迁移工具
ProgramGroupUninstallEntry=卸载 文件迁移工具
DesktopIconEntry=文件迁移工具
