# PowerShell script to run the Google Search Agent Demo
# filepath: c:\Technical\AI Agents\ai-cookbook-main\models\openai\04-structured-output\run_demo.ps1

Write-Host "🤖 AutoGen Google Search Agent Demo Launcher" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

# Check if Python is installed
try {
    $pythonVersion = python --version 2>$null
    if ($pythonVersion) {
        Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python not found"
    }
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ and add it to your PATH" -ForegroundColor Yellow
    exit 1
}

# Check if required packages are installed
Write-Host "🔍 Checking required packages..." -ForegroundColor Yellow

$requiredPackages = @(
    "autogen-agentchat",
    "autogen-ext",
    "python-dotenv"
)

$missingPackages = @()

foreach ($package in $requiredPackages) {
    try {
        $result = pip show $package 2>$null
        if ($result) {
            Write-Host "✅ $package is installed" -ForegroundColor Green
        } else {
            $missingPackages += $package
        }
    } catch {
        $missingPackages += $package
    }
}

if ($missingPackages.Count -gt 0) {
    Write-Host "⚠️  Missing packages detected:" -ForegroundColor Yellow
    foreach ($package in $missingPackages) {
        Write-Host "   • $package" -ForegroundColor Red
    }
    
    $install = Read-Host "Do you want to install missing packages? (y/N)"
    if ($install -eq "y" -or $install -eq "Y") {
        Write-Host "📦 Installing missing packages..." -ForegroundColor Yellow
        foreach ($package in $missingPackages) {
            Write-Host "Installing $package..." -ForegroundColor Cyan
            pip install $package
        }
    } else {
        Write-Host "❌ Cannot proceed without required packages" -ForegroundColor Red
        exit 1
    }
}

# Check for .env file
$envFile = ".\.env"
if (-not (Test-Path $envFile)) {
    Write-Host "⚠️  .env file not found" -ForegroundColor Yellow
    Write-Host "Creating .env file from template..." -ForegroundColor Cyan
    
    if (Test-Path ".\.env.template") {
        Copy-Item ".\.env.template" ".\.env"
        Write-Host "✅ .env file created from template" -ForegroundColor Green
        Write-Host "🔧 Please edit .env file with your Azure OpenAI credentials" -ForegroundColor Yellow
        
        $edit = Read-Host "Do you want to edit .env file now? (y/N)"
        if ($edit -eq "y" -or $edit -eq "Y") {
            notepad .env
        }
    } else {
        Write-Host "❌ .env.template not found. Please create .env file manually" -ForegroundColor Red
        exit 1
    }
}

# Create output directory
$outputDir = "search_results"
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
    Write-Host "📁 Created output directory: $outputDir" -ForegroundColor Green
}

# Display menu
Write-Host ""
Write-Host "🚀 Ready to launch demo!" -ForegroundColor Green
Write-Host "Choose how to run the demo:" -ForegroundColor Cyan
Write-Host "1. Interactive menu (recommended)" -ForegroundColor White
Write-Host "2. Direct Google search demo" -ForegroundColor White
Write-Host "3. Test FileSurfer functionality" -ForegroundColor White
Write-Host "4. View saved files" -ForegroundColor White

$choice = Read-Host "Enter your choice (1-4)"

switch ($choice) {
    "1" {
        Write-Host "🎮 Launching interactive demo..." -ForegroundColor Cyan
        python run_search_demo.py
    }
    "2" {
        Write-Host "🔍 Launching Google search demo..." -ForegroundColor Cyan
        python agentchat_web_google_search.py
    }
    "3" {
        Write-Host "🧪 Testing FileSurfer functionality..." -ForegroundColor Cyan
        python test_file_saving.py
    }
    "4" {
        Write-Host "📁 Checking saved files..." -ForegroundColor Cyan
        if (Test-Path $outputDir) {
            $files = Get-ChildItem $outputDir -File
            if ($files.Count -gt 0) {
                Write-Host "Found $($files.Count) saved files:" -ForegroundColor Green
                foreach ($file in $files) {
                    $size = [math]::Round($file.Length / 1KB, 2)
                    Write-Host "  • $($file.Name) ($size KB, $($file.LastWriteTime))" -ForegroundColor White
                }
            } else {
                Write-Host "No saved files found in $outputDir" -ForegroundColor Yellow
            }
        } else {
            Write-Host "Output directory $outputDir does not exist" -ForegroundColor Red
        }
    }
    default {
        Write-Host "❌ Invalid choice. Launching default interactive demo..." -ForegroundColor Yellow
        python run_search_demo.py
    }
}

Write-Host ""
Write-Host "✅ Demo completed!" -ForegroundColor Green
Write-Host "📁 Check the '$outputDir' directory for saved search results" -ForegroundColor Cyan
