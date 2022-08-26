import argparse
import time
from datetime import datetime, timedelta
import os
import sys
from random import randint
import subprocess
import requests
import browser_cookie3
import json

VER = '1.1.5 for Windows'
UPDATE_CHANNEL = 'https://github.com/darkGrimoire/hoyolab-daily-bot/releases/latest'

run_scheduler = True

# INITIALIZE PROGRAM ENVIRONMENT
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    app_path = os.path.dirname(sys.executable)
    exec_path = sys.executable
else:
    app_path = os.path.dirname(os.path.abspath(__file__))
    exec_path = "run.bat"

# SETUP LOGGING
log = open(os.path.join(app_path, 'botlog.txt'), 'a+')

# SETUP CONFIG
config = None
config_params = ['BROWSER', 'SERVER_UTC', 'DELAY_MINUTE', 'RANDOMIZE',
                 'RANDOM_RANGE', 'ACT_ID', 'DOMAIN_NAME', 'SCHEDULER_NAME']
try:
    config = json.load(open(os.path.join(app_path, 'config.json'), 'r'))
    for param in config_params:
        if param not in config:
            raise Exception(f"ERROR: Broken config file, {param} not found")
except Exception as e:
    print(repr(e))
    print("Config not found/corrupted! Making default config...")
    config = {
        'BROWSER': 'all',
        'SERVER_UTC': 8,
        'DELAY_MINUTE': 0,
        'RANDOMIZE': False,
        'RANDOM_RANGE': 3600,
        'ACT_ID': 'e202102251931481',
        'DOMAIN_NAME': '.hoyolab.com',
        'SCHEDULER_NAME': 'HoyolabCheckInBot'
    }
    config_file = open(os.path.join(app_path, 'config.json'), 'w')
    config_file.write(json.dumps(config))


# GET COOKIES
cookies = None
try:
    if config['BROWSER'].lower() == 'all':
        cookies = browser_cookie3.load(domain_name=config['DOMAIN_NAME'])
    elif config['BROWSER'].lower() == 'firefox':
        cookies = browser_cookie3.firefox(domain_name=config['DOMAIN_NAME'])
    elif config['BROWSER'].lower() == 'chrome':
        cookies = browser_cookie3.chrome(domain_name=config['DOMAIN_NAME'])
    elif config['BROWSER'].lower() == 'opera':
        cookies = browser_cookie3.opera(domain_name=config['DOMAIN_NAME'])
    elif config['BROWSER'].lower() == 'edge':
        cookies = browser_cookie3.edge(domain_name=config['DOMAIN_NAME'])
    elif config['BROWSER'].lower() == 'chromium':
        cookies = browser_cookie3.chromium(domain_name=config['DOMAIN_NAME'])
    else:
        raise Exception("ERROR: Browser not defined!")
except Exception as e:
    print("Login information not found! Please login first to hoyolab once in Chrome/Firefox/Opera/Edge/Chromium before using the bot.")
    print("You only need to login once for a year to https://www.hoyolab.com/genshin/ for this bot to work.")
    log.write("Login information not found! Please login first to hoyolab once in Chrome/Firefox/Opera/Edge/Chromium before using the bot.\n")
    log.write('LOGIN ERROR: cookies not found\n')
    log.close()
    time.sleep(5)
    sys.exit(1)

found = False
for cookie in cookies:
    if cookie.name == "cookie_token":
        found = True
        break
if not found:
    print("Login information not found! Please login first to hoyolab once in Chrome/Firefox/Opera/Edge/Chromium before using the bot.")
    print("You only need to login once for a year to https://www.hoyolab.com/genshin/ for this bot to work.")
    log.write("Login information not found! Please login first to hoyolab once in Chrome/Firefox/Opera/Edge/Chromium before using the bot.\n")
    log.write('LOGIN ERROR: cookies not found\n')
    log.close()
    time.sleep(5)
    sys.exit(1)

# ARGPARSE
help_text = 'Genshin Hoyolab Daily Check-In Bot\nWritten by darkGrimoire'
parser = argparse.ArgumentParser(description=help_text)
parser.add_argument("-v", "--version",
                    help="show program version", action="store_true")
parser.add_argument("-R", "--runascron",
                    help="run program without scheduler", action="store_true")

args = parser.parse_args()
if args.version:
    print(f"Bot ver. {VER}")
    log.close()
    sys.exit(0)
if args.runascron:
    run_scheduler = False


# API FUNCTIONS
def getDailyStatus():
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Origin': 'https://act.hoyolab.com',
        'Connection': 'keep-alive',
        'Referer': f'https://act.hoyolab.com/ys/event/signin-sea-v3/index.html?act_id={config["ACT_ID"]}&lang=en-us',
        'Cache-Control': 'max-age=0',
    }

    params = (
        ('lang', 'en-us'),
        ('act_id', config['ACT_ID']),
    )

    try:
        response = requests.get('https://sg-hk4e-api.hoyolab.com/event/sol/info',
                                headers=headers, params=params, cookies=cookies)
        return response.json()
    except requests.exceptions.ConnectionError as e:
        print("CONNECTION ERROR: cannot get daily check-in status")
        print(e)
        log.write('CONNECTION ERROR: cannot get daily check-in status\n')
        log.write(repr(e) + '\n')
        return None
    except Exception as e:
        print("ERROR: ")
        print(e)
        log.write('UNKNOWN ERROR:\n')
        log.write(repr(e) + '\n')
        return None


