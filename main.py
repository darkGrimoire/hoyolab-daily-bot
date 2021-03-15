import time
import requests
import browser_cookie3

ACT_ID = 'e202102251931481'
DOMAIN_NAME = '.mihoyo.com'

cookies = browser_cookie3.load(domain_name=DOMAIN_NAME)

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

def main():
    print("Connecting to mihoyo...")
    isDone = False
    while not isDone:
        check = isClaimed()
        if not check and check != None:
            print("Reward not claimed yet. Claiming reward...")
            resp = claimReward()
            if resp:
                print("Claiming completed! message:")
                print(resp['message'])
                isDone = True
        if check:
            print("Reward has been claimed!")
            isDone = True
        if not isDone:
            print("There was an error... retrying in a minute")
            time.sleep(60)

if __name__ == "__main__":
    main()
