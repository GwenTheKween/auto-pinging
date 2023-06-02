#!/usr/bin/env python3
import argparse
import subprocess
import os
import datetime

database = ""

def check_for_dependencies(args):
    deps = ['crontab']
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

def read_all_lines ():
    l = []
    with open(database, 'r') as f:
        l = f.readlines()
    return l

def write_all_lines(lines):
    with open(database, "w") as f:
        for line in lines:
            f.write(line)

def first_setup():
    all_lines = []
    try:
        f = open(database, 'r')
        all_lines = f.readlines()
        f.close()
    except:
        print(f"no file {database}. Creating an empty one")
        f = open(database, "w")
        f.close()

    # Check if there is corruption in the file
    # (multiple lines with the same index)
    dic = {}
    for line in all_lines:
        b = line.split(',')[0]
        if b in dic:
            dic[b] += 1
        else:
            dic[b] = 1
    for b, count in dic.items():
        if count > 1:
            print(f"branch {b} is being tracked {count} times! Fix this by manually editing {database}")

# given a certain id BRANCH, find the index containing the related line
def find_line_index(branch, all_lines):
    ind = 0
    for line in all_lines:
        l_branch = line.split(',')[0]
        if branch == l_branch:
            return ind
        ind += 1
    # if we did not return in the loop, it isn't in the list of lines
    return -1

def add(args):
    # Confirm that all required arguments were provided
    if args.time is None and args.email is None:
        print("time (how many weeks to wait) and email (mail-ID) are required to start tracking a patch")
        return
    elif args.time is None:
        print("time (how many weeks to wait) is required to start the tracking")
        return
    elif args.email is None:
        print("Email (mail-ID) is required to track a patch")
        return

    # Check if the branch is already being monitored.
    repeat = 0
    existing = ""
    saved_lines = read_all_lines()
    index = find_line_index(args.branch, saved_lines)

    # Now calculate the line that will be stored
    ping_start = datetime.date.today() + datetime.timedelta(weeks = args.time)
    ping_string = ping_start.strftime("%d-%m-%Y")
    new_line = ','.join([args.branch, args.email, ping_string]) + '\n'

    #Check for errors and if user wants overwrite (if needed)
    if index >= 0:
        ping = saved_lines[index].split(',')[2]
        opt = input(f"{args.branch} is already in being monitored, PING_START is {ping}overwrite? (y/n)")
        if opt != 'y':
            print("exiting.")
            return
        else:
            print("overwritting")
            del saved_lines[index]

    # Add the line to the saved_lines, then write them all to the file
    saved_lines.append(new_line)
    write_all_lines(saved_lines)
    return

def ping(args):
    lines = read_all_lines()
    IDs = []
    # calculate the branches that must be pinged
    for l in lines:
        branch, email, date = l.strip().split(',')
        day, month, year = date.split('-')
        date = datetime.date(int(year), int(month), int(day))
        today = datetime.date.today()
        if today < date:
            print(f"skipping {branch}")
            continue
        IDs.append(branch if args.remind else email)

    # do the pinging
    if args.remind:
        subprocess.run(['notify-send', f'ping: {IDs}', '-a', 'auto-ping'])
    else:
        raise NotImplementedError("not yet")
    print(f"the following will be pinged: {IDs}")

def remove(args):
    lines = read_all_lines()
    ind = find_line_index(args.branch, lines)
    if ind < 0:
        print(f"branch {args.branch} is not being tracked")
        return
    del lines[ind]
    write_all_lines(lines)

def main():
    global database
    # Parse arguments given in the CLI call.
    parser = argparse.ArgumentParser(description="Utility to automate pinging - or ping reminders - of patches in development mailing lists.")
    parser.add_argument ("--dry-run", action="store_true", help="Do not run commands that change the state of the system, only print the commands that would be run")
    #The ID that my git aliases will use will be branch name, but it doesn't have to be
    parser.add_argument("--branch", "-b", required=True, help="the identifier of the patch series. Likely the branch that contains the commits.")
    parser.add_argument("--email", "-e", required=False, help="The email ID that the script will use if the it pings automatically")
    parser.add_argument("--time", "-t", required=False, type=int, help="how long from now to ping/remind")
    parser.add_argument("--remind", "-r", required=False, action="store_true", help="should this script ping on its own or only send a reminder (using notify-send)?")
    parser.add_argument("cmd", choices=["add", "ping", "remove"], help="Which command will be used.")
    args = parser.parse_args()

    missing = check_for_dependencies(args)
    if missing != []:
        print(f"Missing the following dependencies to run the script as requested: {missing}")
        return

    database = os.getenv('HOME')+'/.patches.csv'

    first_setup ()

    if args.cmd == "add":
        add(args)
    elif args.cmd == "ping":
        ping(args)
    elif args.cmd == "remove":
        remove(args)
    else:
        raise NotImplementedError("the subcommand does not seem to be implemented")

main()
