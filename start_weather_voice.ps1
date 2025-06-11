# Weather Assistant with Voice Output Startup Script
Write-Host "🌤️  Starting Weather Assistant with Voice Output" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

Set-Location $PSScriptRoot

# Check if virtual environment exists
if (-not (Test-Path ".venv")) {
    Write-Host "❌ Virtual environment not found. Creating one..." -ForegroundColor Red
    python -m venv .venv
}

# Activate virtual environment
& ".venv\Scripts\Activate.ps1"

# Install required packages
Write-Host "📦 Installing required packages..." -ForegroundColor Yellow
pip install -r speech_requirements.txt

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  .env file not found!" -ForegroundColor Yellow
    Write-Host "📝 Please copy .env.template to .env and configure your API keys" -ForegroundColor White
    Write-Host "🔗 Azure Speech Service: https://portal.azure.com" -ForegroundColor Blue
    Read-Host "Press Enter to exit"
    exit 1
}

# Run the weather application
Write-Host "🚀 Starting weather assistant..." -ForegroundColor Green
python 03-function-calling-weather.py

Read-Host "Press Enter to exit"
