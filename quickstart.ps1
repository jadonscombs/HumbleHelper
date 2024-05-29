# [shell quick compose deployment script on linux]
# NOTE:
#   this script should be executed on your local workstation, to
#   actually build and deploy the docker containers
#
# NOTE:
#   this script is NOT to be run in an already running docker container!

# helper function for loading ".env" file
function LoadEnvVars {
    Get-Content $PSScriptRoot\.env | ForEach-Object {
      $name, $value = $_.split('=')
      if ([string]::IsNullOrWhiteSpace($name) || $name.Contains('#')) {
        continue
      }
      Set-Content env:\$name $value
    }
  }

# check if .env file exists in project root and size greater than 0 bytes
if (!(Test-Path $PSScriptRoot\.env)) {
    Write-Host "Please create an '.env' file here, and insert the following text: BOT_TOKEN=<your.discord.bot.token>"
    Exit
}

# test if .env file's "BOT_TOKEN" field is non-empty/non-null before evaluating
LoadEnvVars
if ($null -eq $env:BOT_TOKEN) {
    Write-Host "Please create an '.env' file here, and insert the following text: BOT_TOKEN=<your.discord.bot.token>"
    Exit
}

# execute helper bot deployment with "docker compose" command
docker compose up -d --build