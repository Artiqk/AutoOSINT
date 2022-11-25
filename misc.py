import os
import shodan


SHODAN_API_KEY = "GrKpd7opQhoCwrQKbDECaCjI6rWvIoU2"

api = shodan.Shodan(SHODAN_API_KEY)

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


def display_shodan_results(results):
    print(f"Results found {results['total']}")
    for result in results['matches']:
        print(f"IP : {result['ip_str']}")
        print(result['data'])
        print("------------------------------")


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


def shodan_search(domain):
    results = api.search(domain)
    display_shodan_results(results)


def handle_domain(domain):
    # dnscan(domain)
    # the_harvester(domain)
    shodan_search(domain)


# def handle_mail(mail):
#     handle_domain(mail)


def handle_argument(arg, callback):
    if arg:
        callback(arg)