#!/usr/bin/env bash
set -e

git config core.hooksPath dev/hooks
chmod +x dev/hooks/pre-push

# Make pretty git log "git loglin"
git config --global alias.logline "log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"