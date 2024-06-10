#!/usr/bin/env python3
import argparse
from bioblend import galaxy

parser = argparse.ArgumentParser()
parser.add_argument("-g", "--galaxy",
                    required=True,
                    dest="galaxy_url",
                    help="Target Galaxy instance URL/IP address (required "
                            "if not defined in the tools list file)")
parser.add_argument("-a", "--apikey",
                    required=True,
                    dest="api_key",
                    help="Galaxy admin user API key (required if not "
                            "defined in the tools list file)")
parser.add_argument("-r", "--remote",
                    help="Whether the user to be created should be a galaxy remote user, instead of a local user.")
parser.add_argument("-e", "--email",
                    required=True,
                    dest="user_email",
                    help="The email of the user to be managed.")
parser.add_argument("-u", "--username",
                    help="The username of the user to be created. Required when creating a non-remote user.")
parser.add_argument("-p", "--password",
                    dest="user_password",
                    help="The password of the user to be created. Required when creating a non-remote user.")
parser.add_argument("-d", "--delete",
                    action="store_true",
                    help="Whether to delete the user instead of creating it")
args = parser.parse_args()

gi = galaxy.GalaxyInstance(url=args.galaxy_url, key=args.api_key)
uc = galaxy.users.UserClient(gi)

# The create methods will return an existing user if the user exists already.
if args.remote:
    admin = uc.create_remote_user(user_email=args.user_email)
else:
    admin = uc.create_local_user(user_email=args.user_email, username=args.username, password=args.user_password)

if args.delete:
    uc.delete_user(admin['id'])
else:
    api_key = uc.get_or_create_user_apikey(admin['id'])
    print(api_key)
