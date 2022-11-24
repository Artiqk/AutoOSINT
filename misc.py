import os

dnscan_path = "./dnscan/dnscan.py"
file_name = "result.txt"

def get_paths(domain, tool_name):
    dir_path = "scans/" + domain + "/" + tool_name + "/"
    if '@' in domain:
        domain = domain.split('@')[1]
    return dir_path, domain


def create_directories(dir_path):
    cmd_dir = "mkdir -p " + dir_path
    os.system(cmd_dir)


def dnscan(domain):
    dir_path, domain = get_paths(domain, "dnscan")
    create_directories(dir_path)
    cmd_dns = dnscan_path + " -d " + domain + " -r -o " + dir_path + file_name
    os.system(cmd_dns)


def the_harvester(domain):
    dir_path, domain = get_paths(domain, "theHarvester")
    create_directories(dir_path)
    search_engine = "bing"
    cmd_harvester = "theHarvester -d " + domain + " -g -s -v -n -b " + search_engine + " -f " + dir_path + file_name
    os.system(cmd_harvester)


def handle_domain(domain):
    dnscan(domain)
    the_harvester(domain)


def handle_mail(mail):
    handle_domain(mail)


def handle_argument(arg, callback):
    if arg:
        callback(arg)