#!/usr/bin/python -u
# -*- coding: utf8 -*-

from __future__ import unicode_literals

import todoist
import re
from sys import argv, exit
from time import sleep
from datetime import datetime as dt


logtime = dt.now

remind_pat_d = '\!([0-9]+)d'
remind_pat_h = '\!([0-9]+)h'
remind_pat_m = '\!([0-9]+)m'
remind_pat   = '\!([0-9]+)'

patterns = [ remind_pat_d, remind_pat_h, remind_pat_m, remind_pat ]
factors  = [ 24*60, 60, 1, 1 ]

def print_info( message, category ):
    try:
        print( u'[{0}] {1}: {2}'.format( str( logtime() ), category, message ) )
    except UnicodeEncodeError:
        print( u'[{0}] UnicodeEncode Error caught.'.format( logtime() ) )
    
def _debug( message ):
    print_info( message, "DBG" )

def log( message ):
    print_info( message, "LOG" )

def add_reminders( item ):
    if item['due_date_utc'] is None:
        return

    content = item['content']

    for pattern, factor in zip( patterns, factors ):

        m = re.findall(pattern, content)
        
        if m == []:
            continue
        
        new_content = re.sub( pattern, "", content ).strip()
    
        for match in m:
            api.reminders.add(item['id'], service="push", minute_offset=int(match)*factor )
            log( u'Added reminder of {}min to "{}"'.format( int(match)*factor, new_content) )

        content = new_content
        
    api.items.get_by_id(item['id']).update(content=content)
    debug( u'Updated items content to "{}"'.format( content ) )

def print_help():
    print "todoist_daemon.py -a API_KEY [-d for debug]"

if __name__ == "__main__":
    if '-d' in argv:
        debug = _debug
    else:
        debug = lambda x: x 

    if '-h' in argv or '--help' in argv:
        print_help()
        exit(0)
    
    skip_next=True
    api_key = ""

    try:
        for index,arg in enumerate(argv):
            if skip_next:
                skip_next = False
                continue

            if arg in ["-a", "--api"]:
                api_key = argv[index+1]
                skip_next = True
    except:
        print_help()
        exit(1)

    if not api_key:
        log( "No api key given" )
        exit(3)

    api = todoist.TodoistAPI(api_key)

    while True:  
        resp = api.sync()
        if "error_tag" in resp.keys():
            if resp["error_tag"] == "AUTH_INVALID_TOKEN":
                log( "Wrong API token" )
            else:
                log( "Something went wrong when syncing" )
                log( str(resp) )
            
            exit(2)

        items = api.items.all()
        for item in items:
            add_reminders( item )
        api.commit()
        sleep(1)

