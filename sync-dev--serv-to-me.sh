#!/usr/bin/env bash

echo "Running sync-server-to-me.sh"
echo "SERVER (SEB) =======> ME"
read -p "Are you sure? (y/n) " -n 1 -r
echo    # (optional) move to a new line
today=`date '+%Y_%m_%d__%H_%M_%S'`;
TARGET='seb:/home/jin/sites/bodt-dev.jinis.online'
LOCAL_DEV='/Users/jin/Personal/bodt-cms-dev'
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "===============Backing up first================="
    cp db.sqlite3 backup/dev/db.sqlite3._$today
    rsync -av ${LOCAL_DEV}/media ${LOCAL_DEV}/backup/dev
    echo "===============RSYNC============================"
    rsync -av jin@${TARGET}/media ${LOCAL_DEV}
    echo "===============Replacing Database==============="
    scp jin@${TARGET}/db.sqlite3 db.sqlite3
    echo ""
    echo "================================================"
    echo "Media and database sync-ed (downloaded) \/ \/ \/"
    echo "================================================"
fi
