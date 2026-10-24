; Instalador de YTMusic (Inno Setup 6). Se genera con crear_instalador.bat.
#define AppName "YTMusic"
#define AppVersion "1.0.0"

[Setup]
AppId={{8C6E2B1A-4F3D-4E8B-9A57-1D2C3B4A5E60}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher=Alexjmendez
AppPublisherURL=https://github.com/Alexjmendez/YTMusic
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
; Instalación por usuario: no pide permisos de administrador
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=dist
OutputBaseFilename=YTMusic-Setup-{#AppVersion}
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayIcon={app}\YTMusic.exe

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "dist\YTMusic\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\YTMusic.exe"
Name: "{group}\Desinstalar {#AppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\YTMusic.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\YTMusic.exe"; Description: "{cm:LaunchProgram,{#AppName}}"; Flags: nowait postinstall skipifsilent
