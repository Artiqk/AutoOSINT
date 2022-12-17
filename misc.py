import os
import shodan
import yaml

def get_shodan_api_key(key_path):
    try:
        key = open(key_path, 'r').readline().split("\n")[0]
    except:
        print(f"Shodan API key not found. Please write yours in : {os.path.abspath('./shodan_api.key')}")
        exit(0)

SHODAN_API_KEY = get_shodan_api_key("shodan_api.key")

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


def the_harvester(domain): # Add search engine search in config file
    dir_path, domain = get_paths(domain, "theHarvester")
    create_directories(dir_path)
    search_engines = get_search_engines_from_config("config/theHarvester.yml")
    cmd_harvester = "theHarvester -d " + domain + " -g -s -v -n " + search_engines + " -f " + dir_path + file_name
    os.system(cmd_harvester)


def get_search_engines_from_config(path_to_config):
    with open(path_to_config, "r") as file:
        config_data = yaml.safe_load(file)
        engines =  config_data["search_engines"].strip()
        if len(engines) == 0:
            return engines
        return ("-b " + engines)


def shodan_search(domain): # Look for more in-depth search
    results = api.search(domain)
    display_shodan_results(results)


def handle_domain(domain):
    dnscan(domain)
    the_harvester(domain)
    shodan_search(domain)


# def handle_mail(mail):
#     handle_domain(mail)


def handle_argument(arg, callback):
    if arg:
        callback(arg)