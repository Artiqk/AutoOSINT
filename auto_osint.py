#!/usr/bin/python3
import argparse
from misc import *

parser = argparse.ArgumentParser()

parser.add_argument("-d", "--domain", help="target single ip/domain")
parser.add_argument("-D", "--domains", help="target multiple ip/domain from file")

parser.add_argument("-m", "--mail", help="target single mail")
parser.add_argument("-M", "--mails", help="target multiple mails from file")

args = parser.parse_args()

handle_argument(args.domain, handle_domain)
# handle_argument(args.mail, handle_mail)

print(f"Scans results are stored under : {os.path.abspath(f'scans/{args.domain}/')}")