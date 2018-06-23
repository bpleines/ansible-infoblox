""" Lab 10 Task 3 Solution

This python script checks to see if there is an existing database snapshot
before creating a new one. After creating one, it checks its existance and
gets the timestamp of the new snapshot.

This script is written in the style that is closer to a 'real'
python script, in that it uses a main() method, contains several sub 
routines/functions, and passes parameters/arguments to and from each
function.

Copyright (C) 2018 Infoblox. All Rights Reserved.
"""

import json
import requests
import urllib3
import time
from requests.auth import HTTPBasicAuth
from http.client import responses

# Disable self-signed certificate warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# setup grid connection parameters
gridmaster = "192.168.1.2"
username = "admin"
password = "infoblox"

def main():
    """Main function
     1) Connect to the Grid and store authentication cookie
     2) Prompt user for comment for the new database snapshot
     3) Search for exiting database snapshot, if any
     4) If old snapshot exists, prompt user to confirm deletion
     5) Create new database snapshot
     6) Check to make sure new snapshot was created
    """
    # 1) connect to Grid
    auth_cookie = wapi_connect()

    # 2) prompt user for new snapshot comment
    print("Please enter a comment for the new snapshot")
    new_comment = input()
    if not new_comment:
        print("Must provide a comment.")
        exit(1)

    # 3) Check for existing snapshot.
    old_snapshot = get_snapshot(auth_cookie)

    # 4) if old snapshot exists, print out its information and prompt user
    # for its deletion, since there can only be one snapshot at a time
    if old_snapshot['timestamp']:
        prompt_user(old_snapshot)

    # 5) Create new database snapshot
    create_snapshot(auth_cookie, new_comment)
    
    # 6) Retrieve new database snapshot and its timestamp, since the 
    # database snapshot may take some time to create, check it in a loop
    # until we find a valid timestamp
    new_timestamp = ''
    while not new_timestamp:
        time.sleep(3) # wait 3 seconds
        new_snapshot = get_snapshot(auth_cookie)
        new_timestamp = new_snapshot['timestamp']
    print("New snapshot created on " + new_timestamp)


def wapi_connect():
    """ Connects to the Grid and stores authentication cookie.
    This function connects by fetching the _schema object, and if the
    connection is successful, cookie is returned; if error occured
    during connection, it exits script execution.

    Args:
        None

    Returns:
        authentication cookie when succesfully connected 

    Outputs:
        prints error messages to STDOUT
    """
    login_url = 'https://' + gridmaster + '/wapi/v2.7/?_schema'
    try:
        login_result = requests.get(
            login_url,
            auth=HTTPBasicAuth(username, password),
            timeout=5,
            verify=False)
    except requests.exceptions.ConnectTimeout as e:
        print("Connection time out after 5 seconds.")
        exit(1)
    except requests.exceptions.ConnectionError as e:
        print("No route to host " + gridmaster)
        exit(1)

    if has_error(login_result):
        exit(1)
    else:
        return login_result.cookies


def get_snapshot(_cookie):
    """Gets existing database snapshot from Grid
    There can only be one database snapshot at any time, this function
    checks the Grid to see if there is already an existing one, and
    extracts its information into a dictionary.

    Notes:
        The timestamp from 'dbsnapshot' is in Epoch time, a long
        integer, is converted to humanly readable format for display

    Args:
        _cookie: authentication cookie

    Returns:
        dictionary containing dbsnapshot information; null if error.
        The dictionary looks like this:
        {
            'timestamp': '2018-09-12 13:52:19',
            'comment': 'this is a comment'
        }
    """
    # check connection is valid, end sub routine if no connection
    if not _cookie:
        print("No connection to the Grid.")
        return
    
    # fetch current database snapshot
    get_url = 'https://' + gridmaster + '/wapi/v2.7/dbsnapshot'
    get_result = requests.get(
        get_url,
        timeout=5,
        cookies=_cookie,
        verify=False)

    # extract information into a dictionary for easier processing,
    # if there are errors, return empty dictionary
    if not has_error(get_result):
        response_data = get_result.json()
        _comment = response_data[0]['comment']
        _seconds = response_data[0]['timestamp']
        _formatted_time = seconds_to_date(_seconds)
        dictionary = {
            "comment":_comment,
            "timestamp":_formatted_time }
        return dictionary
    return []


def seconds_to_date(_seconds):
    """Converts Epoch time (seconds) to human readable format

    Inputs:
        _seconds: Epoch time (number of seconds) as a string (ex: '1522225701')

    Returns:
        readable date format as a string (ex: 2018-03-28 08:28:21')
    """
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(_seconds))


def prompt_user(_snapshot):
    """Prompts user before deleting old dbsnapshot

    Args:
        _snapshot: dictionary containing information about the dbsnapshot, it
        looks like this:
        {
            'timestamp': '2018-09-12 13:52:19',
            'comment': 'this is a comment'
        }

    Returns:
        None

    Outputs:
        Prints text to STDOUT requiring user to interact

    Side Effects:
        Exits the entire script if user chose to not delete dbsnapshot
        
    """
    print("There is an existing snapshot [%s] taken at %s" %
        (_snapshot['comment'], _snapshot['timestamp']))
    print("Are you sure you want to remove it and take a new snapshot? (Y/N)")
    answer = input()
    if answer == "Y":
        pass
    else:
        exit(0)


def create_snapshot(_cookie, _comment):
    """Creates database snapshot on the Grid

    Args:
        _cookie: authentication cookie
        _comment: comment for the snapshot as a string
    
    Returns:
        None

    Outputs:
        If successful, informs by printing to STDOUT

    Side Effects:
        Creates WAPI object 'dbsnapshot' on the Grid if successful
    """
    # check connection is valid, end sub routine if no connection
    if not _cookie:
        print("No connection to the Grid.")
        return

    # create database snapshot    
    function = '?_function=save_db_snapshot'
    post_url = 'https://' + gridmaster + '/wapi/v2.7/dbsnapshot' + function
    data = {'comment':_comment}
    json_payload = json.dumps(data)
    post_result = requests.post(
        post_url,
        timeout=5,
        cookies=_cookie,
        data=json_payload,
        verify=False)

    if has_error(post_result):
        exit(1)
    else:
        print("Database snapshot started.")


def has_error(_result):
    """ Checks HTTP code and JSON response for errors.
    This function is designed to be run every time a HTTP request has
    beeb made, to check whether or not the response contains any errors.
    It first checks if the HTTP response code is successful (200 and 201),
    and only proceed to more checking if the response is NOT successful.

    Args:
        result of a python requests (such as GET, POST, PUT, or DELETE)

    Returns:
        0 if no errors, 1 if error occured

    Outputs:
        Prints error details to STDOUT
    """
    # if status code is 200 or 201, everything is okay, and there is
    # no need to check for other error messages
    if _result.status_code == 200:
        return 0
    elif _result.status_code == 201:
        return 0

    # if we got here, something went wrong, try to get additional
    # error text if there is any. Depending on the type of error
    # encountered, there may or may not be a key named 'text',
    # hence the exception handling for KeyError; also, the response
    # may or may not be valid JSON structure, hence JSONDecodeError
    # exception.
    try:
        err_text = _result.json()['text']
    except KeyError as e:
        err_text = "Response contains no error text"
    except json.decoder.JSONDecodeError as e:
        err_text = "No JSON Response"

    # print out the HTTP response code, description, and error text 
    http_code = _result.status_code
    http_desc = responses[http_code]
    print("HTTP Code [%3d] %s. %s" % (http_code, http_desc, err_text))
    return 1


# execute main(), which executes this entire script
if __name__ == "__main__":
    main()
