# This script download data from kaggle datasets (with credentials) in Windows PowerShell
# pre-installation of the Kaggle API from https://pypi.org/project/kaggle/

kaggle datasets download -d nelgiriyewithana/top-spotify-songs-2023 -p ./experimentation/data

# unzip in experimentation/data/

Set-Location .\experimentation\data
Expand-Archive -Path "top-spotify-songs-2023.zip" -DestinationPath "."

# delete original .zip file
Remove-Item .\top-spotify-songs-2023.zip

# Optional rename-file
Rename-Item -Path spotify-2023.csv -NewName training.csv 