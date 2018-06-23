#!/bin/sh

# Lab 10 Task 3 Solution
#
# This script uses curl commands to take a DB snapshot on the Grid,
# this script performs the following:
#  1) Prompt user for description text (required)
#  2) Check to see if there is an existing snapshot
#  3) If an old snapshot exists, prompt user to confrim deletion
#  4) Create database snapshot
#  5) Check to make sure snapshot was created
#  6) Remove connection cookie
#
# BUG: This script does not re-format comment to be URL compatible
# so if there is a white space, it will break the create call.
#
# Note: this script uses some other shell commands such as 'jq'
# 'sed' to extract the reference ID, these commands are not
# part of the course, instructors will not cover the usage
# of these tools in class.
# 
# Copyright (C) 2018 Infoblox. All Rights Reserved.

# 1) Prompt user for a comment for the snapshot
#echo "Please enter a comment for the new snapshot (no spaces):"
#read COMMENT
#if [ -z "$COMMENT" ] ; then
#    echo "Must provide a comment."
#    exit
#fi

# 2) Before taking a snapshot, check to see if there is an existing one.
# If a non-zero timestamp is returned, proceed with extracting the
# timestamp field and comment field.
CHECK_SNAPSHOT=`curl -s -k -u admin:infoblox -H 'Content-Type:application/json' \
  --cookie-jar '/tmp/wapi.auth' \
  -X GET 'https://{{ nios_provider.host }}/wapi/{{ wapi_version }}/dbsnapshot'`
OLD_TIMESTAMP_SEC=`echo "$CHECK_SNAPSHOT" | jq .[].timestamp | sed 's/"//g'`
#echo $OLD_TIMESTAMP_SEC
if [ ! -z $OLD_TIMESTAMP_SEC ] ; then
	OLD_SNAPSHOT=true
	OLD_TIMESTAMP=`date -d @$OLD_TIMESTAMP_SEC +%Y-%m-%d %T`
	OLD_COMMENT=`echo "$CHECK_SNAPSHOT" | jq .[].comment | sed 's/"//g'`
	echo $CHECK_SNAPSHOT
	echo $OLD_TIMESTAMP
	echo $OLD_COMMENT
else
	OLD_SNAPSHOT=false
fi

# 3) There can only be one snapshot at any given time, get user confirmation
# before erasing existing one
#if [ "$OLD_SNAPSHOT" = true ] ; then
#	echo "There is an existing snapshot [$OLD_COMMENT] taken at $OLD_TIMESTAMP"
#	echo "Are you sure you want to remove it and take a new snapshot? (Y/N)"
#	read ANS
#	case $ANS in
#	    Y) PROCEED=true ;;
#	    *)  PROCEED=false ; exit;
#3	esac
#fi

# 4) If we got here, user wants to create either a new snapshot or remove
# an existing snapshot, proceed
echo "Creating snapshot, please wait."
RESULT=`curl -s -k --cookie '/tmp/wapi.auth' -H 'Content-Type:application/json' \
    -X POST 'https://{{ nios_provider.host }}/wapi/{{ wapi_version }}/dbsnapshot?_function=save_db_snapshot' \
    --data '{"comment":"{{ comment }}"}'`
NEW_REF=`echo $RESULT | jq ._ref | sed 's/"//g'`
if [ $NEW_REF = "null" ] ; then
	echo "Creating snapshot failed."
	echo $RESULT
	exit
fi

# 5) Keep checking to make sure the db snapshot was created
while [ -z "$NEW_TIMESTAMP" ] ; do
	sleep 3
	NEW_SNAPSHOT=`curl -s -k --cookie '/tmp/wapi.auth' -H 'Content-Type:applicationo/json' \
	    -X GET 'https://{{ nios_provider.host }}/wapi/{{ wapi_version }}/dbsnapshot'`
	NEW_TIMESTAMP_SEC=`echo $NEW_SNAPSHOT | jq .[].timestamp | sed 's/"//g'`
	if [ ! -z $NEW_TIMESTAMP_SEC ] ; then
		NEW_TIMESTAMP=`date -d @$NEW_TIMESTAMP_SEC "+%Y-%m-%d %T"`
	fi
done
echo ""
echo "New snapshot created at $NEW_TIMESTAMP"

# 6) Clean up, remove cookie file
#rm -f /tmp/wapi.auth
