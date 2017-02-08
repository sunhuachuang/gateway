try:
    from config import mail_host, mail_user, mail_password, mail_subject
except ImportError:
    print('copy config.py.exmaple to config.py and change mail to yourself.')

import re
import poplib
from email.parser import Parser

def get_servers_from_bak():
    with open('servers.bak') as f:
        content = f.readlines()

    return [x.strip() for x in content]

def save_servers_to_bak(servers):
    with open('servers.bak', 'w') as f:
        for server in servers:
            f.write(server + "\n")

def get_servers_from_email():
    pop_conn = poplib.POP3_SSL(mail_host)
    pop_conn.user(mail_user)
    pop_conn.pass_(mail_password)

    resp, mails, octets = pop_conn.list()
    index = len(mails)
    lastest_mail = []

    for i in range(index, 0, -1):
        lines = pop_conn.retr(i)[1]
        try:
            msg_content = b'\r\n'.join(lines).decode('utf-8')
        except UnicodeDecodeError:
            continue
        mail = Parser().parsestr(msg_content)

        if mail['Subject'] == mail_subject:
            lastest_mail = mail
            break

    pop_conn.quit()

    if not lastest_mail:
        print('no email from VPN Gate')
        exit(1)

    url_re = re.compile(r'http:\/\/[^\s]+:\d+\/')

    return url_re.findall(lastest_mail.get_payload())

def single_server_ping():
    pass

def get_best_server(servers):
    best_server = ''

    return best_server, servers

def main():
    new_servers = get_servers_from_email()
    bak_servers = get_servers_from_bak()
    servers = new_servers + [bak_server for bak_server in bak_servers if bak_server not in new_servers]

    best_server, good_servers = get_best_server(servers)
    save_servers_to_bak(good_servers)

    # connect best server.

    # change network config.

    pass

if __name__ == '__main__':
    main()
