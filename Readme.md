# Cspeakes POP3 Fuzzer

Sometimes during a pentest, you just need to check a bunch of username(s):password(s) pair(s) against an operational POP3 server. This is especially useful when you think you have custom wordlist(s) for usernames and passwords but don’t want to try them all manually. However please note that this process is in no way a quiet operation on the victim POP3 server in terms of traffic and logs left behind, as it literally just bangs auth pairs against the open server, reviewing the returned line lengths looking for variations in the POP3 server’s response to each username:password provided.

## Usage


#### *Single Auth Pair*
```
python3 cspeakes_pop3_server.py -i <ip> -p <port> -u <username> -pw <password>
```

#### *Username with Password_Wordlist, Port Defaults to 110*
```
python3 cspeakes_pop3_server.py -i <ip> -u <username> -PW <pass_wordlist>  
```

#### *Username_Wordlist AND Password_Wordlist*
```
python3 cspeakes_pop3_server.py -i <ip> -U <user_wordlist> -PW <pass_wordlist>
```

## Disclaimer
This script was created for educational purposes only. DO NOT use this script against any system or ip address that you do not have explicit permission to target. Actions such as these ARE ILLEGAL and I take no responsibility for this tool's misuse

Also, be careful when targeting any ip address for that matter as this is purely a developmental project and has no warranty expressed or implied.

*"Quit screwing around, you screw around too much!"* 
-- Richard Adler, South Park