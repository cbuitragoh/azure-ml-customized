# Rem This script download data from kaggle datasets (with credentials) in Linux Terminal (bash)

kaggle datasets download -d nelgiriyewithana/top-spotify-songs-2023 -p ./experimentation/data

# unzip in experimentation/data/
cd experimentation/data
unzip top-spotify-songs-2023.zip

# delete original .zip file
rm top-spotify-songs-2023.zip

# Optional rename-file
mv spotify-2023.csv training.csv