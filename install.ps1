$ErrorActionPreference = "Stop"

$RepoUrl = "https://github.com/Amplicode/spring-skills.git"
$BaseDir = "$HOME\.agents"
$RepoDir = "$BaseDir\.amplicode\spring-skills"
$TargetDir = "$BaseDir\skills"

Write-Host "== Amplicode Spring Skills Installer =="

New-Item -ItemType Directory -Force -Path "$BaseDir\.amplicode" | Out-Null
New-Item -ItemType Directory -Force -Path "$TargetDir" | Out-Null

# --- Git sync ---
if (Test-Path "$RepoDir\.git") {
    Write-Host "✔ Repo exists, pulling latest..."
    git -C "$RepoDir" pull
} else {
    Write-Host "⬇ Cloning repository..."
    git clone $RepoUrl $RepoDir
}

# --- Symlinks for Codex ---
Write-Host "🔗 Creating/updating symlinks for Codex..."

Get-ChildItem "$RepoDir\skills" -Directory | ForEach-Object {
    $skillName = $_.Name
    $targetLink = Join-Path $TargetDir $skillName

    if (Test-Path $targetLink) {
        Write-Host "↻ Removing existing $skillName"
        Remove-Item $targetLink -Recurse -Force
    }

    New-Item -ItemType SymbolicLink `
        -Path $targetLink `
        -Target $_.FullName | Out-Null

    Write-Host "✔ Linked $skillName"
}

Write-Host "✅ Codex skills ready"

# --- Claude integration ---
Write-Host "🤖 Checking Claude CLI..."

$claudeExists = Get-Command claude -ErrorAction SilentlyContinue

if ($claudeExists) {
    Write-Host "✔ Claude found, installing plugins..."

    try {
        claude plugin marketplace add $RepoUrl
    } catch {}

    try {
        claude plugin install spring-tools@spring-tools
    } catch {}

    try {
        claude plugin update spring-tools@spring-tools
    } catch {}

    Write-Host "✅ Claude plugins ready"
} else {
    Write-Host "⚠ Claude CLI not found, skipping Claude setup"
}

Write-Host "🎉 Done"
