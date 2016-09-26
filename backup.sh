#!/bin/bash -e
adb root
adb wait-for-device
source .env/bin/activate
suffix=-$(date +%Y-%m-%d)
rm -f decrypted.db
./android-interact.sh db-decrypt
./android-interact.sh res
mv decrypted.db decrypted.db$suffix
ln -s decrypted.db$suffix decrypted.db
mkdir -p out$suffix
./dump-msg.py decrypted.db out$suffix
./list-chats.py decrypted.db
./count-message.sh out
mkdir -p html$suffix
ls out$suffix/*.txt | while read f ; do ff=$(basename "$f" .txt) ; ./dump-html.py "$ff" --output "html$suffix/$ff.html" || true ; done
