#!/usr/bin/env python3
import argparse
import subprocess
import os

def check_for_dependencies(args):
    deps = []
    if args.remind:
        deps += ['notify-send']
    else:
        deps += ['git']

    not_found = []
    for d in deps:
        proc = subprocess.run(['which', d], stdout=subprocess.DEVNULL)
        if proc.returncode != 0:
            not_found.append(d)
    #specifically checking for git send-email
    if args.remind == False:
        proc = subprocess.run(['git', 'send-email'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = proc.stdout.decode('utf-8')
        if not output.find("No patch files specified!"):
            print(output)
            not_found.append('git-send-email')
    return not_found

def first_setup(path):
    try:
        f = open(path, 'r')
        f.close()
    except:
        print(f"no file {path}. Creating an empty one")
        f = open(path, "w")
        f.close()

def start(args):
    return

def reset(args):
    print(f"resetting the timer for the branch {args.branch}")

def remove(args):
    print(f"removing the timer for branch {args.branch}")

def main():
    # Parse arguments given in the CLI call.
    parser = argparse.ArgumentParser(description="Utility to automate pinging - or ping reminders - of patches in development mailing lists.")
    parser.add_argument ("--dry-run", action="store_true", help="Do not run commands that change the state of the system, only print the commands that would be run")
    #The ID that my git aliases will use will be branch name, but it doesn't have to be
    parser.add_argument("--branch", "-b", required=True, help="the identifier of the patch series. Likely the branch that contains the commits.")
    parser.add_argument("--email", "-e", required=True, help="The email ID that the script will use if the it pings automatically")
    parser.add_argument("--time", "-t", required=True, type=int, help="how long from now to ping/remind")
    parser.add_argument("--remind", "-r", required=False, action="store_true", help="should this script ping on its own or only send a reminder (using notify-send)?")
    parser.add_argument("cmd", choices=["start", "reset", "remove"], help="Which command will be used.")
    args = parser.parse_args()

    missing = check_for_dependencies(args)
    if missing != []:
        print(f"Missing the following dependencies to run the script as requested: {missing}")
        return

    database = os.getenv('HOME')+'/.patches.csv'

    first_setup (database)

    if args.cmd == "start":
        start(args)
    elif args.cmd == "reset":
        reset(args)
    elif args.cmd == "remove":
        reset(args)
    else:
        raise NotImplementedError("the subcommand does not seem to be implemented")

main()
