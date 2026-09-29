$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvDir = Join-Path $scriptDir "venv"
$requirementsFile = Join-Path $scriptDir "requirements.txt"
$appFile = Join-Path $scriptDir "app.py"

if (-not (Test-Path $venvDir)) {
    Write-Host "Creating virtual environment..."
    python -m venv $venvDir
}

$pythonExe = Join-Path $venvDir "Scripts\python.exe"
$streamlitExe = Join-Path $venvDir "Scripts\streamlit.exe"

if (-not (Test-Path $pythonExe)) {
    throw "Python virtual environment was not created correctly."
}

if (-not (Test-Path $streamlitExe)) {
    Write-Host "Installing dependencies..."
    & $pythonExe -m pip install --upgrade pip
    & $pythonExe -m pip install -r $requirementsFile
}

Write-Host "Starting the FAQ chatbot..."
& $pythonExe -m streamlit run $appFile --server.headless true --server.address 127.0.0.1
