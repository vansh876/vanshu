import logging
import subprocess, os, argparse, json, time, binascii, base64, requests, sys, ffmpy
import re
from pywidevine.decrypt.wvdecrypt import WvDecrypt
from pymediainfo import MediaInfo

parser = argparse.ArgumentParser()
parser.add_argument("--keys", dest="keys", action="store_true", help="show keys and exit")
args = parser.parse_args()


currentFile = __file__
realPath = os.path.realpath(currentFile)
dirPath = os.path.dirname(realPath)
dirName = os.path.basename(dirPath)
ytdlp = dirPath + "/binaries/youtube-dl-aria2.exe"
ffmpegpath = dirPath + "/binaries/ffmpeg.exe"
aria2cexe = dirPath + "/binaries/aria2c.exe"
mp4decryptexe = dirPath + "/binaries/mp4decrypt1.exe"
mkvmergeexe = dirPath + "/binaries/mkvmerge.exe"
mp4dump = dirPath + "/binaries/mp4dump.exe"

FInput_video = dirPath + '/temp/vid_enc.mp4'
FInput_audio = dirPath + '/temp/aud_enc.m4a'
out_Audio = FInput_audio.replace('enc', 'dec')
out_Video = FInput_video.replace('enc', 'dec')
Remuxed_Video = out_Video.replace('mp4', 'H264')
Demuxed_Audio = out_Audio.replace('m4a', 'aac')

