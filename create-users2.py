#!/usr/bin/python3
import os, re, sys

def ask_dry_run():
    # Prompt from the real terminal so stdin can still be the input file
    try:
        tty = open('/dev/tty', 'r+')
        tty.write("Run in dry-run mode? (Y/N): ")
        tty.flush()
        ans = tty.readline().strip().lower()
        tty.close()
    except Exception:
        ans = 'y'  # default to safe dry-run if we cannot prompt
    return ans == 'y'

def main():
    dry_run = ask_dry_run()

    line_no = 0
    for raw in sys.stdin:
        line_no += 1
        line = raw.strip()

        # Skip blank lines
        if not line:
            continue

        # Commented line (starts with #)
        if re.match(r"^#", line):
            if dry_run:
                print(f"SKIP (comment) line {line_no}: {line}")
            # In real mode, stay quiet per instructions
            continue

        parts = line.split(':')

        # Must have exactly 5 fields: user:pass:last:first:groups
        if len(parts) != 5:
            if dry_run:
                print(f"ERROR line {line_no}: expected 5 fields -> {line}")
            # In real mode, stay quiet and skip bad lines
            continue

        username, password, last, first, groups_field = parts
        gecos = f"{first} {last},,,"

        # Parse groups (comma-separated). '-' means no extra groups.
        groups = [g.strip() for g in groups_field.split(',') if g.strip()]

        # 1) Create user
        cmd = f"/usr/sbin/adduser --disabled-password --gecos '{gecos}' {username}"
        if dry_run:
            print(f"WOULD RUN: {cmd}")
        else:
            os.system(cmd)

        # 2) Set password
        cmd = f"/bin/echo -ne '{password}\\n{password}' | /usr/bin/sudo /usr/bin/passwd {username}"
        if dry_run:
            print(f"WOULD RUN: {cmd}")
        else:
            os.system(cmd)

        # 3) Group membership (skip entries that are just '-')
        for g in groups:
            if g != '-':
                cmd = f"/usr/sbin/adduser {username} {g}"
                if dry_run:
                    print(f"WOULD RUN: {cmd}")
                else:
                    os.system(cmd)

if __name__ == '__main__':
    main()
