import argparse
import os
import requests

import sys

APP_NAME = "jellyfin_refresh"  # Used in the CLI and to identify the client to Jellyfin
APP_VERSION = "0.1"  # Used to identify the client to Jellyfin
CONTENT_TYPE_JSON = "application/json"
HEADER_AUTHORIZATON = "Authorization"
HEADER_CONTENT_TYPE = "Content-Type"
INTERNAL_JELLYFIN_FOLDER = "/var/lib/jellyfin/"  # Using Debian/Ubuntu paths
TEMPLATE_AUTHORIZATION = "MediaBrowser Token=\"{}\"" + f", Client=\"{APP_NAME}\", Version=\"{APP_VERSION}\""  # Jellyfin API Authorization: https://gist.github.com/nielsvanvelzen/ea047d9028f676185832e51ffaf12a6f

# Parse launch args
def arg_parser():
    arg_parser_instance = argparse.ArgumentParser(APP_NAME)
    arg_parser_instance.add_argument(
        "--apikey",
        help="Jellyfin API key, e.g. `5cfbeb1325e24721ae142efb343d4921`",
        type=str
    )
    arg_parser_instance.add_argument(
        "--address",
        help="Jellyfin website address, including protocol and no trailing slash. e.g. `https://myjellyfinserver.com`",
        type=str
    )
    return arg_parser_instance


# Run main if script executed directly
if __name__ == "__main__":
    print(f"Starting {APP_NAME}...")
    parser = arg_parser()
    args = parser.parse_args()
    print(f"Provided server address: `{args.address}`.")
    result = requests.get(
        args.address + "/Library/PhysicalPaths",
        headers={HEADER_CONTENT_TYPE: CONTENT_TYPE_JSON,
                 HEADER_AUTHORIZATON: TEMPLATE_AUTHORIZATION.format(args.apikey)}
    )
    if result.status_code != 200:
        print(f"Error getting Library paths from Jellyfin API: {result}, {result.content}", file=sys.stderr)
        exit(1)
    paths = result.json()
    if len(paths) < 3:
        # It is expected that at least 3 library paths are defined, since two default paths are in the list for collections/playlists
        print(
            f"There are fewer than 2 paths defined, which suggests that no libraries exist: `{paths}`",
            file=sys.stderr
        )
        exit(3)
    print(f"There are {len(paths)} library paths defined.")
    for path in paths:
        print(f"Checking `{path}`...")
        # Don't bother testing anything in the Jellyfin install folder, but should be ok if it does
        if not path.startswith(INTERNAL_JELLYFIN_FOLDER) and not (os.path.exists(path) and os.path.isdir(path)):
            print(f"Path is not an accessible folder: `{path}`", file=sys.stderr)
            exit(4)
    print("All paths are accessible; starting scan now.")
    result = requests.post(
        args.address + "/Library/Refresh",
        headers={HEADER_CONTENT_TYPE: CONTENT_TYPE_JSON,
                 HEADER_AUTHORIZATON: TEMPLATE_AUTHORIZATION.format(args.apikey)}
    )
    if result.status_code != 204:
        print(f"Error starting library refresh: {result}, {result.content}", file=sys.stderr)
        exit(4)
    print(f"Scan started; {APP_NAME} complete.")