auth_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE2Mzg0NzU5NzEsImV4cCI6MTY3MDAxMTk3MSwiaXNzIjoiaHR0cHM6Ly91c2VyYXBpLnplZTUuY29tIiwiYXVkIjpbImh0dHBzOi8vdXNlcmFwaS56ZWU1LmNvbS9yZXNvdXJjZXMiLCJ1c2VyYXBpIiwic3Vic2NyaXB0aW9uYXBpIl0sImNsaWVudF9pZCI6InJlZnJlc2hfdG9rZW5fY2xpZW50Iiwic3ViIjoiY2NjMjE4NGYtYjQwNi00YTRkLTk2MjAtM2ZmZDUzZDUwYmQyIiwiYXV0aF90aW1lIjoxNjM4NDc1ODc5LCJpZHAiOiJsb2NhbCIsInVzZXJfaWQiOiJjY2MyMTg0Zi1iNDA2LTRhNGQtOTYyMC0zZmZkNTNkNTBiZDIiLCJzeXN0ZW0iOiJaNSIsImFjdGl2YXRpb25fZGF0ZSI6IjIwMTctMTItMTJUMDA6MDA6MDAiLCJjcmVhdGVkX2RhdGUiOiIiLCJyZWdpc3RyYXRpb25fY291bnRyeSI6IklOIiwidXNlcl9tb2JpbGUiOiI5MTcwMDQ4MTQyOTMiLCJzdWJzY3JpcHRpb25zIjoiW3tcImlkXCI6XCI5MTk3ZDJkYi0wZTZiLTQ0MGUtYWMzYi05MTM1ZmY1YzIzNjBcIixcInVzZXJfaWRcIjpcImNjYzIxODRmLWI0MDYtNGE0ZC05NjIwLTNmZmQ1M2Q1MGJkMlwiLFwiaWRlbnRpZmllclwiOlwiQ1JNXCIsXCJzdWJzY3JpcHRpb25fcGxhblwiOntcImlkXCI6XCIwLTExLTE4MzRcIixcImFzc2V0X3R5cGVcIjoxMSxcInN1YnNjcmlwdGlvbl9wbGFuX3R5cGVcIjpcIlNWT0RcIixcInRpdGxlXCI6XCJQcmVtaXVtXCIsXCJvcmlnaW5hbF90aXRsZVwiOlwiUHJlbWl1bVwiLFwic3lzdGVtXCI6XCJaNVwiLFwiZGVzY3JpcHRpb25cIjpcIlByZW1pdW0gUGFjayAtIDYgbXRoc1wiLFwiYmlsbGluZ19jeWNsZV90eXBlXCI6XCJkYXlzXCIsXCJiaWxsaW5nX2ZyZXF1ZW5jeVwiOjE4MCxcInByaWNlXCI6NTk5LjAsXCJjdXJyZW5jeVwiOlwiSU5SXCIsXCJjb3VudHJ5XCI6XCJJTlwiLFwiY291bnRyaWVzXCI6W1wiSU5cIl0sXCJzdGFydFwiOlwiMjAyMS0wMi0wMVQwMDowMDowMFpcIixcImVuZFwiOlwiMjAyMi0xMi0zMVQyMzo1OTo1OVpcIixcIm9ubHlfYXZhaWxhYmxlX3dpdGhfcHJvbW90aW9uXCI6ZmFsc2UsXCJyZWN1cnJpbmdcIjpmYWxzZSxcInBheW1lbnRfcHJvdmlkZXJzXCI6W3tcIm5hbWVcIjpcIlpFRTVcIn1dLFwicHJvbW90aW9uc1wiOltdLFwiYXNzZXRfdHlwZXNcIjpbNiwwLDldLFwiYXNzZXRfaWRzXCI6W10sXCJidXNpbmVzc190eXBlXCI6XCJmcmVlXCIsXCJiaWxsaW5nX3R5cGVcIjpcInByZW1pdW1cIixcIm51bWJlcl9vZl9zdXBwb3J0ZWRfZGV2aWNlc1wiOjUsXCJtb3ZpZV9hdWRpb19sYW5ndWFnZXNcIjpbXSxcInR2X3Nob3dfYXVkaW9fbGFuZ3VhZ2VzXCI6W10sXCJjaGFubmVsX2F1ZGlvX2xhbmd1YWdlc1wiOltdLFwidmFsaWRfZm9yX2FsbF9jb3VudHJpZXNcIjp0cnVlLFwiYWxsb3dlZF9wbGF5YmFja19kdXJhdGlvblwiOjYsXCJjYXRlZ29yeVwiOm51bGx9LFwic3Vic2NyaXB0aW9uX3N0YXJ0XCI6XCIyMDIxLTEyLTAyVDIwOjEyOjQ5Ljg0WlwiLFwic3Vic2NyaXB0aW9uX2VuZFwiOlwiMjAyMi0wNS0zMVQyMzo1OTo1OVpcIixcInN0YXRlXCI6XCJhY3RpdmF0ZWRcIixcInJlY3VycmluZ19lbmFibGVkXCI6ZmFsc2UsXCJwYXltZW50X3Byb3ZpZGVyXCI6XCJjcm1cIixcImZyZWVfdHJpYWxcIjpudWxsLFwiY3JlYXRlX2RhdGVcIjpcIjIwMjEtMTItMDJUMjA6MTI6NDkuODRaXCIsXCJpcF9hZGRyZXNzXCI6XCIxNTcuMzUuOTAuODlcIixcInJlZ2lvblwiOlwiQmloYXJcIixcImFkZGl0aW9uYWxcIjp7XCJwYXltZW50bW9kZVwiOlwiUHJlcGFpZENvZGVcIixcImNvdXBvbmNvZGVcIjpcIlo1TTZQVG9UckpIakZFXCJ9LFwiYWxsb3dlZF9iaWxsaW5nX2N5Y2xlc1wiOjAsXCJ1c2VkX2JpbGxpbmdfY3ljbGVzXCI6MH1dIiwiY3VycmVudF9jb3VudHJ5IjoiWloiLCJzY29wZSI6WyJ1c2VyYXBpIiwic3Vic2NyaXB0aW9uYXBpIiwib2ZmbGluZV9hY2Nlc3MiXSwiYW1yIjpbImRlbGVnYXRpb24iXX0.oc23r7B9Cu738oXSpiqiEHgfEDaNnbi6A6RBEhyOI0-jdUfNyCMt48y2Vqwhix9zgFtTJsAjs3dy0JSOb9t1gAFyRZus-ylpzv0AfH0X-mAwgZFbCmIBQqPZCXm1G0rvxaAnmOsvv-OeFBVUMeWLT3lAMcMe5JMy8gwOkLm6AKBgyxIKMnXaX1Wm0o4ndtFoaQfpZ1Sw5EXi-WFLy_4dtHNFvrUK77EqflhA5usarWrYtjww-Dxuh-rJ11wCvSDNRubG5x3ZLYTBj4SOurgOGbZPLATQqabaWsuf3lmEWFXapXz0xZaJ4OxYGhbyzqemw3i36k229ZVNoPuf0OvQUw"
dev_id = 'K6J3rzHjLhD2P1yXzpDZ000000000000'
licurl = "https://wv-keyos-aps1.licensekeyserver.co/"

