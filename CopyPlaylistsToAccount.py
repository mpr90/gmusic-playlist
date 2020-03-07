# Author: Matthew Robinson
# License: MIT <LICENSE>
#
# Usage: python CopyPlaylistsToAccount.py
#
# Exports user playlists to separate folders, then imports them all into a single account prefixed by each user name
#

from common import *
import runpy
import sys
import glob
import os
import argparse

###########################################################################
def run_script(prog, args):
    argv_orig = sys.argv
    sys.argv = [prog] + args
    try:
        runpy.run_path(prog, run_name='__main__')
    except SystemExit as excp:
        sys.argv = argv_orig
        if excp.code == 0:
            pass
        else:
            raise
    sys.argv = argv_orig

###########################################################################
def export_playlist(username):
    if not username: return
    log('Exporting playlists for '+username)
    run_script('ExportLists.py', ["out_"+username, username])

###########################################################################

parser = argparse.ArgumentParser(description="Exports user playlists to separate folders, then imports them all into a single account, each playlist prefixed by source user name")
parser.add_argument('exportnames', metavar='user', type=str, nargs='+', help='Usernames for which to export playlists')
parser.add_argument('-i', '--import', metavar='importuser', required=True, help='Username in which to import user playists')
args = vars(parser.parse_args())

# Which users do we want to export playlists for
exportnames = args['exportnames']
importname  = args['import']

# Export all playlists for each named user
for user in exportnames:
    log("Exporting playlists from " + user)
    files=glob.glob("out_"+user+"/*")
    for f in files:
        log(" + Cleaning "+f)
        os.remove(f)
    export_playlist(user)

# Delete the old playlists
log('Deleting old playlists')
run_script('DeleteAllPlaylists.py', [importname, "--delete"])

# Import each user's playlists into single account with playlist names prefixed by source username
for user in exportnames:
    playlist_prefix = user.title() + "'s"
    log('Importing ' + playlist_prefix + ' playlists')
    files=glob.glob("out_"+user+"/*.csv")
    for f in files:
        log(' + ' + f)
        run_script("ImportList.py", [f, importname, playlist_prefix])
