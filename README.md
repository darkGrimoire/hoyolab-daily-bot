# Genshin Hoyolab Daily Check-in Bot 📜🖋
Genshin Impact's Hoyolab Daily Check-in Bot is here! The concept is simple, **run once, run forever**. You only need to run it once, then it will continue to run forever (except if you uninstall it ofc tehe)

![Demo Gif](demo/demo.gif)

> #### Disclaimer: Only works on Windows (Linux & Mac version coming soon!)

# Features 🃏
- **Run once, run forever**✨ The program will configure itself to run daily according to your localtime's reward claiming time. It will also autorun if your laptop/computer is in sleep mode, and will still run the next time your computer is on if you skipped the server refresh time.
- If there's no connection, it will wait for a minute. No maximum retry.

# Prerequisites 🎯
- Windows OS
- Have login to mihoyo's website at any browser (A login for a year is enough)

# How to use ✨
1. [Download the newest release (.zip)](https://github.com/darkGrimoire/hoyolab-daily-bot/releases/latest) and extract
2. Run program and click Yes when prompted. The program needs to be run as administrator to enable scheduling
3. You can see what's the bot doing from `botlog.txt`.

# How to update 📈
Just overwrite the executable file haha

# Development Setup
1. Setup virtualenv
   ```
   pip install virtualenv
   python -m venv env
   env\Scripts\activate
   ```
2. Install dependencies
   ```
   pip install -r requirements.txt
   ```
3. Run `main.py` as administrator if you want to run the scheduling, or if not use `main.py -R`


Feel free to open up issues for feature request, bugs, etc. or contribute.