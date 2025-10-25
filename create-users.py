#!/usr/bin/python3

# INET4031
# Stephano Opdahl
# Date Created: Oct 2025
# Date Last Modified: Oct 2025

# Run Linux commands like useradd/passwd/usermod
import os
# Detect lines that start with '#' so we can treat them as comments
import re
# Read lines from stdin (we redirect the input file into the script)
import sys

def main():
    for line in sys.stdin:
        # Treat lines beginning with '#' as comments to skip
        match = re.match("^#", line)

        # Expect exactly 5 colon-separated fields per line
        # username : password : last : first : groups(comma-separated or '-')
        fields = line.strip().split(':')

        # Skip commented lines or lines with the wrong number of fields
        if match or len(fields) != 5:
            continue

        # Map the fields; GECOS stores "First Last,,," in /etc/passwd
        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3], fields[2])

        # Parse group list; '-' means no extra groups
        groups = fields[4].split(',')

        # Create the account with a disabled password; set GECOS
        print("==> Creating account for %s..." % (username))
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos, username)
        print(cmd)
        os.system(cmd)

        # Set the account password non-interactively
        print("==> Setting the password for %s..." % (username))
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password, password, username)
        print(cmd)
        os.system(cmd)

        # Add the user to each listed group (skip when '-')
        for group in groups:
            if group != '-':
                print("==> Assigning %s to the %s group..." % (username, group))
                cmd = "/usr/sbin/adduser %s %s" % (username, group)
                print(cmd)
                os.system(cmd)

if __name__ == '__main__':
    main()
