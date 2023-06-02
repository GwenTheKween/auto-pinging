#!/usr/bin/env python3
import argparse

def start(args):
    print(f"starting a timer for the branch {args.id}, which will go off in {args.time}")

def reset(args):
    print(f"resetting the timer for the branch {args.id}, setting a new ping in {args.time}")

def remove(args):
    print(f"removing the timer for branch {args.id}")

def main():
    # Parse arguments given in the CLI call.
    parser = argparse.ArgumentParser(description="Utility to automate pinging - or ping reminders - of patches in development mailing lists.")

    # Generic arguments that all subcommands use
    parser.add_argument ("--dry-run", action="store_true", help="Do not run commands that change the state of the system, only print the commands that would be run")
    parser.add_argument("--id", required=True, nargs=1)
    parser.add_argument("--time", "-t", required=True, nargs=1)

    # testing if I can use this for subcommands
    parser.add_argument("cmd", choices=["start", "reset", "remove"], help="Which command will be used.")

    ## Parsers for the subcommands
    #subparsers = parser.add_subparser("subcommands")
    #start_parser = subparsers.add_parser("start", help="start a timer to ping a given patch")
    #reset_parser = subparsers.add_parser("reset", help="reset the timer for pinging the given patch")
    #delete_parser = subparsers.add_parser("remove", help="remove the timer for pinging a patch")
    args = parser.parse_args()
    if args.cmd == "start":
        start(args)
    elif args.cmd == "reset":
        reset(args)
    elif args.cmd == "remove":
        reset(args)
    else:
        raise NotImplementedError("the subcommand does not seem to be implemented")

main()
