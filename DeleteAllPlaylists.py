# Author: Matthew Robinson
# License: MIT <LICENSE>
#
# Usage: python DeleteAllPlaylists.py oauth_file_prefix [--delete]
#
# Authenticates using oauth from stored crentials in oauth_file_prefix+".gMusic.oauth"
# Deletes all users playlists only if '--delete' option is given, else just lists them

from common import *

if len(sys.argv) < 2:
    log('ERROR oauth user key name is required')
    exit()

# log in and load playlists
oauth_file_prefix = sys.argv[1]
api = open_api(oauth_file_prefix)

def playlist_handler(playlist_name, playlist_description, playlist_id):
    # skip no-name playlists
    if not playlist_name: return

    log(u'Found playlist '+playlist_name+u' for deletion')
    if '--delete' in sys.argv:
        log(u'Deleting '+playlist_name+u' with ID '+playlist_id)
        api.delete_playlist(playlist_id)


playlists = api.get_all_playlists()

for playlist in playlists:
    playlist_name = playlist.get('name')
    playlist_description = playlist.get('description')
    playlist_id = playlist.get('id')

    playlist_handler(playlist_name, playlist_description, playlist_id)

close_api()
    
