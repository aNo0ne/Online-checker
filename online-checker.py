import socket
import subprocess

def resolve_ip_address(domain):
    # Resolve the domain name to an IP address
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror:
        return None

def ping(ip_address):
    # Use the ping command to check the status of the IP address
    try:
        subprocess.check_output(["ping", "-c", "1", ip_address])
        return "Online"
    except subprocess.CalledProcessError:
        return "Offline"

def print_status(domain, status):
    # Define ANSI escape codes for colors
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

    # Print the domain and status with color
    if status == "Online":
        print(f"{domain:<20}{GREEN}{status:<10}{RESET}")
    elif status == "Offline":
        print(f"{domain:<20}{RED}{status:<10}{RESET}")
    elif status == "Invalid":
        print(f"{domain:<20}{'Invalid':<10}")

def is_valid_domain(domain):
    try:
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False

def save_domains(filename, domains):
    # Save the list of domains to a file
    with open(filename, "w") as file:
        for domain in domains:
            file.write(domain + "\n")

def load_domains(filename):
    # Load the list of domains from a file
    domains = []
    try:
        with open(filename, "r") as file:
            domains = [line.strip() for line in file]
    except FileNotFoundError:
        pass
    return domains

def main():
    # File name to store domains
    filename = "domains.txt"

    # Load the list of domains from the file
    domains = load_domains(filename)

    # Prompt the user for action: Execute or Edit
    action = input("Enter 'X' to execute with saved domains or 'E' to edit the list: ")

    if action.upper() == "E":
        # Edit the list of domains
        domains = []
        num_domains = int(input("Enter the number of domains: "))
        for i in range(num_domains):
            domain = input(f"Enter domain {i+1}: ")
            if is_valid_domain(domain):
                domains.append(domain)
                print("Domain is valid.")
            else:
                print("Invalid domain. Skipping...")

        # Save the updated list of domains to the file
        save_domains(filename, domains)

    # Print table header
    print(f"{'Domain':<20}{'Status':<10}")
    print("-" * 30)  # Line separator

    # Check the status of each domain
    for domain in domains:
        ip_address = resolve_ip_address(domain)
        if ip_address:
            status = ping(ip_address)
            print_status(domain, status)
        else:
            print_status(domain, "Invalid")

if __name__ == "__main__":
    main()

