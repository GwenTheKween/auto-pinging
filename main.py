#!/usr/bin/env python3
import argparse
import subprocess

def check_for_dependencies(args):
    deps = ['at']
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

def start(args):
    print(f"starting a timer for the branch {args.id}, which will go off in {args.time}")

def reset(args):
    print(f"resetting the timer for the branch {args.id}, setting a new ping in {args.time}")

def remove(args):
    print(f"removing the timer for branch {args.id}")

def main():
    # Parse arguments given in the CLI call.
    parser = argparse.ArgumentParser(description="Utility to automate pinging - or ping reminders - of patches in development mailing lists.")
    parser.add_argument ("--dry-run", action="store_true", help="Do not run commands that change the state of the system, only print the commands that would be run")
    parser.add_argument("--id", required=True, nargs=1)
    parser.add_argument("--time", "-t", required=True, nargs=1)
    parser.add_argument("--remind", "-r", required=False, action="store_true")
    parser.add_argument("cmd", choices=["start", "reset", "remove"], help="Which command will be used.")
    args = parser.parse_args()

    missing = check_for_dependencies(args)
    if missing != []:
        print(f"Missing the following dependencies to run the script as requested: {missing}")
        return

    if args.cmd == "start":
        start(args)
    elif args.cmd == "reset":
        reset(args)
    elif args.cmd == "remove":
        reset(args)
    else:
        raise NotImplementedError("the subcommand does not seem to be implemented")

main()
