class script(object):

    START_TEXT = """<b>Hi ,
    
I'm A simple Zee5 Link Downloader Bot With Permanent Thumbnail Support.

Please Send Me Any Zee5 link, I Can Upload It To Telegram As File/Video.

Click <i>/help</i> For More Details....</b>"""


    HELP_USER = """<b>Hai, Follow These Steps..</b>
 
1. Send Custom Thumbnail (It Will Be Saved Permenantly!)

2. Send Your Zee5 Url And Select Desired Option.


NOTE: Download May Take Some Time! So Please Wait For It To Complete!"""


    ABOUT_TEXT = """⭕️<b>My Name : AIOM Zee5 DL Bot</b>

⭕️<b>Creater :</b> <a href='https://t.me/ajvadntr'>A̸̐J̵͋8̴̽1̶͐</a>

⭕️<b>Language :</b> <code>Python3</code>

⭕️<b>Library :</b> <a href='https://docs.pyrogram.org/'>Pyrogram 1.0.7</a> 

⭕️<b>Source Code :</b> <a href='https://github.com/ajvadntr/AIOM_ZEE5_DL_BOT'>Click Here</a>"""



    FORMAT_SELECTION = """<b>Choose appropriate option</b> <a href='{}'>⬇️</a>

🎞  - Stream format
📁  - File format

<i>NOTE : Taking high resolutions may result in files above 2GB and hence cannot Upload to TG. So better select a medium resolution.</i> 😇
"""    
    
    UPGRADE_TEXT = "PING At @ajvadntr"
    
    DOWNLOAD_START = "Trying To Download To My Server. This May Take A While"
    
    UPLOAD_START = "Uploading..."
    
    RCHD_TG_API_LIMIT = "Downloaded in {} seconds.\nDetected File Size: {}\nSorry. But, I Cannot Upload Files Greater Than 1.95GB Due To Telegram API limitations."

    AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS = "**Thank You For Using Meh!! ❤️**"
    
    SAVED_CUSTOM_THUMB_NAIL = "<b>✅️ Custom Thumbnail Saved </b>"
    
    DEL_ETED_CUSTOM_THUMB_NAIL = "✅ Custom Thumbnail Cleared Succesfully."
    
    SHOW_THUMB = "@ajvadntr\n\nUse /delthumb To Clear This Thumbnail."
    
    NO_THUMB = "No Saved Thumbnails Found!!"
    
    CUSTOM_CAPTION_UL_FILE = "<b>{newname}\n\n- @AIOM_BOTS -</b>"
    
    TIMEOUT = "<b><i>Sorry for the delay. It'll help reduce the flood wait</i> 😇\n\nWait for {} sec and try again.</b>"
    
