import random
import shutil
import time
import colorama

banner = """
                           ,--.             
                          {    }            
                          K,   }            
                         /  Y             
                    _   /   /               
                   {_'-K.__/                
                     /-.__L._              
                     /  ' /\_}             
                    /  ' /     
            ____   /  ' /                   
     ,-'~~~~    ~~/  ' /_                   
   ,'             `~~~%%',                 
  (                     %  Y                
 {                      %% I                
{      -                 %  .              
|       ',                %  )              
|        |   ,..__      __. Y               
|    .,_./  Y ' / ^Y   J   )|               
\           |' /   |   |   ||               
 \          L_/    . _ (_,.'(               
  \,   ,      ^^""' / |      )              
    \_  \          /,L]     /               
      '-_-,           ./                
         -(_            )                  
             ^^\..___,.--    
                            "𝙏𝙤 𝙬𝙞𝙣 𝙖𝙣𝙮 𝙗𝙖𝙩𝙩𝙡𝙚, 𝙮𝙤𝙪 𝙢𝙪𝙨𝙩 𝙛𝙞𝙜𝙝𝙩 𝙖𝙨 𝙞𝙛 𝙮𝙤𝙪 𝙖𝙧𝙚 𝙖𝙡𝙧𝙚𝙖𝙙𝙮 𝙙𝙚𝙖𝙙"
 __           __   _____                            _   _                        _        _     _ _     _              _ 
 \ \    _    / /  / ____|                          | | (_)                 
  \ \ _| |_ / /  | |     ___  _ __  _ __   ___  ___| |_ _  ___  _ __     
   > >_   _< <   | |    / _ \| '_ \| '_ \ / _ \/ __| __| |/ _ \| '_ \   
  / /  |_|  \ \  | |____ (_) | | | | | | |  __/ (__| |_| | (_) | | | |  
 /_/         \_\  \_____\___/|_| |_|_| |_|\___|\___|\__|_|\___/|_| |_|  

                           | |      | |   | (_)   | |            | |
                   ___ ___| |_ __ _| |__ | |_ ___| |__   ___  __| |
                  / _ \ __| __/ _ | '_ \| | / __| '_ \ / _ \/ _ |
                 |  __\__ \ |_ (_| | |_) | | \__ \ | | |  __/ (_| |
                  \___|___/\__\__,_|_.__/|_|_|___/_| |_|\___|\__,_|
                                                                    "𝙗𝙮 𝙢𝙯𝙜"
                                                                                                                                                                        
        """


def show_banner():
    banners = [banner]
    show = random.choice(banners)
    print(show)


def center(text):
    terminal_width = shutil.get_terminal_size().columns
    centered_text = text.center(terminal_width)
    return centered_text

def red(message):
    print(colorama.Fore.RED + message + colorama.Style.RESET_ALL)


def yellow(message):
    print(colorama.Fore.YELLOW + message + colorama.Style.RESET_ALL)

def green(message):
    print(colorama.Fore.GREEN + message + colorama.Style.RESET_ALL)


