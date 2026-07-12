param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("x64", "x86")]
    [string]$Arch,

    [Parameter(Mandatory=$false)]
    [string]$Version = "v1.2"
)

$ErrorActionPreference = "Stop"

if ($Arch -eq "x64") {
    $py = "C:\Users\yuki\AppData\Local\Python\pythoncore-3.14-64\python.exe"
    $suffix = "x64"
} else {
    $py = "C:\Users\yuki\AppData\Local\Programs\Python\Python312-32\python.exe"
    $suffix = "x86"
}

$zipName = "LinkShift-$Version-Windows-$suffix.zip"
$setupName = "LinkShift-$Version-Windows-$suffix-Setup.exe"
$iscc = "C:\Users\yuki\AppData\Local\Programs\Inno Setup 6\ISCC.exe"

Write-Host "=== Building $Arch ($Version) ===" -ForegroundColor Cyan

# Step 1: PyInstaller
Write-Host "[1/3] Running PyInstaller..." -ForegroundColor Yellow
& $py -m PyInstaller build.spec --noconfirm
if ($LASTEXITCODE -ne 0) { throw "PyInstaller failed" }

# Discover the built exe
$exePath = @(Get-ChildItem -LiteralPath dist -Filter "*.exe" -File | Select-Object -First 1 -ExpandProperty FullName)
if (-not $exePath) { throw "No exe found in dist/ after PyInstaller" }
Write-Host "  Found exe: $exePath" -ForegroundColor Gray

# Step 2: Create zip (portable)
Write-Host "[2/3] Creating portable zip..." -ForegroundColor Yellow
$null = New-Item -ItemType Directory -Path out -Force
Remove-Item -LiteralPath "out\$zipName" -ErrorAction SilentlyContinue
Compress-Archive -LiteralPath $exePath -DestinationPath "out\$zipName"

# Step 3: Create installer
Write-Host "[3/3] Creating installer..." -ForegroundColor Yellow
Remove-Item -LiteralPath "out\$setupName" -ErrorAction SilentlyContinue
& $iscc "installer\setup.iss" /DArch=$Arch /Q
if ($LASTEXITCODE -ne 0) { throw "Inno Setup failed" }

Write-Host "=== Done ===" -ForegroundColor Green
Write-Host "  Portable: out\$zipName" -ForegroundColor Green
Write-Host "  Installer: out\$setupName" -ForegroundColor Green
