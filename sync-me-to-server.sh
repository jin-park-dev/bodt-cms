#!/usr/bin/env bash

echo "Running sync-me-to-server.sh"
echo "ME =======> SERVER"
read -p "Are you sure? (y/n) " -n 1 -r
echo    # (optional) move to a new line
today=`date '+%Y_%m_%d__%H_%M_%S'`;
#seb='bodt.jinis.online';
TARGET='seb:/home/jin/sites/bodt.jinis.online'
LOCAL_DEV='/Users/jin/Personal/bodt-cms-master'
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "===============Backing server first============="
    scp jin@${TARGET}/db.sqlite3 ${LOCAL_DEV}/backup/server/db.sqlite3._${today}
    rsync -av jin@${TARGET}/media ${LOCAL_DEV}/backup/server/
    echo "===============RSYNC============================"
    rsync -av /Users/jin/Personal/bodt-cms-master/media jin@${TARGET}
    echo "===============Replacing Database==============="
    scp db.sqlite3 jin@${TARGET}/db.sqlite3
    echo ""
    echo "================================="
    echo "Media and database uploaded ^^^^^"
    echo "================================="
fi
