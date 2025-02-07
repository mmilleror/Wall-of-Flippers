
# bluepy library (https://github.com/IanHarvey/bluepy/blob/master/README.md)

#   What is Wall of Flippers? 
#   Wall of Flippers (WoF) is a Python based project designed for Bluetooth Low Energy (BTLE) exploration. 
#   Its primary functionality involves the discovery of the Flipper Zero and the identification of potential BTLE based attacks


#  How to use?
#       1. Install libglib2.0-dev (sudo apt-get install python-pip libglib2.0-dev) 
#       2. Install bluepy (sudo pip install bluepy)
#       3. Run the script (sudo python WallofFlippers.py)




import os,time,json,random
from bluepy.btle import Scanner


dolphin_thinking = [
    'Let\'s hunt some flippers', 
    "uWu, I see a flipper nearby!", 
    "I have been deployed owo", 
    "Ya'll like war driving flippers?", 
    "I was made with love and care",
    "Please stop annoying people with your flipper...",
    "Script kiddie detector 9000",
    "This video is sponsored by PCBWay!!!",
    "I'm a flipper, you're a flipper, we're all flippers!",
    "Please refrain from annoying people with your flipper...",
    "My VIBRO Motor go brrrrrzz5rzrrz",
    "Fun fact: Astro is a synesthesiac moon deer 🤯",
    "Flipper Zero : Advanced Warefare",
    "Why does my flipper make a ticking noise with the RGB Mod??!?!",
    "Stop committing 'war crimes' with your flipper",
    "Don't be a skid!!!!!!",
    "yo put a lily quote in there - lily",
    "discord.gg/squachtopia",
    "Hack the planet!",
    "I look really intimidating!"
]
ascii = open('ascii.txt', 'r').read()




wof_data = { # I just hold important data
    "found_flippers": [], # (IGNORE)
    "data_baseFlippers": [], # (IGNORE)
    "live_flippers": [], # (IGNORE)
    "display_live": [], # (IGNORE)
    "display_offline": [], # (IGNORE)
    "max_online": 30, # Max online devices to display
    "max_offline": 30, # Max offline devices to display
    "bool_scanning": False, # (IGNORE)
    "forbidden_packets_found": [], # (IGNORE)
    "forbidden_packets": [ # You can add your own packet detection here (optional)
        {"PCK": "4c000f05c_________000010______", "TYPE": "BLE_APPLE_IOS_CRASH_LONG"},
        {"PCK": "4c000719010_2055__________________________________________", "TYPE": "BLE_APPLE_DEVICE_POPUP_CLOSE"},
        {"PCK": "4c000f05c00_______", "TYPE": "BLE_APPLE_ACTION_MODAL_LONG"},
        {"PCK": "2cfe______", "TYPE": "BLE_ANDROID_DEVICE_CONNECT"},
        {"PCK": "750042098102141503210109____01__063c948e00000000c700", "TYPE": "BLE_SAMSUNG_BUDS_POPUP_LONG"},
        {"PCK": "7500010002000101ff000043__", "TYPE": "BLE_SAMSUNG_WATCH_PAIR_LONG"},
        {"PCK": "0600030080________________________", "TYPE": "BLE_WINDOWS_SWIFT_PAIR_SHORT"},
        {"PCK": "ff006db643ce97fe427_______", "TYPE": "BLE_LOVE_TOYS_SHORT_DISTANCE"},
    ]                                                  
}





