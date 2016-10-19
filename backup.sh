#!/bin/bash -ex
adb root
adb wait-for-device
source .env/bin/activate
suffix=-$(date +%Y-%m-%d)
rm -f decrypted.db
./android-interact.sh db-decrypt
./android-interact.sh res
mv decrypted.db decrypted.db$suffix
ln -s decrypted.db$suffix decrypted.db
mkdir -p out
./dump-msg.py decrypted.db out
./list-chats.py decrypted.db
./count-message.sh out
mkdir -p html
./dump-html.py --all --output "html/"
