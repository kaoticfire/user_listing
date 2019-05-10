#  /usr/bin/python3.7
# 
#   Author: Virgil Hoover
#   License found in './License.txt'

#  /usr/bin/python3.7
#
#   Author: Virgil Hoover
#   License found in './GNU License.txt'

from os import getenv, listdir
from contextlib import redirect_stdout
from subprocess import call
from time import sleep
from socket import getfqdn
from tqdm import tqdm
from datetime import date
from re import sub


def progress_bar():
    for i in tqdm(range(100)):
        sleep(0.01)


def format_date():
    date_stamp = date.today().day
    year_stamp = date.today().year
    month_stamp = date.today().month
    date_str = str(year_stamp) + str('{:02d}'.format(month_stamp)) + str(date_stamp)
    return date_str


def user_listing(date_str):
    ip = str(input('Enter the IP '))
    print('Please wait while I generate the file.')
    file_name = getenv('UserProfile') + '\\Desktop\\' + getfqdn(str(ip)) + '_' + date_str + '.txt'
    access_method = 'w'
    try:
        name = getfqdn(ip)
        host = name.upper()
        domain = sub(r'mydomain.com', '', host)
        tag = domain.split('-')
        service_tag = tag[1]
        call('CMD /C echo Service Tag: ' + service_tag + ' >> ' + file_name)
        call('CMD /C echo Users: >> ' + file_name)
        with open(file_name, access_method) as lists:
            with redirect_stdout(lists):
                ignore = ['Administrator',
                          'All Users',
                          'Default',
                          'Default User',
                          'desktop.ini',
                          'GEN_DTP_COMPJOIN',
                          'Public',
                          'TEMP']
                folder = [x.lower() for x in listdir('\\\\' + ip + '\\c$\\Users') if x not in ignore]
                print()
                progress_bar()
                print(folder)
        call('cmd /c manage-bde -status -cn ' + ip + ' | findstr "Percentage Encrypted" >> ' + file_name)
    except PermissionError:
        print('Access to the remote system ' + domain + ' is not allowed at this time.')
        sleep(5.5)
    except IOError:
        print('Access Denied to ' + domain)
        sleep(5.5)


def main():
    date_str = format_date()
    user_listing(date_str)


# Call the main function if this is the application run
if __name__ == '__main__':
    main()