def ReplaceDontLikeWord(X):
    X = X.replace(' !', '').replace('!', '').replace(' DRM', '').replace('…', '').replace('\n', '').replace(' : ', ' - ').replace(': ', ' - ').replace(':', ' - ').replace('&', 'and').replace('+', '').replace(';', '').replace('ÃƒÂ³', 'o').replace('[', '').replace(']', '').replace('/', '.').replace('//', '').replace('’', "").replace('*', 'x').replace('<', '').replace('>', '').replace('|', '').replace('~', '').replace('#', '').replace('%', '').replace('{', '').replace('}', '').replace(',', '').replace('?', '').replace("'","").replace('�', ' ').replace('"', '').replace('"', '').replace('  ', ' ').replace('(Telugu Dubbed) ','').replace('(Tamil Dubbed) ','').replace('(Hindi Dubbed) ','').replace('(Telugu dubbed) ','').replace('(Tamil dubbed) ','').replace('(Hindi dubbed) ','').replace('(telugu Dubbed) ','').replace('(tamil Dubbed) ','').replace('(hindi Dubbed) ','').replace('(telugu dubbed) ','').replace('(tamil dubbed) ','').replace('(hindi dubbed) ','').replace('(Telugu) ','').replace('(Tamil) ','').replace('(Hindi) ','').replace('(telugu) ','').replace('(tamil) ','').replace('(hindi) ','').replace('  ', ' ').replace('Season 2 ', '').replace('Season 1 ', '').replace('Season 3 ', '').replace('Season 5 ', '').replace('Season 4 ', '')
    X = X.replace(" - ","-").replace(" ",".")
    return X

def GetMPD(video_id, lic_token=False):
    api_url = "https://spapi.zee5.com/singlePlayback/getDetails/"
    access_token = requests.get('https://useraction.zee5.com/token/platform_tokens.php?platform_name=web_app').json()['token']
    
    api_headers = {
        "x-access-token": access_token
    }
    
    params = {
        'content_id': video_id,
        'device_id': dev_id,
        'platform_name': 'android_app',
        'translation': 'en',
        'user_language': 'his',
        'country': 'IN',
        'state': 'TN',
        'app_version': '2.50.52',
        'user_type': 'premium',
        'check_parental_control': False,
        'uid': dev_id,
        'ppid': dev_id,
        'version': 12
    }
        
    data = {
        'Authorization': f'bearer {auth_token}',
        'x-access-token': access_token
    }
    
    resp = requests.post(api_url, headers=api_headers, params=params, json=data).json()
    #print(resp)    
    if 'error_msg' in resp:
        print(f'\n{resp["error_msg"]}')
        exit()
        
    if lic_token:
        return resp['keyOsDetails']['drm']
    
    ContentType = resp['assetDetails']["asset_subtype"]
    if ContentType == "movie" or ContentType == 'trailer':
        title = resp['assetDetails']["title"]
        try:
            year = resp['assetDetails']["release_date"][0:4]
            output = f'{title}.{year}'
        except Exception:
            output = title

    elif ContentType == "episode":
        show_name = resp["assetDetails"]["tvshow_name"]
        
        s_id = resp["assetDetails"]["season"]
        for x in resp['showDetails']['seasons']:
            if x['id'] == s_id:
                s_num = x['orderid']
        
        season_number = str(s_num).zfill(2)
        episode_number = str(resp['assetDetails']["orderid"]).zfill(2)
        episode_title = resp['assetDetails']["title"]
        output = f'{show_name}.S{season_number}E{episode_number}.{episode_title}'
    
    MPD = resp['assetDetails']['video_url']['mpd'].split('?')[0].replace("-phone.mpd",".mpd").replace("https://vodprime-ak.akamaized.net","https://mediacloudfront.zee5.com")
    print(MPD)
    subs_res = resp['assetDetails']['subtitle_url']
    subs_lang = []
    subs_urls = []
    for x in range(len(subs_res)):
        subs_lang.append(subs_res[x]['language'])
        subs_urls.append(subs_res[x]['url'])
    
    return MPD, ReplaceDontLikeWord(output), subs_lang, subs_urls

