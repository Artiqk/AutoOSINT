import os

dnscan_path = "./dnscan/dnscan.py"

def dnscan(domain):
    dir_path = "scans/" + domain + "/dnscan/"
    if '@' in domain:
        domain = domain.split('@')[1]
    file_name = "result.txt"
    cmd_dir = "mkdir -p " + dir_path
    cmd_scan = dnscan_path + " -d " + domain + " -r -o " + dir_path + file_name
    os.system(cmd_dir)
    os.system(cmd_scan)


def handle_domain(domain):
    dnscan(domain)


def handle_mail(mail):
    dnscan(mail)


def handle_argument(arg, callback):
    if arg:
        callback(arg)