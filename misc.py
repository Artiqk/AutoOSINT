def handle_domain(domain):
    print(domain)


def handle_mail(mail):
    print(mail)


def handle_argument(arg, callback):
    if arg:
        callback(arg)