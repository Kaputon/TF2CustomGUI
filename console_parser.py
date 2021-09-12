import keyboard
import time
import tkinter as tk

begin = 0
end = 0

console_list = []
status_list = [[], []]
plrL = []

current_players = status_list[0]
prev_players = status_list[1]

keyword_dict = {
                    "sniperrifle." : "Sniper Rifle",
                    "blackbox" : "The Black Box",
                    "awper_hand." : "Awper Hand.",
                    "big_earner." : "Big Earner.",
                    "scattergun." : "Scattergun",
                    "sydney_sleeper." : "Syndey Sleeper",
                    "knife." : "Knife",
                    "kunai." : "Connivers Kunai",
                    "ambassador." : "Ambassador",
                    "shotgun_primary." : "Shotgun",
                    "sword." : "Eyelander",
                    "tf_projectile_pipe_remote." : "Stickybomb Launcher",
                    "sticky_resistance" : "Scottish Resistance",
                    "iron_bomber." : "Iron Bomber",
                    "quake_rl." : "The Original",
                    "rocketlauncher_directhit" : "Direct Hit",
                    "tf_projectile_pipe." : "Grenade Launcher",
                    "tf_projectile_rocket." : "Rocket Launcher",
                    "tf_projectile_arrow." : "Huntsman",
                    "flaregun." : "Flaregun",
                    "revolver." : "Revolver",
                    "diamondback." : "Diamondback",
                    "obj_minisentry." : "Mini Sentry",
                    "detonator" : "Detonator",
                    "obj_sentrygun2" : "Sentry (Level 2)",
                    "obj_sentrygun3" : "Sentry (Level 3)",
                    "deflect_rocket." : "Reflected Rocket",
                    "panic_attack" : "Panic Attack",
                    "team #1" : "Blu Team",
                    "team #2" : "Red Team"}

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


def determineLine(lst):
    for plr in plrL:
        if plr in lst:
            return True
    return False


def parse(line):
    if not line in console_list:
        chars = line.split(" ")
        if chars[0] == "#" and not (chars[1] == "userid"):
            quotes = returnTween(line, '"')
            plr = line[quotes[0] + 1: quotes[1]]
            try:
                steamID = line[line.index("["): line.index("]") + 1]
            except:
                steamID = "NaN"
            if not playerInList(plr):
                current_players.append([plr, steamID])
                plrL.append(plr)
        elif determineLine(chars):
            for ind, ch in enumerate(chars):
                try:
                    chars[ind] = keyword_dict[ch]
                except:
                    pass
            line = " ".join(chars)
            updateChatLog(line)


def tf_gamestate():
    console_file = 'C:\\Program Files (x86)\\Steam\\SteamApps\\common\\Team Fortress 2\\tf\\console.log'
    console = open(console_file, 'rb')

    frame = tk.Frame(master=window, relief=tk.SUNKEN, borderwidth=5)
    frame2 = tk.Frame(master=window, relief=tk.GROOVE, borderwidth=5)
    frame.grid(row=0, column=0)
    frame2.grid(row=1, column=0)

    for lab in range(24):
        label = tk.Label(master=frame, text=f"{lab + 1}. ", relief=tk.GROOVE,
                         borderwidth=2)
        label.pack(fill=tk.BOTH)
    for lab in range(10):
        label = tk.Label(master=frame2, text=f"", relief=tk.GROOVE, borderwidth=2)
        label.pack(fill=tk.BOTH)

    begin = time.time()
    end = time.time()
    while True:
        if abs(begin - end) > 10:
            keyboard.send("f10")
            begin = end

        if len(console_list) > 20:
            excess = len(console_list) - 20
            for i in range(excess):
                console_list.pop(i)

        lines = console.readlines()[-20:]
        for line in lines:
            parse(str(line)[2:-5])  # remember [2:]

        prev_players = current_players

        if len(status_list) > 0:
            plr = 0
            for wid in frame.winfo_children():
                try:
                    wid.config(text=f"{plr + 1}. {prev_players[plr]}")
                    plr += 1
                except:
                    pass
            current_players.clear()

        if len(console_list) > 0:
            con = 0
            for wid in frame2.winfo_children():
                try:
                    wid.config(text=f"{console_list[con]}")
                    con += 1
                except:
                    pass

        window.update()
        end = time.time()

    # console.close()


window = tk.Tk()
window.size()

tf_gamestate()
