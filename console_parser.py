import keyboard
import time
import tkinter as tk

windX = 1080
windY = 720

console_list = []
status_list = [[], []]
killfeed = []
plrL = []

friend_list = ["[U:1:186034054]", # Kaputon
               "[U:1:16041424]", # CJ
               "[U:1:160707434]", # Vamvava
               "[U:1:1153449353]"# Andrew
               ]

# Friend's names are volatile, therefore, if the steamID matches a friend, put em in here.
friend_names = []

# Basic player blacklist to prevent STV maker from being  counted as a person.
blacklist = ["Use /call to report players"]

current_players = status_list[0]
prev_players = status_list[1]

# Weapon dict to formal name.
keyword_dict = {
    "sniperrifle.": "Sniper Rifle",
    "blackbox.": "The Black Box",
    "awper_hand.": "Awper Hand",
    "big_earner.": "Big Earner",
    "scattergun.": "Scattergun",
    "sydney_sleeper.": "Syndey Sleeper",
    "knife.": "Knife",
    "kunai.": "Connivers Kunai",
    "carved_cutter." : "Carved Cutter",
    "ambassador.": "Ambassador",
    "shotgun_primary.": "Shotgun",
    "sword.": "Eyelander",
    "tf_projectile_pipe_remote.": "Stickybomb Launcher",
    "sticky_resistance.": "Scottish Resistance",
    "iron_bomber.": "Iron Bomber",
    "quake_rl.": "The Original",
    "rocketlauncher_directhit.": "Direct Hit",
    "tf_projectile_pipe.": "Grenade Launcher",
    "tf_projectile_rocket.": "Rocket Launcher",
    "tf_projectile_arrow.": "Huntsman",
    "flaregun.": "Flaregun",
    "scorch_shot.": "Scorch Shot",
    "phlogistinator." : "Phlog",
    "revolver.": "Revolver",
    "diamondback.": "Diamondback",
    "obj_minisentry.": "Mini Sentry",
    "detonator.": "Detonator",
    "obj_sentrygun2.": "Sentry (Level 2)",
    "obj_sentrygun3.": "Sentry (Level 3)",
    "deflect_rocket.": "Reflected Rocket",
    "panic_attack.": "Panic Attack",
    "team #1": "Blu Team",
    "team #2": "Red Team"}


def playerInList(plr):
    for lst in status_list[0]:
        if lst[0] == plr:
            return True
    return False


def returnTween(li, char):
    return [i for i, ch in enumerate(li) if ch == char]


def updateChatLog(message):
    if len(console_list) > 10:
        console_list.pop(9)
    console_list.insert(0, message)


def updateKillFeed(message):
    if len(killfeed) > 10:
        killfeed.pop(9)
    killfeed.insert(0, message)

# Detect if a player in the game is in the submitted list.
def determineLine(lst):
    for plr in plrL:
        if plr in lst:
            return True
    return False


def formalizeWeapons(lst):
    for ind, ch in enumerate(lst):
        try:
            lst[ind] = (keyword_dict[ch] or keyword_dict[ch][:-1])
        except:
            pass
    line = " ".join(lst)
    if not line[len(line)-1] == ".":
        line = line+"."
    return line

def friendParser(line):
    for friend in friend_names:
        if friend in line:
            return True
        else:
            return False

def parse(line):
    if not line in console_list:
        chars = line.split(" ")

        if len(chars) > 0:
            # The first character in all status posts is a pound sign.
            if chars[0] == "#" and not (chars[1] == "userid"):
                quotes = returnTween(line, '"')
                plr = line[quotes[0] + 1: quotes[1]]
                try:
                    steamID = line[line.index("["): line.index("]") + 1].strip()
                except:
                    steamID = "NaN"
                if not playerInList(plr) and not plr in blacklist:
                    current_players.append([plr, steamID])
                    plrL.append(plr)

            # Otherwise, determine if a player is mentioned in this line. If so, replace any weapon names with formal ones,
            # and send it to the console list.
            elif determineLine(chars) and (":" in chars):
                updateChatLog(line)
            elif "killed" in chars:
                line = formalizeWeapons(chars)
                updateKillFeed(line)


def tf_gamestate():
    console_file = 'C:\\Program Files (x86)\\Steam\\SteamApps\\common\\Team Fortress 2\\tf\\console.log'
    console = open(console_file, 'rb')

    #### Setup TKinter GUI
    frame = tk.Frame(master=window, relief=tk.SUNKEN, borderwidth=5, bg="black")
    frame2 = tk.Frame(master=window, relief=tk.GROOVE, borderwidth=5, bg="black")
    frame3 = tk.Frame(master=window, relief=tk.GROOVE, borderwidth=5, bg="black")
    frame.grid(row=0, column=0)
    frame2.grid(row=1, column=0)
    frame3.grid(row=0, column=1)

    for lab in range(24):
        label = tk.Label(master=frame, text=f"{lab + 1}. ", relief=tk.GROOVE,
                         borderwidth=2, width=int(windX / 20))
        label.pack()

    for _ in range(10):
        label = tk.Label(master=frame2, text=f"", relief=tk.GROOVE, borderwidth=2, width=int(windX / 20))
        label.pack()

    for _ in range(10):
        label = tk.Label(master=frame3, text=f"", relief=tk.GROOVE, borderwidth=2, width=int(windX / 20))
        label.pack()
    ####

    begin = time.time()
    end = time.time()

    while True:
        # If 10 seconds have passed, press HOME button to trigger "status" bind in TF2
        if abs(begin - end) > 10:
            keyboard.send("f10")
            begin = end

        # Hand 20 console lines to the parse function
        lines = console.readlines()[-60:]
        for line in lines:
            parse(str(line)[2:-5])  # remember [2:]

        # Set the current leaderboard to previous
        prev_players = current_players

        # If there are players, begin filling the GUI with their name and steamID.
        if len(status_list) > 0:
            plr = 0
            for ind, wid in enumerate(frame.winfo_children()):
                try:
                    wid.config(bg="white")
                    if prev_players[ind][1] in friend_list:
                        wid.config(bg="green")
                        if not prev_players[ind][0] in friend_names:
                            friend_names.append(prev_players[ind][0])
                    wid.config(text=f"{ind + 1}. '{prev_players[ind][0]}' ; {prev_players[ind][1]}")
                except:
                    pass
            current_players.clear()

        # If console messages exist, fill the GUI with them.
        if len(console_list) > 0:
            con = 0
            for ind, wid in enumerate(frame2.winfo_children()):
                try:
                    wid.config(bg="white")
                    if friendParser(console_list[ind]) == True:
                        wid.config(bg="green")
                    wid.config(text=f"{console_list[ind]}")
                except:
                    pass

        if len(killfeed) > 0:
            for ind, wid in enumerate(frame3.winfo_children()):
                try:
                    wid.config(bg="white")
                    if friendParser(killfeed[ind]) == True:
                        wid.config(bg="green")
                    wid.config(text=f"{killfeed[ind]}")
                except:
                    pass

        window.update()
        end = time.time()

    console.close()


window = tk.Tk()
window.minsize(windX, windY)

tf_gamestate()
