import os
import shodan
import yaml

def get_shodan_api_key(key_path):
    try:
        key = open(key_path, 'r').readline().split("\n")[0]
        return key
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


def save_shodan_results(path_to_file, results):
    with open(path_to_file, "w") as file:
        file.write(f"Results found {results['total']} :\n\n")
        for result in results['matches']:
            file.write(f"IP : {result['ip_str']}\n\n")
            file.write(f"{result['data']}")
            file.write("\n------------------------------\n\n")


def dnscan(domain):
    dir_path, domain = get_paths(domain, "dnscan")
    create_directories(dir_path)
    cmd_dns = dnscan_path + " -d " + domain + " -r -o " + dir_path + file_name
    os.system(cmd_dns)


def the_harvester(domain):
    dir_path, domain = get_paths(domain, "theHarvester")
    create_directories(dir_path)
    search_engines = get_search_engines_from_config("config/theHarvester.yml")
    parameters = get_harvester_params("config/theHarvester.yml")
    cmd_harvester = "theHarvester -d " + domain + " " + parameters + " " + search_engines + " -f " + dir_path + file_name
    os.system(cmd_harvester)


def get_search_engines_from_config(path_to_config):
    with open(path_to_config, "r") as file:
        config = yaml.safe_load(file)
        engines =  config["search_engines"].strip()
        if len(engines) == 0:
            return engines
        return ("-b " + engines)


def get_harvester_params(path_to_config): # Add tuto for shodan api key (locate shodansearch.py)
    with open(path_to_config, "r") as file:
        config = yaml.safe_load(file)
        elements = {"shodan_search": "s", "virtual_hosts": "v", "dns_lookup": "n"}
        params = "-" if any([config[element] for element in elements.keys()]) else ""
        for key, value in elements.items():
            if config[key]:
                params += value
    return params


def shodan_search(domain): # Look for more in-depth search
    results = api.search(domain)
    dir_path, domain = get_paths(domain, "shodan")
    path_to_file = dir_path + file_name
    create_directories(dir_path)
    save_shodan_results(path_to_file, results)


def urlscan(domain):
    dir_path, domain = get_paths(domain, "urlscan")
    filename = file_name.split(".")[0] + ".json" # Pas belle comme ligne mais solution rapide => Je remplace le .txt du filename en .json
    path_to_file = dir_path + filename
    create_directories(dir_path)
    os.system(f"curl \"https://urlscan.io/api/v1/search/?q=domain:{domain}\" | tee {path_to_file}")


def get_general_config(path_to_file):
    with open(path_to_file, "r") as file:
        return yaml.safe_load(file)


def handle_domain(domain):
    config = get_general_config("config/config.yml")
    if config["dnscan"]:
        dnscan(domain)
    if config["theHarvester"]:
        the_harvester(domain)
    if config["shodan"]:
        shodan_search(domain)
    if config["urlscan"]:
        urlscan(domain)


# def handle_mail(mail):
#     handle_domain(mail)


def handle_argument(arg, callback):
    if arg:
        callback(arg)