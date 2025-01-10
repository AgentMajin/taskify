# Activate virtual environment
& .\venv\Scripts\activate

# Change directory to the icons folder and run pyrcc5 command
Set-Location -Path .\resources
pyrcc5 icon.qrc -o icon_rc.py

# Navigate back to the parent directory and then to the UI folder
Set-Location -Path ..\ui

# Run pyuic5 command to convert the UI file
pyuic5 -x ui-design.ui -o main-ui.py

# Add import statements to main-ui.py
$mainUiPath = ".\main-ui.py"
$importStatements = @"
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources')))
"@
Add-Content -Path $mainUiPath -Value $importStatements

# Navigate back to the project's root directory
Set-Location -Path ..