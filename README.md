# inet_4031_adduser_script

## Description
This project includes a Python script that automates creating multiple users and assigning them to groups on an Ubuntu system. It reads user data from an input file and sets up each account with the right name, password, and group memberships.

## Requirements
- Ubuntu system with `adduser`, `passwd`, and `sudo`
- Python 3 installed

## Input File Format
Each line contains five fields separated by colons:
username:password:last:first:group1,group2  
Use "-" for no groups. Lines starting with "#" are ignored.

## Dry Run (testing)
Comment out the three `os.system(cmd)` lines and keep the `print()` lines active.  
Run the script in dry run mode:
./create-users.py < create-users.input  

This shows what commands would run without actually adding users.

## Run For Real
Uncomment the three `os.system(cmd)` lines and then run:
sudo ./create-users.py < create-users.input  

This will create the accounts and assign them to their groups.

## Verify
Use these commands to confirm the users were added:
grep user0 /etc/passwd  
grep user0 /etc/group
