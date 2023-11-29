# Genshin Hoyolab Daily Check-in Bot 📜🖋
The Genshin Hoyolab Daily Check-in Bot is a tool that automates the daily check-in process for Genshin Impact's Hoyolab. With this bot, you only need to run it once, and it will continue to run forever, claiming your daily rewards.

![Demo Gif](demo/demo.gif)

> #### Disclaimer: This bot only works on Windows (Linux & Mac version coming soon!)

## Features 🃏
- **Run once, run forever**✨ The program will configure itself to run daily according to your local time's reward claiming time. It will also autorun if your laptop/computer is in sleep mode and will still run the next time your computer is on if you skipped the server refresh time.
- **No connection, no problem**🌐 If there's no connection, it will wait for a minute and retry. No maximum retry limit.

## Prerequisites 🎯
- Windows OS
- Have logged in to mihoyo's website using any browser (A login for a year is enough)

## How to Use ✨
1. [Download the latest release (.zip)] and extract it.
2. Run the program and click "Yes" when prompted. The program needs to be run as an administrator to enable scheduling.
3. You can monitor the bot's activity from the `botlog.txt` file.

## Configuration File (v1.1.5+) 🔧
You can customize some settings in the `config.ini` file. Here are the available options:
- **BROWSER**: You can target a specific browser to be used for login. Please note that this program doesn't support multiple accounts yet, so choose a browser that only contains one account.  
Currently supported browsers are: `firefox`, `chrome`, `chromium`, `opera`, and `edge`. The default is `all`.
- **SERVER_UTC**: The server UTC in each region is different. You can check your UTC on [Your Hoyolab Daily Check-in page]. The default for the Asia server is +8 UTC.
- **DELAY_MINUTE**: Sometimes, your PC's time is a few minutes ahead of the server time. If you're experiencing the "reward already claimed" message when the bot starts, please add a delay.
- **RANDOMIZE**: Turn on (`true`) or off (`false`) to randomize the bot scheduler. The default is `false`.
- **RANDOM_RANGE**: The range in seconds for randomizing the bot scheduler. The default is `3600` (which means the bot will start with a random delay within 1 hour after the daily reset).
- **SCHEDULER_NAME**: The name of the bot scheduler. With this, you can have multiple bot schedules with different configurations. For example, in one folder, the bot is configured to log in from Chrome, while in another folder, it is configured to log in from Firefox. The default is "HoyolabCheckInBot".
- **ACT_ID** and **DOMAIN_NAME** do not need to be changed. They are included for future-proofing purposes.

## How to Update 📈
Simply overwrite the executable file.

## Development Setup 💻
1. Set up a virtual environment:
```bash
pip install virtualenv
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run `python main_windows.py` or `run.bat` as an administrator if you want to run the scheduling. If not, use `python main_windows.py -R` or `run.bat -R`.
4. Use Pyinstaller to compile into a binary.

## Feedback and Contribution 🙌
Feel free to open issues for feature requests, bug reports, etc., or contribute to the project.

: https://github.com/darkGrimoire/hoyolab-daily-bot/releases/latest
