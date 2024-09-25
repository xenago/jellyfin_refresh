# `jellyfin_refresh`

A small script to refresh Jellyfin library content only if the library folders are accessible at runtime.

Using the API, it requests a list of library mountpoints and checks to ensure they are all accessible folders before triggering a refresh; if this process fails then a library scan is not triggered.

## Background

Jellyfin versions [prior to 10.9](https://github.com/jellyfin/jellyfin/issues/1714#issuecomment-2362798558) have a major deficiency: if an entire library's content is temporarily unavailable during a library refresh/scan, then the corresponding Jellyfin metadata/database content will be removed!

Even with versions 10.9+, the behavior is still insufficient to fully resolve the issue. Until a proper "recycle bin" function is added, this script may be helpful.

Obviously, this is a significant problem; SMB, NFS, or CephFS are typically used to logically separate bulk storage from the media server. If any of these are temporarily unavailable due to e.g. a network problem, then data loss within Jellyfin is likely if a scan occurs. The same applies for any storage, e.g. if a USB disk is removed or an rclone mount fails during a scan, data loss will happen. Backups are great, but why should the system have to be taken down to restore the entire metadata database if part of a library goes offline?

## Requirements

* Python 3
* Jellyfin server API key, generated in the Jellyfin Web UI at `/web/#!/apikeys.html`
* Tested with Jellyfin on Debian/Ubuntu; expected to work on other systems as well

## Usage

1. Read the script to ensure you understand what it is doing.

2. Download or copy `jellyfin_refresh.py` to the server

       wget https://raw.githubusercontent.com/xenago/jellyfin_refresh/main/jellyfin_refresh.py

3. Run the script, replacing the address and API key with your own (ensure that the running user account can access the folders):

       python3 jellyfin_refresh.py --address=https://jellyfin.mydomain.com --apikey=5cfbeb1325e24721ae142efb343d4921

4. If it works as expected, disable the automatic library scanning/refresh functionality within Jellyfin, and schedule this script to run instead (e.g. with your usual media import process, or with cron).
