## Zee5 Downloader
If You Find Any Bugs, Report At @AIOM_BOTS_GROUP

**My Features**:

⭕️ Upload As file/video From Any NON-DRM Zee5 Link

⭕️ Permanent Thumbnail Support.

### Installation


#### Deploy To Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://www.heroku.com/deploy?template=https://github.com/ajvadntr/AIOM_ZEE5_DL_BOT)

#### Run In Your VPS

* Install Requirements

```sh
sudo apt install python3-pip
sudo apt install ffmpeg
```

* Create Config.py Appropriately (Refer Configs section)

* Run the app

```sh
git clone https://github.com/ajvadntr/AIOM_ZEE5_DL_BOT
cd Zee5-Downloader
pip3 install -r requirements.txt
python3 bot.py
```

## Configs

* TG_BOT_TOKEN  - Get bot token from @BotFather
* APP_ID        - From my.telegram.org
* API_HASH      - From my.telegram.org
* DB_URI        - PostgreSQL DB URL

## Commands

* /start             - Check if bot is alive
* /help              - To know how the bot works
* /upgrade           - Nothing much here
* /showthumb         - Shows saved thumbnail
* /delthumb          - Clear saved thumbnail