def isClaimed():
    resp = getDailyStatus()
    if resp:
        return resp['data']['is_sign']
    else:
        return None


def claimReward():
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/json;charset=utf-8',
        'Origin': 'https://act.hoyolab.com',
        'Connection': 'keep-alive',
        'Referer': f'https://act.hoyolab.com/ys/event/signin-sea-v3/index.html?act_id={config["ACT_ID"]}&lang=en-us',
    }

    params = (
        ('lang', 'en-us'),
    )

    data = {'act_id': config['ACT_ID']}

    try:
        response = requests.post('https://sg-hk4e-api.hoyolab.com/event/sol/sign',
                                 headers=headers, params=params, cookies=cookies, json=data)
        return response.json()
    except requests.exceptions.ConnectionError as e:
        print("CONNECTION ERROR: cannot claim daily check-in reward")
        print(e)
        log.write('CONNECTION ERROR: cannot claim daily check-in reward\n')
        log.write(repr(e) + '\n')
        return None
    except Exception as e:
        print("ERROR: ")
        print(e)
        log.write('UNKNOWN ERROR:\n')
        log.write(repr(e) + '\n')
        return None


# SCHEDULER CONFIGURATION
def configScheduler():
    print("Running scheduler...")
    cur_tz_offset = datetime.now().astimezone().utcoffset()
    target_tz_offset = timedelta(hours=config['SERVER_UTC'])
    delta = (cur_tz_offset - target_tz_offset)
    delta += timedelta(minutes=int(config['DELAY_MINUTE']))
    if (config['RANDOMIZE']):
        delta += timedelta(seconds=randint(0, int(config['RANDOM_RANGE'])))
    target_hour = int((24 + (delta.total_seconds()//3600)) % 24)
    target_minute = int((60 + (delta.total_seconds()//60)) % 60)
    target_seconds = int(delta.total_seconds() % 60)
    ret_code = subprocess.call((
        f'powershell',
        f'$Time = New-ScheduledTaskTrigger -Daily -At {target_hour}:{target_minute}:{target_seconds} \n',
        f'$Action = New-ScheduledTaskAction -Execute \'{exec_path}\' {"" if config["RANDOMIZE"] else "-Argument -R"} -WorkingDirectory "{app_path}" \n',
        f'$Setting = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -WakeToRun -RunOnlyIfNetworkAvailable -MultipleInstances Parallel -Priority 3 -RestartCount 30 -RestartInterval (New-TimeSpan -Minutes 1) \n',
        f'Register-ScheduledTask -Force -TaskName "{config["SCHEDULER_NAME"]}" -Trigger $Time -Action $Action -Settings $Setting -Description "Genshin Hoyolab Daily Check-In Bot {VER}" -RunLevel Highest'
    ), creationflags=0x08000000)
    if ret_code:
        print("PERMISSION ERROR: please run as administrator to enable task scheduling")
        log.write(
            "PERMISSION ERROR: please run as administrator to enable task scheduling\n")
        log.close()
        input()
        sys.exit(1)
    else:
        print("Program scheduled daily!")


# UPDATE CHECKER
def checkUpdates():
    res = requests.get(UPDATE_CHANNEL)
    newVer = res.url.split('/')[-1][1:]
    thisVer = VER.split()[0]
    if newVer > thisVer:
        print(
            f'New version (v{newVer}) available!\nPlease go to {UPDATE_CHANNEL} to download the new version.')
        log.write(
            f'New version (v{newVer}) available!\nPlease go to {UPDATE_CHANNEL} to download the new version.')
        time.sleep(60)


# MAIN PROGRAM
def main():
    log.write(f'\nSTART BOT: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n')
    print("Connecting to mihoyo...")
    is_done = False
    while not is_done:
        check = isClaimed()
        if not check and check != None:
            print("Reward not claimed yet. Claiming reward...")
            resp = claimReward()
            if resp:
                log.write(
                    f'Reward claimed at {datetime.now().strftime("%d %B, %Y | %H:%M:%S")}\n')
                print("Claiming completed! message:")
                print(resp['message'])
                is_done = True
        if check:
            log.write(
                f'Reward already claimed when checked at {datetime.now().strftime("%d %B, %Y | %H:%M:%S")}\n')
            print("Reward has been claimed!")
            is_done = True
        if not is_done:
            log.write(
                f'Error at {datetime.now().strftime("%d %B, %Y | %H:%M:%S")}, retrying...\n')
            print("There was an error... retrying in a minute")
            time.sleep(60)
    checkUpdates()
    log.close()


if __name__ == "__main__":
    if run_scheduler or config["RANDOMIZE"]:
        configScheduler()
    main()
    time.sleep(2)
