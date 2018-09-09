from ldap3 import Server, Connection, ALL
import configparser

config = configparser.ConfigParser()
config.read('ldap.conf')

server = config['Main']['Server']
username = config['Main']['Username']
password = config['Main']['Password']
baseDN = config['Main']['BaseDN']
emailFile = config['Main']['EmailFile']
outputFile = config['Main']['OutputFile']

s = Server(server, get_info=ALL)  
c = Connection(s, user='CN='+username+','+baseDN, password=password)

if not c.bind():
    print('error in bind', c.result)
c.start_tls()

f=open(emailFile)
emails = f.read().split('\n')
f.close

searchFilter = '(|'
for email in emails:
    searchFilter+='(mail=' + email + ')'
searchFilter+=')'

c.search(baseDN,searchFilter,attributes=['cn', 'mail', 'sAMAccountName'])
f = open(outputFile,'w')
for entry in c.entries:
    accountUsername = entry['sAMAccountName']
    f.write(accountUsername.values[0])
    print(accountUsername)
f.close