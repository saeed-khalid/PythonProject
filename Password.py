#!/usr/bin/env python3
import csv
import argparse
import os
import random
import string

def generate_password(length=12):
    """Generate a random password with given length."""
    return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))

def add_password(csv_file, service, username, password):
    """Add a new password to the CSV file."""
    with open(csv_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([service, username, password])

def get_password(csv_file, service):
    """Retrieve a password from the CSV file."""
    with open(csv_file, 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == service:
                return row[1:]
    return None

def update_password(csv_file, service, username=None, password=None):
    """Update a password in the CSV file."""
    temp_file = csv_file + '.temp'
    with open(csv_file, 'r', newline='') as f:
        reader = csv.reader(f)
        with open(temp_file, 'w', newline='') as f_temp:
            writer = csv.writer(f_temp)
            for row in reader:
                if row[0] == service:
                    if username:
                        row[1] = username
                    if password:
                        row[2] = password
                writer.writerow(row)
    os.remove(csv_file)
    os.rename(temp_file, csv_file)

def delete_password(csv_file, service):
    """Delete a password from the CSV file."""
    temp_file = csv_file + '.temp'
    with open(csv_file, 'r', newline='') as f:
        reader = csv.reader(f)
        with open(temp_file, 'w', newline='') as f_temp:
            writer = csv.writer(f_temp)
            for row in reader:
                if row[0] != service:
                    writer.writerow(row)
    os.remove(csv_file)
    os.rename(temp_file, csv_file)


def main():
    parser = argparse.ArgumentParser(description='Password Manager with CSV Storage')
    parser.add_argument('-h', '--help', action='help',
                        help='show this help message and exit')
    parser.add_argument('-a', '--add', nargs=3, metavar=('SERVICE', 'USERNAME', 'PASSWORD'),
                        help='add a new password for a service')
    parser.add_argument('-g', '--get', metavar='SERVICE',
                        help='get the password for a service')
    parser.add_argument('-u', '--update', nargs=3, metavar=('SERVICE', 'USERNAME', 'PASSWORD'),
                        help='update the password for a service')
    parser.add_argument('-d', '--delete', metavar='SERVICE',
                        help='delete the password for a service')
    parser.add_argument('-g', '--generate', metavar='SERVICE',
                        help='generate a new password for a service')
    args = parser.parse_args()

    if not args.add and not args.get and not args.update and not args.delete and not args.generate:
        print("Error: At least one of the -a, -g, -u, -d, or -g options is required.")
        return

    csv_file = 'passwords.csv'

    if args.add:
        service, username, password = args.add
        add_password(csv_file, service, username, password)
        print(f"Password for {service} added successfully!")

    elif args.get:
        service = args.get
        password = get_password(csv_file, service)
        if password:
            print(f"Password for {service}: {password}")
        else:
            print(f"Error: No password for {service} found.")

    elif args.update:
        service, username, password = args.update
        update_password(csv_file, service, username, password)
        print(f"Password for {service} updated successfully!")

    elif args.delete:
        service = args.delete
        delete_password(csv_file, service)
        print(f"Password for {service} deleted successfully!")

    elif args.generate:
        service = args.generate
        password = generate_password()
        add_password(csv_file, service, service, password)
        print(f"Password for {service} generated and added successfully: {password}")

    if __name__ == '__main__':
        main()