# `jellyfin_refresh`

A small script to refresh Jellyfin library content only if the library folders are accessible at runtime.

Using the API, it requests a list of library mountpoints and checks to ensure they are all accessible folders before triggering a refresh; if this process fails then a library scan is not triggered.

## Background

Jellyfin has a major deficiency that has been left unresolved for many years: if *any* library content is temporarily unavailable during a library refresh/scan, then the corresponding Jellyfin metadata/database content will be removed!

Obviously, this is a significant problem; most users employ remote storage systems such as a NAS or CephFS to logically separate their bulk storage from their media server. If any of these are temporarily unavailable due to e.g. a network problem, then data loss within Jellyfin is likely if a scan occurs. The same applies for any storage, e.g. if a USB disk is removed or an rclone mount fails during a scan, data loss will happen. Backups are great, but why should the system have to be taken down to restore the entire metadata database if a drive is temporarily offline?

Many [people have pointed this out](https://features.jellyfin.org/posts/399/dont-remove-missing-media-during-library-scan), but no action has been taken on this problem as [the developers do not see it as a critical issue, for some inexplicable reason](https://github.com/jellyfin/jellyfin/issues/1714#issuecomment-1328110567)! Some PRs and suggestions have been made, yet so far there has been no noticeable progress.

Utterly baffling... hopefully this script helps others deal with the issue.

## Requirements

* Python 3
* Jellyfin server API key, generated in the Jellyfin Web UI at `/web/#!/apikeys.html`
* Tested with Jellyfin on Debian/Ubuntu; expected to work on other systems as well

## Usage

1. Read the script to ensure you understand what it is doing.

2. Download or copy `jellyfin_refresh.py` to the server

       wget https://raw.githubusercontent.com/xenago/jellyfin_refresh/master/jellyfin_refresh.py

3. Run the script, replacing the address and API key with your own (ensure that the running user account can access the folders):

       python3 jellyfin_refresh.py --address=https://jellyfin.mydomain.com --apikey=5cfbeb1325e24721ae142efb343d4921

4. If it works as expected, disable the automatic library scanning/refresh functionality within Jellyfin, and schedule this script to run instead (e.g. with your usual media import process, or with cron).