def RipIt(video_id, qual):
    MPD, output, subs_lang, subs_urls = GetMPD(video_id)
    print('\nRipping:', output)
    #subprocess.run([ytdlp, '-k', '--user-agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/83.0.4103.61 Mobile/15E148 Safari/604.1', '-F', MPD])
    #time.sleep(1)

    Content = ""
    if '1' in Content:
        if not os.path.exists(FInput_audio) and not os.path.exists(out_Audio):
            subprocess.run([ytdlp, '-k', '--user-agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/83.0.4103.61 Mobile/15E148 Safari/604.1', '-f', "bestaudio", '--fixup', 'never', MPD, '-o', FInput_audio])
        else:
            pass
    else:
        try:
        
            if not os.path.exists(FInput_audio) and not os.path.exists(out_Audio):
                subprocess.run([ytdlp, '-k', '--user-agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/83.0.4103.61 Mobile/15E148 Safari/604.1', '-f bestaudio', '--fixup', 'never', MPD, '-o', FInput_audio])
            else:
                pass
        except Exception:
            pass

        if not os.path.exists(FInput_video) and not os.path.exists(out_Video):
            subprocess.run([ytdlp, '-k', '--user-agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/83.0.4103.61 Mobile/15E148 Safari/604.1', '-f', qual, '--fixup', 'never', MPD, '-o', FInput_video])
        else:
            pass

    for x in range(len(subs_lang)):
        subs_srt = f'{subs_lang[x]}.srt'
        if os.path.exists(subs_srt): os.remove(subs_srt)
        subprocess.run([ffmpegpath, '-loglevel', 'panic', '-i', subs_urls[x], subs_srt])

    if not os.path.exists(out_Video) or not os.path.exists(out_Audio):
        print('\nEnter Decryption Section...')
    KID = ''
    pssh = None
    def find_str(s, char):
            index = 0
            if char in s:
                c = char[0]
                for ch in s:
                    if ch == c and s[index:index + len(char)] == char:
                        return index
                    index += 1

            return -1
    mp4dump = dirPath + "/binaries/mp4dump.exe"
    mp4dump = subprocess.Popen([mp4dump, FInput_audio], stdout=subprocess.PIPE)
    mp4dump = str(mp4dump.stdout.read())
    A = find_str(mp4dump, 'default_KID')
    KID = mp4dump[A:A + 63].replace('default_KID = ', '').replace('[', '').replace(']', '').replace(' ', '')
    KID = KID.upper()
    KID_video = KID[0:8] + '-' + KID[8:12] + '-' + KID[12:16] + '-' + KID[16:20] + '-' + KID[20:32]
    # print('KID:{}'.format(KID_video))
    if KID == '':
        KID = 'nothing'


    pssh = re.findall(r'<cenc:pssh>(.*?)</cenc:pssh>', requests.get(MPD).text)[1]
    # print(pssh)

    license_headers = {
        'customdata': GetMPD(video_id, True)
    }

    def do_decrypt(pssh, licurl):
        wvdecrypt = WvDecrypt(pssh)
        chal = wvdecrypt.get_challenge()
        resp = requests.post(url=licurl,data = chal,headers=license_headers)
        license_decoded = resp.content
        license_b64 = base64.b64encode(license_decoded)
        wvdecrypt.update_license(license_b64)
        keys = wvdecrypt.start_process()

        return keys

    def keysOnly(keys):
        for key in keys:
            if key.type == 'CONTENT':
                key = ('{}:{}'.format(key.kid.hex(), key.key.hex()))
                print(key)
    if not os.path.exists(out_Video) or not os.path.exists(out_Audio):
        print('\nGetting Keys...\n')
        KEYS = do_decrypt(pssh=pssh, licurl=licurl)
        keysOnly(KEYS)

    if args.keys:
        exit()

    def proper(keys):
        commandline = [mp4decryptexe]
        for key in keys:
            if key.type == 'CONTENT':
                commandline.append('--key')
                commandline.append('{}:{}'.format(key.kid.hex(), key.key.hex()))

        return commandline

    def decrypt(keys_, inputt, output):
        Commmand = proper(keys_)
        Commmand.append(inputt)
        Commmand.append(output)

        wvdecrypt_process = subprocess.Popen(Commmand)
        stdoutdata, stderrdata = wvdecrypt_process.communicate()
        wvdecrypt_process.wait()

        return

    def keysOnly(keys):
        for key in keys:
            if key.type == 'CONTENT':
                key = ('{}:{}'.format(key.kid.hex(), key.key.hex()))
        return key

    try:
        if not os.path.exists(out_Video):
            print("\nDecrypting Video...")
            print ("Using KEY: " + keysOnly(KEYS))
            command = decrypt(KEYS, FInput_video, out_Video)
            print('Done!')
    except Exception:
        pass

    if not os.path.exists(out_Audio):
        print("\nDecrypting Audio...")
        print ("Using KEY: " + keysOnly(KEYS))
        command = decrypt(KEYS, FInput_audio, out_Audio)
        print('Done!')

    try:
        if os.path.exists(out_Video) and not os.path.exists(Remuxed_Video):
            print("\nRemuxing video...")
            ff = ffmpy.FFmpeg(executable=ffmpegpath, inputs={out_Video: None}, outputs={Remuxed_Video: '-c copy -metadata title="TheDNK" -metadata:s:v:0 language=eng -metadata:s:v:0 title="TheDNK" '}, global_options="-y -hide_banner -loglevel warning")
            ff.run()
            time.sleep (50.0/1000.0)
            print('Done!')
    except Exception:
        pass

    if os.path.exists(out_Audio) and not os.path.exists(Demuxed_Audio):
        print("\nDemuxing audio...")
        ff = ffmpy.FFmpeg(executable=ffmpegpath, inputs={out_Audio: None}, outputs={Demuxed_Audio: '-c copy -metadata:s:a:0 language=tel -metadata:s:a:0 title="TheDNK" '}, global_options="-y -hide_banner -loglevel warning")
        ff.run()
        time.sleep (50.0/1000.0)
        print('Done!')
    
    vid_mi = MediaInfo.parse(Remuxed_Video)
    vid_height = vid_mi.video_tracks[0].height
    vid_format = vid_mi.video_tracks[0].format
    if vid_height > 1440 and vid_height <= 2160: resoln = "2160p"
    elif vid_height > 1080 and vid_height <= 1440: resoln = "1440p"
    elif vid_height > 720 and vid_height <= 1080: resoln = "1080p"
    elif vid_height > 576 and vid_height <= 720: resoln = "720p"
    elif vid_height > 480 and vid_height <= 576: resoln = "576p"
    elif vid_height > 360 and vid_height <= 480: resoln = "480p"
    elif vid_height > 240 and vid_height <= 360: resoln = "360p"
    elif vid_height > 144 and vid_height <= 240: resoln = "240p"                
    else: resoln = "144p"
    
    output += f".{resoln}.ZEE5.WEB-DL.{vid_format}.BTSPROHD.COM.mkv" 
    
    try:
        print('\nMuxing Video and Audio...')
        mkvmerge_command = [mkvmergeexe, '-q', '--ui-language' ,'en', '--output', output, '--language', '0:und', '--default-track', '0:yes', '--compression', '0:none', Remuxed_Video, '--language', '0:und', '--default-track', '0:yes', '--compression' ,'0:none', Demuxed_Audio,'--language', '0:und','--track-order', '0:0,1:0,2:0,3:0,4:0']
        
        #for i in range(len(subs_lang)):
            #mkvmerge_command.append("--language")
            #mkvmerge_command.append(f"0:{subs_lang[i]}")
            #mkvmerge_command.append(f"{dirPath}/{subs_lang[i]}.srt")
        subprocess.run(mkvmerge_command)
    except Exception:
        pass
      
    if '1' in Content:
        print('Cleaning Directory...')
        os.remove(FInput_audio)
        os.remove(out_Audio)
        print('Done!!')
    else:    
        print('Cleaning Directory...')
        if os.path.exists(output):
            os.remove(out_Audio)
            os.remove(out_Video)
            #for i in range(len(subs_lang)):
                #os.remove(f"{dirPath}/{subs_lang[i]}.srt")
            os.remove(Demuxed_Audio)
            os.remove(Remuxed_Video)       
            os.remove(FInput_audio)
            os.remove(FInput_video)
            print('Done!')
        else:
            pass


url = input('\nEnter URL: ')
ThisIsTheWay = url.split('?')[0].split('/')[-1]
hmm = input('\nEnter 1 if url is web-series, or anything else if movie or episode: ')
qual = input("Press 1 for 1080p, 2 for 720p,....: ")
# 1 is highest qual available, if 1080p fails to exist qual fallbacks to 720p, no qual selection for audio
if "1" not in hmm:
    print("Ripping Only 1 Video....")
    RipIt(ThisIsTheWay,qual)
else:
    resp = requests.get(url = f"https://gwapi.zee5.com/content/tvshow/{ThisIsTheWay}?translation=en&country=IN").json()["seasons"][0]['episodes']
    print(f'Downloading {len(resp)} episodes from series....')
    for x in range(0, len(resp)):
        RipIt(resp[x]['id'],qual)