class FlipperUtils:
    def __asciiArt__():
        print(ascii.replace("[RANDOM_QUOTE]", random.choice(dolphin_thinking)))
    def __convertHowLongAgo__(timey):
        currentTime = int(time.time())
        timeAgo = currentTime - timey
        minutes = str(timeAgo // 60) + "m"
        seconds = str(timeAgo % 60) + "s"
        return f"{(minutes)} {(seconds)}"
    def __logFlipper__(name, data): 
        db = open('Flipper.json', 'r')
        file_data = json.load(db)
        for flipper in file_data:
             if flipper['MAC'] == data['MAC']:
                flipper['Time Last Seen'] = data['Time Last Seen']
                flipper['RSSI'] = data['RSSI']
                flipper['Detection Type'] = data['Detection Type']
                flipper['unixLastSeen'] = data['unixLastSeen']
                flipper['Spoofing'] = data['Spoofing']
                with open('Flipper.json', 'w') as f:
                    json.dump(file_data, f, indent=4)
                db.close()
                return
        file_data.append(data)
        with open('Flipper.json', 'w') as f:
               json.dump(file_data, f, indent=4)
        db.close()
    def __fancyDisplay__():
        global wof_data
        db = open('Flipper.json', 'r')
        file_data = json.load(db)
        for flipper in file_data:
            wof_data['data_baseFlippers'].append(flipper)
        db.close()
        allign_center = 8
        for flipper in wof_data['data_baseFlippers']:
            flipper['Name'] = flipper['Name'].replace("Flipper ", "")
            if len(flipper['Name']) > 15:
                flipper['Name'] = flipper['Name'][:15]
            if flipper['MAC'] in wof_data['live_flippers']:
                wof_data['display_live'].append(flipper)
            else:
                wof_data['display_offline'].append(flipper)
        totalLive = 0
        totalOffline = 0
        os.system("clear || cls")
        FlipperUtils.__asciiArt__()
        print(f"Total Online...: {len(wof_data['display_live'])}")
        print(f"Total Offline..: {len(wof_data['display_offline'])}\n\n")
        total_ble = 0
        if (len(wof_data['forbidden_packets_found']) > 0):
            print(f"[NAME]\t\t\t\t\t[ADDR]\t\t   [PACKET]")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            for packet in wof_data['forbidden_packets_found']:
                total_ble = total_ble + 1
                if (total_ble <= 10):
                    name = packet['Type']
                    mac = packet['MAC']
                    pkt = packet['PCK']
                    print(  
                        name.ljust(allign_center) + 
                          "\t\t" +  
                        mac.ljust(allign_center) + "  " + 
                        pkt.ljust(allign_center)
                    )
        if (len(wof_data['forbidden_packets_found']) > 25):
            print(f"━━━━━━━━━━━━━━━━━━ Bluetooth Low Energy (BLE) Attacks Detected ({len(wof_data['forbidden_packets_found'])}+ Packets) ━━━━━━━━━━━━━━━━━━━━")
        print(f"\n\n[FLIPPER]".ljust(8)
            + "\t" +
            "[ADDR]".ljust(8)
            + "\t\t" +
            "[FIRST]".ljust(8)
            + "\t" +
            "[LAST]".ljust(8)
            + "\t" +
            "[RSSI]".ljust(8)
            + "\t" +
            "[SPOOFING]".ljust(8)
        )
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        if (len(wof_data['display_live']) > 0):
            print("(ONLINE DEVICES)".center(100))
            for flipper in wof_data['display_live']:
                totalLive += 1
                if totalLive < wof_data['max_online']:
                    print(  
                        flipper['Name'].ljust(8)
                        + "\t" + 
                        flipper['MAC']
                        + "\t" + 
                        str(FlipperUtils.__convertHowLongAgo__(flipper['unixFirstSeen'])).ljust(8) 
                        + "\t" + 
                        str(FlipperUtils.__convertHowLongAgo__(flipper['unixLastSeen'])).ljust(8) 
                        + "\t" + 
                        str((flipper['RSSI'])) +"".ljust(8) 
                        + "\t" + 
                        str(flipper['Spoofing']).ljust(8) 
                    )
                if totalLive == wof_data['max_online'] - 1:
                    totalLiveStr = len(wof_data['display_live']) - wof_data['max_online']
                    print(f"Too many <online> devices to display. ({totalLiveStr} devices)".center(100))
                    break
        if (len(wof_data['display_offline']) > 0):
            # reorganize to show the unix last seen first
            wof_data['display_offline'] = sorted(wof_data['display_offline'], key=lambda k: k['unixLastSeen'], reverse=True)
            print("(OFFLINE DEVICES)".center(100))
            for flipper in wof_data['display_offline']:
                totalOffline += 1
                if totalOffline < wof_data['max_offline']:
                    print( 
                        flipper['Name'].ljust(8)
                        + "\t" + 
                        flipper['MAC']
                        + "\t" + 
                        str(FlipperUtils.__convertHowLongAgo__(flipper['unixFirstSeen'])).ljust(8) 
                        + "\t" + 
                        str(FlipperUtils.__convertHowLongAgo__(flipper['unixLastSeen'])).ljust(8)
                        + "\t" + 
                        "-".ljust(8)
                        + "\t" + 
                        str(flipper['Spoofing']).ljust(8)
                    )
                if totalOffline == wof_data['max_offline'] - 1:
                    totalOfflineStr = len(wof_data['display_offline'])  - wof_data['max_offline']
                    print(f" Too many <offline> devices to display. ({totalOfflineStr} devices)".center(100))
                    break
        wof_data['display_live'] = []
        wof_data['display_offline'] = []
        wof_data['live_flippers'] = []
        wof_data['forbidden_packets_found'] = []

class FlipDetection:
    def __scan__():
        try:
            scanner = Scanner()
            wof_data['bool_scanning'] = True
            devices = scanner.scan(5)
            for dev in devices:
                for (adtype, desc, value) in dev.getScanData():
                    string1 = value
                    string2 = ""
                    packet_listing = wof_data['forbidden_packets']
                    for packet in packet_listing:
                        similar = True
                        packet_encoded = packet['PCK']
                        packet_type = packet['TYPE']
                        string2 = packet_encoded
                        total_underscores = string2.count("_")
                        total_found = 0
                        for char1, char2 in zip(string1, string2):
                            if char2 != '_' and char1 != char2:
                                similar = False
                            if (char1 == char2):
                                total_found += 1
                        if (similar == True):
                            get_non_underscore_chars = len(string2) - total_underscores
                            if (total_found == get_non_underscore_chars):
                                wof_data['forbidden_packets_found'].append({"MAC": dev.addr, "PCK": string1, "Type": packet_type})
                    if (desc == "Complete Local Name"):
                        if ("Flipper") in value:
                            record_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                            random_flipper_name = value
                            flipper_full_name = random_flipper_name
                            flipper_rssi = dev.rssi
                            flipper_mac = dev.addr
                            for flipper in wof_data['found_flippers']: 
                                if flipper['MAC'] == flipper_mac: wof_data['found_flippers'].remove(flipper)
                            arrTemp = {"Name": str(flipper_full_name),"MAC": str(flipper_mac),"RSSI": str(flipper_rssi) + "","Detection Type": "Flipper","Spoofing": False,"Time Last Seen": str(record_time),"Time First Seen": str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),"unixFirstSeen": int(time.time()),"unixLastSeen": int(time.time()),"isFlipper": True}
                            allowFlipperProxy = True
                            for flipper in wof_data['found_flippers']:
                                if flipper['MAC'] == flipper_mac: allowFlipperProxy = False
                            if allowFlipperProxy:
                                wof_data['live_flippers'].append(str(flipper_mac))
                                wof_data['found_flippers'].append(arrTemp)
                                FlipperUtils.__logFlipper__(flipper_full_name,arrTemp)     
                        elif ("80:e1:26" or "80:e1:27") in dev.addr:
                                record_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                random_flipper_name = value
                                flipper_full_name = random_flipper_name
                                flipper_rssi = dev.rssi
                                flipper_mac = dev.addr
                                for flipper in wof_data['found_flippers']: 
                                    if flipper['MAC'] == flipper_mac: wof_data['found_flippers'].remove(flipper)
                                arrTemp = {"Name": str(flipper_full_name),"MAC": str(flipper_mac),"RSSI": str(flipper_rssi) + "","Detection Type": "Flipper","Spoofing": True,"Time Last Seen": str(record_time),"Time First Seen": str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),"unixFirstSeen": int(time.time()),"unixLastSeen": int(time.time()),"isFlipper": True}
                                allowFlipperProxy = True
                                for flipper in wof_data['found_flippers']:
                                    if flipper['MAC'] == flipper_mac: allowFlipperProxy = False
                                if allowFlipperProxy == True:
                                    wof_data['live_flippers'].append(str(flipper_mac))
                                    wof_data['found_flippers'].append(arrTemp)
                                    FlipperUtils.__logFlipper__(flipper_full_name,arrTemp)  
            wof_data['bool_scanning'] = False
        except (RuntimeError, TypeError, NameError) as e:
                print("[!] NoFlip >> Encountered an error while scanning for devices. Error: " + str(e))
                wof_data['bool_scanning'] == False
if __name__ == '__main__':
    os.system("clear || cls")
    get_os = os.name
    get_root = os.getuid()
    if (get_os != "posix"):
        print("[!] NoFlip >> WoF is not supported on Windows.\n\t      Reason: Dependency on bluepy library.")
        exit()
    if (get_root != 0):
        print("[!] NoFlip >> WoF requires root privileges to run.\n\t      Reason: Dependency on bluepy library.")
        exit()
    while True:
        if (wof_data['bool_scanning'] == False):
            wof_data['data_baseFlippers'] = []
            FlipperUtils.__fancyDisplay__()
            FlipDetection.__scan__()
        time.sleep(0.1)
