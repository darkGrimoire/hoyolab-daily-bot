import argparse
import time
import os
import sys
import subprocess
import requests
import browser_cookie3

ACT_ID = 'e202102251931481'
DOMAIN_NAME = '.mihoyo.com'
VER = '1.0 for Windows'

run_scheduler = True

# GET COOKIES
cookies = browser_cookie3.load(domain_name=DOMAIN_NAME)

# INITIALIZE PROGRAM ENVIRONMENT
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    app_path = os.path.dirname(sys.executable)
    exec_path = sys.executable
else:
    app_path = os.path.dirname(os.path.abspath(__file__))
    exec_path = f"python \'{os.path.abspath(__file__)}\'"

# ARGPARSE
help_text = 'Genshin Hoyolab Daily Check-In Bot\nWritten by darkGrimoire'
parser = argparse.ArgumentParser(description=help_text)
parser.add_argument("-v", "--version", help="show program version", action="store_true")
parser.add_argument("-R", "--runascron", help="run program without scheduler", action="store_true")

args = parser.parse_args()
if args.version:
    print(f"Bot ver. {VER}")
    sys.exit(0)
if args.runascron:
    run_scheduler = False

def getDailyStatus():
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Origin': 'https://webstatic-sea.mihoyo.com',
        'Connection': 'keep-alive',
        'Referer': f'https://webstatic-sea.mihoyo.com/ys/event/signin-sea/index.html?act_id={ACT_ID}&lang=en-us',
        'Cache-Control': 'max-age=0',
    }

    params = (
        ('lang', 'en-us'),
        ('act_id', ACT_ID),
    )

    try:
        response = requests.get('https://hk4e-api-os.mihoyo.com/event/sol/info', headers=headers, params=params, cookies=cookies)
        return response.json()
    except requests.exceptions.ConnectionError as e:
        print("CONNECTION ERROR: cannot get daily check-in status")
        print(e)
        return None
    except Exception as e:
        print("ERROR: ")
        print(e)
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
        'Origin': 'https://webstatic-sea.mihoyo.com',
        'Connection': 'keep-alive',
        'Referer': f'https://webstatic-sea.mihoyo.com/ys/event/signin- sea/index.html?act_id={ACT_ID}&lang=en-us',
    }

    params = (
        ('lang', 'en-us'),
    )

    data = { 'act_id':ACT_ID }

    try:
        response = requests.post('https://hk4e-api-os.mihoyo.com/event/sol/sign', headers=headers, params=params, cookies=cookies, json=data)
        return response.json()
    except requests.exceptions.ConnectionError:
        print("CONNECTION ERROR: cannot claim daily check-in reward")
        return False
    except Exception as e:
        print("ERROR: ")
        print(e)
        return False

def configScheduler():
    ret_code = subprocess.call((
        f'powershell',
        f'$Time = New-ScheduledTaskTrigger -Daily -At 4am \n',
        f'$Action = New-ScheduledTaskAction -Execute "{exec_path}" \n',
        f'$Setting = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -WakeToRun -RunOnlyIfNetworkAvailable -MultipleInstances Parallel -Priority 3 -RestartCount 30 -RestartInterval (New-TimeSpan -Minutes 1) \n',
        f'Register-ScheduledTask -Force -TaskName "HoyolabCheckInBot" -Trigger $Time -Action $Action -Settings $Setting -Description "SIX Auto Presence Submitter {VER}" -RunLevel Highest'
    ), creationflags=0x08000000)
    if ret_code:
        print("PERMISSION ERROR: please run as administrator to enable task scheduling")

def main():
    print("Connecting to mihoyo...")
    is_done = False
    while not is_done:
        check = isClaimed()
        if not check and check != None:
            print("Reward not claimed yet. Claiming reward...")
            resp = claimReward()
            if resp:
                print("Claiming completed! message:")
                print(resp['message'])
                is_done = True
        if check:
            print("Reward has been claimed!")
            is_done = True
        if not is_done:
            print("There was an error... retrying in a minute")
            time.sleep(60)

if __name__ == "__main__":
    if run_scheduler:
        configScheduler()
    main()
    time.sleep(2)
