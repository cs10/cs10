#! /usr/bin/env bash

echo "PUSH10 Message Found"
echo "Attempting to update the CS10 Website"
echo
# Rsync script to show progress of changes
# Uses compression and makes the dest. match the source
# This requires SSH access setup for the user pusing data.
# Use this to setup exclusions
excls="--exclude=.git/ --exclude=topic/original_bjc --exclude=topic/pd_bjc"
excls="${excls} --exclude=README.md --exclude=.nojekyll --exclude=.gitignore"
excls="${excls} --exclude=assess/ --exclude=glossary/ --exclude=prog/BYOB/"
excls="${excls} --exclude=.DS_Store"
sync="rsync -ahPvz --itemize-changes --progress --delete ${excls}"
cs10="cs10@cory.cs.berkeley.edu"
labloc="~/public_html/labs/"
$sync . $cs10:$labloc
ssh cs10@cory.cs.berkeley.edu "~/url.py"