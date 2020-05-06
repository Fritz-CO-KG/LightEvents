#!/usr/bin/python
# -*- coding: iso-8859-15 -*-


# Import
import json
import threading
from org.bukkit.boss import BossBar
from net.md_5.bungee.api import ChatMessageType
from net.md_5.bungee.api import ChatColor as BungeeChatColor
from net.md_5.bungee.api.chat import TextComponent
from sys import path
from time import sleep
from random import randint
from org.bukkit import Bukkit
from org.bukkit import ChatColor
from org.bukkit import GameMode
from org.bukkit import Location
from org.bukkit import Material
from org.bukkit import Sound
from org.bukkit import SoundCategory
from org.bukkit import GameRule
from org.bukkit.boss import BarColor
from org.bukkit.boss import BarStyle
from org.bukkit.enchantments import Enchantment
from org.bukkit.event import EventPriority
from org.bukkit.event.entity import EntityDamageEvent
from org.bukkit.event.player import PlayerQuitEvent
from org.bukkit.event.player import PlayerRespawnEvent
from org.bukkit.event.entity import FoodLevelChangeEvent
from org.bukkit.event.entity import PlayerDeathEvent
from org.bukkit.event.inventory import InventoryClickEvent
from org.bukkit.event.inventory import InventoryType
from org.bukkit.event.player import PlayerDropItemEvent
from org.bukkit.event.player import PlayerInteractEvent
from org.bukkit.event.player import PlayerJoinEvent
from org.bukkit.event.player import PlayerMoveEvent
from org.bukkit.event.player import PlayerPickupItemEvent
from org.bukkit.entity import EntityType
from org.bukkit.inventory import ItemStack
from org.bukkit.event.inventory import CraftItemEvent
from org.bukkit.scoreboard import DisplaySlot
from org.bukkit.scoreboard import Objective
from org.bukkit.scoreboard import Scoreboard
from org.bukkit.scoreboard import ScoreboardManager


# Variables

DEBUG = True
PREFIX = "&bBingo&6 > "
JSON_DIR = "/home/fritz/jsons/"
HELPALIASES = ["help", "?", "|"]
STAGE = "setup"
firstplayer = True
spawnX = None
spawnY = None
spawnZ = None
path.append(JSON_DIR)
spawn = None
diablock = None
stopmanager = False
diablock = False
diatypebefore = False
presets = {
    "0": {
        "0": "minecraft:barrier",
        "1": "minecraft:barrier",
        "2": "minecraft:barrier",
        "3": "minecraft:barrier",
        "4": "minecraft:barrier",
        "5": "minecraft:barrier",
        "6": "minecraft:barrier",
        "7": "minecraft:barrier",
        "8": "minecraft:barrier",
        "9": "minecraft:barrier"
    }}
diatypebefore = False
# big

# Inventories
# Items
# nothing
NOTHING = ItemStack(Material.GRAY_STAINED_GLASS_PANE, 1)
NOTHING_META = NOTHING.getItemMeta()
NOTHING_META.setDisplayName(" ")
NOTHING_META.setLore(["LightEvents"])
NOTHING.setItemMeta(NOTHING_META)
# bingochooseitems

# bingodict
create = False
bingo = {"spawn": False, "spawnblock": False, "spawnblock_before": False, "allowmove": True, "invclick": True, "kick": False, "admingui": True, "stage": "setup", "timer": {"timetotal": 0, "timerunning": {"sec": 0, "min": 0}}, "timetostart": 0,
         "preset": "0", "page": 0, "teamsize": 2, "join": False, "stage:": "setup",
         "pvp": {"enabled": False, "after": 0}, "timerestart": 90}
teams = {"&e&lTeam 1": [], "&e&lTeam 2": [], "&e&lTeam 3": [], "&e&lTeam 4": []}
teamscompleted = {"&e&lTeam 1": [], "&e&lTeam 2": [], "&e&lTeam 3": [], "&e&lTeam 4": []}
randomcode = False
stopstarter = False
tocollect = []
playerinvs = []
# Listeners

class QuitListener(PythonListener):
    @PythonEventHandler(PlayerQuitEvent, EventPriority.NORMAL)
    def onPlayerQuit(self, event):
        global teams
        name = event.getPlayer().getDisplayName()
        if bingo["stage"] != "playing":
            for team in teams:
                if name in teams[team]:
                    teams[team].remove(name)

class JoinListener(PythonListener):
    @PythonEventHandler(PlayerJoinEvent, EventPriority.NORMAL)
    def onPlayerJoin(self, event):
        global firstplayer
        global spawn
        global diablock
        global diatypebefore
        global teams

        # items
        JOIN_BED = ItemStack(Material.RED_BED, 1)
        JOIN_BED_META = JOIN_BED.getItemMeta()
        JOIN_BED_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&6&lTeams"))
        JOIN_BED_META.setLore(["o(teamsgui)", "LightEvents"])
        JOIN_BED.setItemMeta(JOIN_BED_META)

        # inv
        joininv = Bukkit.createInventory(None, InventoryType.PLAYER, "teamschoose")
        joininv.setItem(4, JOIN_BED)

        targetplayer = event.getPlayer()
        playername = targetplayer.getDisplayName()
        PLAYERJOIN = PREFIX + "Welcome to the event, &a" + playername + "!"
        event.setJoinMessage(ChatColor.translateAlternateColorCodes("&", PLAYERJOIN))
        PLAYERJOINTITLE = "&2Welcome to the event!"
        PLAYERJOINSUBTITLE = "&eThe event will start soon!"
        targetplayer.sendTitle(ChatColor.translateAlternateColorCodes("&", PLAYERJOINTITLE),
                               ChatColor.translateAlternateColorCodes("&", PLAYERJOINSUBTITLE), 15, 100, 15)
        targetplayer.setGameMode(GameMode.ADVENTURE)
        targetplayer.playSound(targetplayer.getLocation(), Sound.ENTITY_PLAYER_LEVELUP, SoundCategory.MASTER,
                               float(1.0), float(1))
        targetplayer.setFoodLevel(100)
        targetplayer.setHealthScale(18.0)
        pinv = targetplayer.getInventory()
        pinv.clear()
        pinv.setContents(joininv.getContents())
        if bingo["kick"] == True:
            KICKMSG = "&cSorry, you can't join yet! Please try again in &e&l" + str(bingo["timetostart"]) + " &cseconds."
            targetplayer.kickPlayer(ChatColor.translateAlternateColorCodes("&", KICKMSG))
        if spawn is not None:
            targetplayer.teleport(spawn)
        if firstplayer:
            firstplayer = False
            spawn = targetplayer.getLocation()
            border = spawn.getWorld().getWorldBorder()
            border.setCenter(spawn)
            border.setSize(15, 0)
            ploc = targetplayer.getLocation()
            pworld = targetplayer.getWorld()
            diablock = pworld.getBlockAt(Location(ploc.getWorld(), ploc.getX(), ploc.getY() - 1, ploc.getZ()))
            bingo["spawn"] = spawn
            bingo["spawnblock"] = diablock
            #diatypebefore = bingo["spawnblock"].getType()
            #bingo["spawnblock_before"] = diatypebefore
            bingo["spawnblock"].setType(Material.DRIED_KELP_BLOCK)

class PlayerDeath(PythonListener):
    @PythonEventHandler(PlayerDeathEvent, EventPriority.LOW)
    def onDeath(self, event):
        global teams
        global playerinvs
        if event.getEntityType() == EntityType.PLAYER:
            player = event.getEntity()
            pname = player.getDisplayName()
            for team in teams:
                if pname in teams[team]:
                    teamname = team
            PDEATH = PREFIX + "&5Respawning &6" + str(pname) + " (" + teamname + "&6)..."
            event.setDeathMessage(ChatColor.translateAlternateColorCodes("&", PDEATH))


class FoodListener(PythonListener):
    @PythonEventHandler(FoodLevelChangeEvent, EventPriority.LOWEST)
    def onFoodChange(self, event):
        global bingo
        stage = bingo["stage"]
        if stage == "setup" or stage == "hold_teams" or stage == "hold_admin" or stage == "countdown":
            event.setCancelled(True)

first = True
scoreboard_update = True
class MoveListener(PythonListener):
    @PythonEventHandler(PlayerMoveEvent, EventPriority.LOWEST)
    def onEvent(self, event):
        global first
        global bingo
        global checknow
        global scoreboard_update
        global teamscompleted
        if bingo["allowmove"] == False:
            event.setCancelled(True)
        if first == True:
            if bingo["stage"] == "playing":
                bingo["allowmove"] = True
                rawplayerlist = Bukkit.getOnlinePlayers()
                for player in rawplayerlist:
                    player.setGameMode(GameMode.SURVIVAL)
                    player.teleport(bingo["spawn"])
                    player.setFireTicks(0)
                Bukkit.dispatchCommand(Bukkit.getConsoleSender(), "recipe give @a *")
                event.getPlayer().getLocation().getWorld().setGameRule(GameRule.KEEP_INVENTORY, True)
                first = False
        if scoreboard_update == True:
            #Bukkit.broadcastMessage("check!")
            sm = Bukkit.getScoreboardManager()
            #Bukkit.broadcastMessage("scoreboard manager initialisized")
            board = sm.getNewScoreboard()
            #Bukkit.broadcastMessage("new scoreboard")
            score = board.registerNewObjective("aaa", "bbb")
            #Bukkit.broadcastMessage("displayname")
            score.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&6&lBingo"))
            score.setDisplaySlot(DisplaySlot.SIDEBAR)

            #Bukkit.broadcastMessage("ok bar created")

            stage = bingo["stage"]
            if stage == "setup" or stage == "hold_admin" or stage == "hold_teams" or stage == "countdown":
                #Bukkit.broadcastMessage("setup-countdown stages")
                score.getScore("  ").setScore(9)
                if bingo["timetostart"] == 0:
                    score.getScore(ChatColor.translateAlternateColorCodes("&", "&c&lWaiting...")).setScore(8)
                    score.getScore(ChatColor.translateAlternateColorCodes("&", "  ")).setScore(7)
                else:
                    score.getScore(ChatColor.translateAlternateColorCodes("&", "&2&lStarting in")).setScore(8)
                    score.getScore(ChatColor.translateAlternateColorCodes("&", "&b" + str(bingo["timetostart"]) + " &2sec.")).setScore(7)
                for player in Bukkit.getOnlinePlayers():
                    score.getScore(ChatColor.translateAlternateColorCodes("&", "  ")).setScore(6)
                    score.getScore(ChatColor.translateAlternateColorCodes("&", "&a&lYour Team:")).setScore(5)
                    noteam = False
                    for team in teams:
                        if event.getPlayer().getDisplayName() in teams[team]:
                            noteam = True
                            score.getScore(ChatColor.translateAlternateColorCodes("&", team)).setScore(4)
                    if noteam == False:
                        score.getScore(ChatColor.translateAlternateColorCodes("&", "&cNo team")).setScore(4)
                    score.getScore(ChatColor.translateAlternateColorCodes("&", "  ")).setScore(2)
                    score.getScore(ChatColor.translateAlternateColorCodes("&", "&2&lHosted by Quashi")).setScore(1)
                    player.setScoreboard(board)
            elif stage == "playing":
                score.getScore(ChatColor.translateAlternateColorCodes("&", "  ")).setScore(9)
                score.getScore(ChatColor.translateAlternateColorCodes("&", "&2&lTime elapsed:")).setScore(8)
                score.getScore(ChatColor.translateAlternateColorCodes("&", "&b" + str(bingo["timer"]["timerunning"]["min"]) + " &9min. &b" + str(bingo["timer"]["timerunning"]["sec"]) + " &9sec.")).setScore(7)
                score.getScore(ChatColor.translateAlternateColorCodes("&", "   ")).setScore(6)
                for player in Bukkit.getOnlinePlayers():
                    score.getScore(ChatColor.translateAlternateColorCodes("&", "&a&lYour Team:")).setScore(5)
                    noteam = False
                    max = 0
                    maxteam = "  "
                    for team in teams:
                        if event.getPlayer().getDisplayName() in teams[team]:
                            noteam = True
                            score.getScore(ChatColor.translateAlternateColorCodes("&", team)).setScore(4)
                        if max <= len(teamscompleted[team]):
                            maxteam = team
                    if noteam == False:
                        score.getScore(ChatColor.translateAlternateColorCodes("&", "&7Spectators")).setScore(4)
                    score.getScore(ChatColor.translateAlternateColorCodes("&", "  ")).setScore(3)
                    score.getScore(ChatColor.translateAlternateColorCodes("&", "&6Leading team:")).setScore(2)
                    score.getScore(ChatColor.translateAlternateColorCodes("&", maxteam)).setScore(1)
                    score.getScore(ChatColor.translateAlternateColorCodes("&", "&2&lHosted by Quashi")).setScore(0)
                    player.setScoreboard(board)
            elif stage == "end":
                score.getScore(ChatColor.translateAlternateColorCodes("&", "  ")).setScore(9)
                score.getScore(ChatColor.translateAlternateColorCodes("&", "&2&lTime until restart:")).setScore(8)
                score.getScore(ChatColor.translateAlternateColorCodes("&", "&b" + str(bingo["timerestart"]) + "&2 sec.")).setScore(7)
                score.getScore(ChatColor.translateAlternateColorCodes("&", "   ")).setScore(6)
                score.getScore(ChatColor.translateAlternateColorCodes("&", "&2&lTime played:")).setScore(5)
                score.getScore(ChatColor.translateAlternateColorCodes("&", "&b" + str(bingo["timer"]["timerunning"]["min"]) + " &9min. &b" + str(bingo["timer"]["timerunning"]["sec"]) + " &9sec.")).setScore(4)
                score.getScore(ChatColor.translateAlternateColorCodes("&", "    ")).setScore(3)
                for player in Bukkit.getOnlinePlayers():
                    score.getScore(ChatColor.translateAlternateColorCodes("&", "&6&lWinner Team:")).setScore(2)
                    max = 0
                    maxteam = "  "
                    for team in teams:
                        if max < len(teamscompleted[team]):
                            maxteam = team
                    score.getScore(ChatColor.translateAlternateColorCodes("&", maxteam)).setScore(1)
                    score.getScore(ChatColor.translateAlternateColorCodes("&", "&2&lHosted by Quashi")).setScore(0)
                    player.setScoreboard(board)

            scoreboard_update = False
class CraftEvent(PythonListener):
    @PythonEventHandler(CraftItemEvent, EventPriority.NORMAL)
    def onCraft(self, event):
        global tocollect
        global teamscompleted
        global teams
        global bingo
        if bingo["stage"] == "playing" and event.getView().getTitle() != "Bingo items":
            item = unicode(event.getCurrentItem().getType().getKey(), "utf-8")
            name = event.getWhoClicked().getDisplayName()
            #Bukkit.broadcastMessage(str(item))
            #Bukkit.broadcastMessage(str(name))
            for team in teams:
                if name in teams[team]:
                    teamname = team
                    #Bukkit.broadcastMessage(str(teamname))
            #Bukkit.broadcastMessage(str(tocollect))
            if item in tocollect:
                #Bukkit.broadcastMessage(str(teamscompleted))
                if item not in teamscompleted[teamname]:
                    for player in teams[teamname]:
                        COLLECTED = PREFIX + "&2Your team collected item " + str(item) + " !"
                        Bukkit.getPlayer(player).sendMessage(ChatColor.translateAlternateColorCodes("&", COLLECTED))
                    teamscompleted[teamname].append(str(item))
                     #Bukkit.broadcastMessage(str(len(teamscompleted[teamname])))
                    if len(teamscompleted[teamname]) == 9:
                        #Bukkit.broadcastMessage("in")
                        totp = event.getWhoClicked().getLocation()
                        rawplayerlist = Bukkit.getOnlinePlayers()
                        for player in rawplayerlist:
                            if event.getWhoClicked().getDisplayName() != player.getDisplayName():
                                player.teleport(totp)
                                player.setGameMode(GameMode.SPECTATOR)
                            WIN_MAIN = teamname + " &2&lwon!"
                            WIN_SUB = "&6Time spent: &c" + str(bingo["timer"]["timerunning"]["min"]) + " min " + str(bingo["timer"]["timerunning"]["sec"]) + " sec!"
                            player.sendTitle(ChatColor.translateAlternateColorCodes("&", WIN_MAIN), ChatColor.translateAlternateColorCodes("&", WIN_SUB), 15, 150, 10)
                            global stopmanager
                            stopmanager = True
                            bingo["stage"] = "end"


class PickupEvent(PythonListener):
    @PythonEventHandler(PlayerPickupItemEvent, EventPriority.NORMAL)
    def onPickup(self, event):
        global tocollect
        global teamscompleted
        global teams
        global bingo
        if bingo["stage"] == "playing":
            item = unicode(event.getItem().getItemStack().getType().getKey(), "utf-8")
            name = event.getPlayer().getDisplayName()
            #Bukkit.broadcastMessage(str(item))
            #Bukkit.broadcastMessage(str(name))
            for team in teams:
                if name in teams[team]:
                    teamname = team
                    #Bukkit.broadcastMessage(str(teamname))
            #Bukkit.broadcastMessage(str(tocollect))
            if item in tocollect:
                #Bukkit.broadcastMessage(str(teamscompleted))
                if item not in teamscompleted[teamname]:
                    for player in teams[teamname]:
                        COLLECTED = PREFIX + "&2Your team collected item " + str(item) + " !"
                        Bukkit.getPlayer(player).sendMessage(ChatColor.translateAlternateColorCodes("&", COLLECTED))
                    teamscompleted[teamname].append(str(item))
                    #Bukkit.broadcastMessage(str(len(teamscompleted[teamname])))
                    if len(teamscompleted[teamname]) == 9:
                        #Bukkit.broadcastMessage("in")
                        totp = event.getPlayer().getLocation()
                        rawplayerlist = Bukkit.getOnlinePlayers()
                        for player in rawplayerlist:
                            if event.getPlayer().getDisplayName() != player.getDisplayName():
                                player.teleport(totp)
                                player.setGameMode(GameMode.SPECTATOR)
                            WIN_MAIN = teamname + " &2&lwon!"
                            WIN_SUB = "&6Time spent: &c" + str(bingo["timer"]["timerunning"]["min"]) + " min " + str(bingo["timer"]["timerunning"]["sec"]) + " sec!"
                            player.sendTitle(ChatColor.translateAlternateColorCodes("&", WIN_MAIN), ChatColor.translateAlternateColorCodes("&", WIN_SUB), 15, 150, 10)
                            global stopmanager
                            stopmanager = True
                            bingo["stage"] = "end"

class DamageEvent(PythonListener):
    @PythonEventHandler(EntityDamageEvent, EventPriority.LOW)
    def onDamage(self, event):
        global bingo
        stage = bingo["stage"]
        if stage == "setup" or stage == "hold_teams" or stage == "hold_admin" or stage == "countdown":
            event.setCancelled(True)


class InteractListener(PythonListener):
    @PythonEventHandler(PlayerInteractEvent, EventPriority.LOW)
    def onInteract(self, event):
        if event.getItem() is not None and event.getItem().getItemMeta() is not None:
            if event.getItem().getItemMeta().hasLore():
                item = event.getItem()
                meta = item.getItemMeta()
                lore = meta.getLore()
                if len(lore) > 1:
                    action = lore[0]
                    word = action[2:-1]
                    # Bukkit.broadcastMessage("action: " + action + " word: " + word)
                    player = event.getPlayer()
                    # Bukkit.broadcastMessage(action[0])
                    if action[0] == "o":
                        if word == "teamsgui":
                            player.openInventory(InteractListener.teamgui(self, "player", player.getDisplayName()))

    def teamgui(self, forplayer, playername):
        global bingo
        global teams

        if bingo["join"]:
            NOTHING = ItemStack(Material.GRAY_STAINED_GLASS_PANE, 1)
            NOTHING_META = NOTHING.getItemMeta()
            NOTHING_META.setDisplayName(" ")
        else:
            NOTHING = ItemStack(Material.RED_STAINED_GLASS_PANE, 1)
            NOTHING_META = NOTHING.getItemMeta()
            NOTHING_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&c&lJoins disabled."))
        NOTHING_META.setLore(["LightEvents"])
        NOTHING.setItemMeta(NOTHING_META)

        yourteam = False
        yourteamraw = False
        for entry in teams:
            if playername in teams[entry]:
                yourteam = entry
                yourteamraw = entry
                break
        if not yourteam:
            yourteam = "&c&lYou haven't joined any team!"
            YOUR_TEAM = ItemStack(Material.WHITE_BED, 1)
            YOUR_TEAM_META = YOUR_TEAM.getItemMeta()
        else:
            yourteam = "&2&lYour team: " + yourteam
            YOUR_TEAM = ItemStack(Material.RED_BED, 1)
            YOUR_TEAM_META = YOUR_TEAM.getItemMeta()
        YOUR_TEAM_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", yourteam))
        if yourteamraw:
            teammemvers = ChatColor.translateAlternateColorCodes("&", "&a&lTeam members:")
            lore = [teammemvers]
            for player in teams[yourteamraw]:
                lore.append(ChatColor.translateAlternateColorCodes("&", "&f> " + str(player)))
        else:
            lore = ["You haven't joined a team yet!"]
        lore.append("LightEvents")
        YOUR_TEAM_META.setLore(lore)
        YOUR_TEAM.setItemMeta(YOUR_TEAM_META)
        teamview = False
        if forplayer == "player":

            INFO_PAPER = ItemStack(Material.PAPER, 1)
            INFO_PAPER_META = INFO_PAPER.getItemMeta()
            INFO_PAPER_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&9&lInformation"))
            dump = "Teams: " + str(len(teams))
            dump1 = "Team size: " + str(bingo["teamsize"])
            INFO_PAPER_META.setLore([dump, dump1, "LightEvents"])
            INFO_PAPER.setItemMeta(INFO_PAPER_META)

            CLOSE_PANE = ItemStack(Material.LIME_STAINED_GLASS_PANE, 1)
            CLOSE_PANE_META = CLOSE_PANE.getItemMeta()
            CLOSE_PANE_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&2&lOK / Confirm"))
            CLOSE_PANE_META.setLore(["Left click to", "close this view", "LightEvents", "x()"])
            CLOSE_PANE.setItemMeta(CLOSE_PANE_META)

            if not bingo["join"]:
                JOINS_STATUS = ItemStack(Material.RED_STAINED_GLASS_PANE, 1)
                JOINS_STATUS_META = JOINS_STATUS.getItemMeta()
                JOINS_STATUS_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&c&lJoins are disabled"))
            else:
                JOINS_STATUS = ItemStack(Material.LIME_STAINED_GLASS_PANE, 1)
                JOINS_STATUS_META = JOINS_STATUS.getItemMeta()
                JOINS_STATUS_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&2&lJoins are enabled"))
            JOINS_STATUS_META.setLore(["Indicates wether joins are", "enabled or disabled.", "LightEvents"])
            JOINS_STATUS.setItemMeta(JOINS_STATUS_META)

            teamview = Bukkit.createInventory(None, 27, "Team chooser")

            for i in range(0, 9):
                teamview.setItem(i, NOTHING)

            for i in range(18, 27):
                teamview.setItem(i, NOTHING)

            teamview.setItem(4, YOUR_TEAM)
            teamview.setItem(22, INFO_PAPER)
            teamview.setItem(26, CLOSE_PANE)
            teamview.setItem(25, JOINS_STATUS)

            num = 0
            for entry in teams:
                if bingo["join"]:
                    TEAM = ItemStack(Material.RED_BED, 1)
                    TEAM_META = TEAM.getItemMeta()
                    TEAM_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", entry))
                else:
                    TEAM = ItemStack(Material.WHITE_BED, 1)
                    TEAM_META = TEAM.getItemMeta()
                    TEAM_META.setDisplayName(
                        ChatColor.translateAlternateColorCodes("&", "&c&lYou can't join any teams yet!"))
                members = ChatColor.translateAlternateColorCodes("&", "&a&lTeam members:")
                lore = [members]
                if len(teams[entry]) != 0:
                    for player in teams[entry]:
                        newline = "&f> " + player
                        lore.append(ChatColor.translateAlternateColorCodes("&", newline))
                lore.append("LightEvents")
                if bingo["join"]:
                    cmdump = "j(" + entry + ")"
                    lore.append(cmdump)
                TEAM_META.setLore(lore)
                TEAM.setItemMeta(TEAM_META)
                slot = num + 9
                teamview.setItem(slot, TEAM)

                num = num + 1
        return teamview


class DropListener(PythonListener):
    @PythonEventHandler(PlayerDropItemEvent, EventPriority.LOW)
    def onDrop(self, event):
        if event.getItemDrop() is not None and event.getItemDrop().getItemStack().getItemMeta() is not None and event.getItemDrop().getItemStack().getItemMeta().hasLore() == True:
            item = event.getItemDrop().getItemStack()
            meta = item.getItemMeta()
            lore = meta.getLore()
            if lore[-2] == "LightEvents" or lore[-1] == "LightEvents":
                event.setCancelled(True)


class InventoryListener(PythonListener):
    @PythonEventHandler(InventoryClickEvent, EventPriority.LOW)
    def onClick(self, event):
        global JSON_DIR
        global presets
        global create
        global teams
        global teamscompleted
        if event.getCurrentItem() is not None and event.getCurrentItem().getItemMeta() is not None and event.getCurrentItem().getItemMeta().hasLore() == True:
            item = event.getCurrentItem()
            meta = item.getItemMeta()
            lore = meta.getLore()
            lenlore = len(lore)
            if lenlore > 0:
                if lore[-1] == "LightEvents":
                    event.setCancelled(True)
                if lenlore > 1 and lore[-1] == "LightEvents":
                    event.setCancelled(True)
                elif lenlore > 1 and lore[-2] == "LightEvents":
                    event.setCancelled(True)
                elif lenlore > 2 and lore[-3] == "LightEvents":
                    event.setCancelled(True)
                if lenlore > 1 and bingo["invclick"] == True:
                    lore = lore[-1]
                    word = lore[2:-1]
                    if lore[0] == "o":
                        if word == "timer_set":
                            event.getWhoClicked().openInventory(InventoryListener.timeinv(self, "admin"))
                        elif word == "admininv":
                            event.getWhoClicked().openInventory(InventoryListener.admininv(self))
                        elif word == "adm_teams":
                            event.getWhoClicked().openInventory(
                                InventoryListener.teamgui(self, "admin", event.getWhoClicked().getName()))
                        elif word == "newpreset":
                            event.getWhoClicked().openInventory(
                                InventoryListener.newpreset(self, "inventory", event.getInventory()))
                        elif word == "b_chooseinv":
                            event.getWhoClicked().openInventory(InventoryListener.binv(self, "admin"))
                    elif lore[0] == "x":
                        event.getWhoClicked().closeInventory()
                    elif lore[0] == "n":
                        if word[0] == "-":
                            # Bukkit.broadcastMessage(("-" + str(word[1:])))
                            if bingo["page"] != 0:
                                bingo["page"] = bingo["page"] - int(word[1:])
                                # Bukkit.broadcastMessage(str(bingo["page"]))
                                event.getWhoClicked().openInventory(InventoryListener.binv(self, "admin"))
                        else:
                            # Bukkit.broadcastMessage(("+" + str(word)))
                            bingo["page"] = bingo["page"] + int(word)
                            # Bukkit.broadcastMessage(str(bingo["page"]))
                            event.getWhoClicked().openInventory(InventoryListener.binv(self, "admin"))
                    elif lore[0] == "p":
                        event.getWhoClicked().openInventory(InventoryListener.presetview(self, str(word), "admin"))
                    elif lore[0] == "a":
                        if word == "reset":
                            bingo["timer"]["timetotal"] = 0
                            event.getWhoClicked().openInventory(InventoryListener.timeinv(self, "admin"))
                        elif word[0] == "-":
                            amount = float(word[1:])
                            if amount <= abs(bingo["timer"]["timetotal"]):
                                bingo["timer"]["timetotal"] = bingo["timer"]["timetotal"] - amount
                                event.getWhoClicked().openInventory(InventoryListener.timeinv(self, "admin"))
                        else:
                            amount = float(word)
                            bingo["timer"]["timetotal"] = bingo["timer"]["timetotal"] + amount
                            event.getWhoClicked().openInventory(InventoryListener.timeinv(self, "admin"))
                    elif lore[0] == "l":
                        bingo["preset"] = word
                        event.getWhoClicked().openInventory(InventoryListener.binv(self, "admin"))
                    elif lore[0] == "j":
                        if len(teams[word]) != bingo["teamsize"]:
                            for entry in teams:
                                if event.getWhoClicked().getName() in teams[entry]:
                                    teams[entry].remove(event.getWhoClicked().getName())
                            teams[word].append(event.getWhoClicked().getName())
                            TEAMJOIN = PREFIX + "&2You joined " + word + "&2!"
                            event.getWhoClicked().sendMessage(ChatColor.translateAlternateColorCodes("&", TEAMJOIN))
                            event.getWhoClicked().openInventory(
                                InventoryListener.teamgui(self, "player", event.getWhoClicked().getName()))
                        else:
                            TEAMJOINFAIL = PREFIX + "&cCannot join team " + word + ".&c Team is full!"
                            event.getWhoClicked().sendMessage(ChatColor.translateAlternateColorCodes("&", TEAMJOINFAIL))
                    elif lore[0] == "!":
                        if len(teams[word]) != bingo["teamsize"]:
                            for entry in teams:
                                if event.getWhoClicked().getName() in teams[entry]:
                                    teams[entry].remove(event.getWhoClicked().getName())
                            teams[word].append(event.getWhoClicked().getName())
                            TEAMJOIN = PREFIX + "&2You joined " + word + "&2!"
                            event.getWhoClicked().sendMessage(ChatColor.translateAlternateColorCodes("&", TEAMJOIN))
                            event.getWhoClicked().openInventory(
                                InventoryListener.teamgui(self, "admin", event.getWhoClicked().getName()))
                        else:
                            TEAMJOINFAIL = PREFIX + "&cCannot join team " + word + ".&c Team is full!"
                            event.getWhoClicked().sendMessage(ChatColor.translateAlternateColorCodes("&", TEAMJOINFAIL))
                    elif lore[0] == "k":
                        teams[word] = []
                        TEAMKICK = PREFIX + "&cKlicked all members of team " + word + "!"
                        event.getWhoClicked().sendMessage(ChatColor.translateAlternateColorCodes("&", TEAMKICK))
                        event.getWhoClicked().openInventory(
                            InventoryListener.teamgui(self, "admin", event.getWhoClicked().getName()))
                    elif lore[0] == "z":
                        if word == "addteam":
                            if len(teams) < 9:
                                toaddnum = len(teams) + 1
                                teamname = "&e&lTeam " + str(toaddnum)
                                teams[teamname] = []
                                teamscompleted[teamname] = []
                                # Bukkit.broadcastMessage(str(list(teams)))
                                list(teams).sort()
                                # Bukkit.broadcastMessage(" ")
                                # Bukkit.broadcastMessage(str(list(teams)))
                                event.getWhoClicked().sendMessage(
                                    ChatColor.translateAlternateColorCodes("&", PREFIX + "&2Team added!"))
                            else:
                                event.getWhoClicked().sendMessage(ChatColor.translateAlternateColorCodes("&", PREFIX + "&cCould not add team, team limit reached!"))
                            event.getWhoClicked().openInventory(
                                InventoryListener.teamgui(self, "admin", event.getWhoClicked().getName()))
                        elif word == "on":
                            bingo["join"] = True
                            event.getWhoClicked().openInventory(
                                InventoryListener.teamgui(self, "admin", event.getWhoClicked().getName()))
                        elif word == "off":
                            bingo["join"] = False
                            for team in list(teams):
                                teams[team] = []
                            Bukkit.broadcastMessage(ChatColor.translateAlternateColorCodes("&",
                                                                                           PREFIX + "&cEvery player got kicked out by an admin!\n" + PREFIX + "Please join again as teams get enabled again!"))
                            event.getWhoClicked().openInventory(
                                InventoryListener.teamgui(self, "admin", event.getWhoClicked().getName()))
                        elif word == "remteam":
                            if len(teams) > 1:
                                teamname = "&e&lTeam " + str(len(teams))
                                del teams[teamname]
                                del teamscompleted[teamname]
                                event.getWhoClicked().sendMessage(
                                    ChatColor.translateAlternateColorCodes("&", PREFIX + "&2Team removed!"))
                            else:
                                event.getWhoClicked().sendMessage(ChatColor.translateAlternateColorCodes("&",
                                                                                                         PREFIX + "&cCould not remove team, you must at least have 1 team!"))
                            event.getWhoClicked().openInventory(
                                InventoryListener.teamgui(self, "admin", event.getWhoClicked().getName()))
                        elif word == "addteamsiz":
                            if bingo["teamsize"] < 5:
                                bingo["teamsize"] = bingo["teamsize"] + 1
                                event.getWhoClicked().sendMessage(ChatColor.translateAlternateColorCodes("&",
                                                                                                         PREFIX + "&2Team size increased to " + str(
                                                                                                             bingo[
                                                                                                                 "teamsize"]) + "!"))
                            else:
                                event.getWhoClicked().sendMessage(ChatColor.translateAlternateColorCodes("&",
                                                                                                         PREFIX + "&cCould increase team size, max. team size is 5!"))
                            event.getWhoClicked().openInventory(
                                InventoryListener.teamgui(self, "admin", event.getWhoClicked().getName()))
                        elif word == "remteamsiz":
                            if bingo["teamsize"] > 1:
                                bingo["teamsize"] = bingo["teamsize"] - 1
                                event.getWhoClicked().sendMessage(ChatColor.translateAlternateColorCodes("&",
                                                                                                         PREFIX + "&2Team size decreased to " + str(
                                                                                                             bingo[
                                                                                                                 "teamsize"]) + "!"))
                            else:
                                event.getWhoClicked().sendMessage(ChatColor.translateAlternateColorCodes("&",
                                                                                                         PREFIX + "&cCould decrease team size, min. team size is 1!"))
                            event.getWhoClicked().openInventory(
                                InventoryListener.teamgui(self, "admin", event.getWhoClicked().getName()))
                        elif word == "reload":
                            with open((JSON_DIR + "presets.json"), "r") as jsonloader:
                                presets = json.load(jsonloader)
                                event.getWhoClicked().sendMessage(
                                    ChatColor.translateAlternateColorCodes("&", PREFIX + "&2Reload complete!"))
                            event.getWhoClicked().openInventory(InventoryListener.binv(self, "admin"))
                        elif word == "start":
                            starter = threading.Thread(target=InventoryListener.event_starter, args=(self,))
                            starter.start()
                            event.getWhoClicked().openInventory(InventoryListener.admininv(self))
                        elif word == "creatpres":
                            tosav = []
                            saveditems = []
                            topinv = event.getWhoClicked().getOpenInventory().getTopInventory()

                            i11 = topinv.getItem(11).getType().getKey()
                            i12 = topinv.getItem(12).getType().getKey()
                            i13 = topinv.getItem(13).getType().getKey()

                            i15 = topinv.getItem(15).getType().getKey()

                            i20 = topinv.getItem(20).getType().getKey()
                            i21 = topinv.getItem(21).getType().getKey()
                            i22 = topinv.getItem(22).getType().getKey()

                            i29 = topinv.getItem(29).getType().getKey()
                            i30 = topinv.getItem(30).getType().getKey()
                            i31 = topinv.getItem(31).getType().getKey()

                            tosav.append(i15)
                            tosav.append(i11)
                            tosav.append(i12)
                            tosav.append(i13)
                            tosav.append(i20)
                            tosav.append(i21)
                            tosav.append(i22)
                            tosav.append(i29)
                            tosav.append(i30)
                            tosav.append(i31)

                            # for i in range(0, 45):
                            #    if event.getWhoClicked().getOpenInventory().getTopInventory().getItem(i).hasItemMeta() == False:
                            #        savitems.append(event.getWhoClicked().getOpenInventory().getTopInventory().getItem(i).getKey())

                            presetnum = len(presets)
                            num = 0
                            toappend = {}
                            for entries in tosav:
                                # REG = PREFIX + "Registered item " + str(unicode(entries, 'utf-8'))
                                # event.getWhoClicked().sendMessage(ChatColor.translateAlternateColorCodes("&", REG))
                                saveditems.append(unicode(entries, 'utf-8'))
                                toappend[unicode(str(num), 'utf-8')] = unicode(entries, 'utf-8')
                                num = num + 1
                            # Bukkit.broadcastMessage(str(toappend))
                            presets[unicode(str(presetnum), 'utf-8')] = toappend
                            # Bukkit.broadcastMessage(str(presets))

                            event.getWhoClicked().sendMessage(
                                ChatColor.translateAlternateColorCodes("&", PREFIX + "&2Preset created!"))
                            with open((JSON_DIR + "presets.json"), "w") as jsonloader:
                                jsn_dump = json.dumps(presets, indent=4)
                                jsonloader.write(jsn_dump)
                                event.getWhoClicked().sendMessage(
                                    ChatColor.translateAlternateColorCodes("&", PREFIX + "&2Presets saved!"))
                            event.getWhoClicked().openInventory(InventoryListener.binv(self, "admin"))
                        elif word == "resumetimer":
                            bingo["stage"] = "countdown"
                            event.getWhoClicked().openInventory(InventoryListener.admininv(self))
                        elif word == "pausetimer":
                            bingo["stage"] = "hold_admin"
                            event.getWhoClicked().openInventory(InventoryListener.admininv(self))

                        elif word == "rlcheck":
                            if event.getWhoClicked().getOpenInventory().getTitle() == "Create Preset":
                                InventoryListener.newpreset(self, "update", event.getWhoClicked().getOpenInventory())
                        elif word == "save":
                            with open((JSON_DIR + "presets.json"), "w") as jsonloader:
                                jsn_dump = json.dumps(presets, indent=4)
                                jsonloader.write(jsn_dump)
                                event.getWhoClicked().sendMessage(
                                    ChatColor.translateAlternateColorCodes("&", PREFIX + "&2Presets saved!"))

    def event_starter(self):
        global bingo
        global teams
        global stopstarter
        global randomcode
        global diablock
        global diatypebefore
        global spawn
        global tocollect
        EVENT_COUNTDOWN = "&2Bingo configured!"
        EVENT_COUNTDOWN_SUBTITLE = "&7Bingo can only start when every player is in a team!"
        for player in Bukkit.getOnlinePlayers():
            player.sendTitle(ChatColor.translateAlternateColorCodes("&", EVENT_COUNTDOWN),
                             ChatColor.translateAlternateColorCodes("&", EVENT_COUNTDOWN_SUBTITLE), 15, 100, 15)
        bingo["timetostart"] = 60
        bingo["stage"] = "countdown"
        rawplayerlist = Bukkit.getOnlinePlayers()
        while bingo["timetostart"] != 0 and stopstarter == False:
            sleep(1)
            if bingo["stage"] != "hold_admin":
                bingo["stage"] = "countdown"
                #Bukkit.broadcastMessage("im here!")
                timetostart = bingo["timetostart"]
                rawplayerlist = Bukkit.getOnlinePlayers()
                playerlist = []
                for player in rawplayerlist:
                    #player.setLevel(timetostart)
                    playerlist.append(player.getDisplayName())
                playersinteams = []
                for team in teams:
                    if len(teams[team]) != 0:
                        for i in teams[team]:
                            playersinteams.append(i)
                TITLE = "&6&lBINGO"
                if timetostart == 23:
                    PLUGIN = "&7Hosted by Quashi"
                    for player in rawplayerlist:
                        player.getInventory().clear()
                        player.sendTitle(ChatColor.translateAlternateColorCodes("&", TITLE), ChatColor.translateAlternateColorCodes("&", PLUGIN), 15, 320, 15)
                elif timetostart == 17:
                    MADE_BY = "&aPlugin made with <3 from Quasi"
                    for player in rawplayerlist:
                        player.getInventory().clear()
                        player.sendTitle(ChatColor.translateAlternateColorCodes("&", TITLE), ChatColor.translateAlternateColorCodes("&", MADE_BY), 0, 90, 15)
                elif timetostart == 11:
                    IPs = PREFIX + "&2Getting IPs..."
                    Bukkit.broadcastMessage(ChatColor.translateAlternateColorCodes("&", IPs))
                elif timetostart == 10:
                    for player in playerlist:
                        ip = str(randint(0, 255)) + "." + str(randint(0, 255)) + "." + str(randint(0, 255)) + "." + str(randint(0, 255))
                        msg = "Logging IP from " + player + ": " + ip
                        Bukkit.broadcastMessage(msg)
                elif timetostart == 9:
                    DOS = PREFIX + "&2Starting DOS..."
                    Bukkit.broadcastMessage(ChatColor.translateAlternateColorCodes("&", DOS))
                    bingo["allowmove"] = False
                    sleep(3)
                    bingo["allowmove"] = True
                    bingo["timetostart"] = 6
                    DOS = PREFIX + "&2DOS Complete..."
                    Bukkit.broadcastMessage(ChatColor.translateAlternateColorCodes("&", DOS))
                elif timetostart == 30:
                    bingo["admingui"] = False
                    bingo["kick"] = True
                    LOCKED_IN = "&2Bingo locked in!"
                    LOCKED_IN_SUB = "&cNobody can edit the settings anymore, nobody can join!"
                    for player in rawplayerlist:
                        bingo["invclick"] = False
                        player.getInventory().clear()
                        player.sendTitle(ChatColor.translateAlternateColorCodes("&", LOCKED_IN), ChatColor.translateAlternateColorCodes("&", LOCKED_IN_SUB), 15, 100, 15)
                elif timetostart == 4:
                    bingo["allowmove"] = False
                    for player in rawplayerlist:
                        TITLE = "&3&l3"
                        player.sendTitle(ChatColor.translateAlternateColorCodes("&", TITLE), "", 15, 320, 15)
                elif timetostart == 3:
                    for player in rawplayerlist:
                        TITLE = "&2&l2"
                        player.sendTitle(ChatColor.translateAlternateColorCodes("&", TITLE), "", 15, 320, 15)
                elif timetostart == 2:
                    for player in rawplayerlist:
                        TITLE = "&1&l1"
                        player.sendTitle(ChatColor.translateAlternateColorCodes("&", TITLE), "", 15, 320, 15)
                if len(playersinteams) == 0:
                    bingo["timetostart"] = 60
                    bingo["kick"] = False
                if len(playersinteams) != len(playerlist):
                    bingo["stage"] = "hold_teams"
                elif bingo["stage"] != "hold_admin" and len(playersinteams) != 0:
                    bingo["timetostart"] = bingo["timetostart"] - 1

        border = rawplayerlist[0].getLocation().getWorld().getWorldBorder()
        border.setSize(100, 3)
        border.setSize(10000, 0)
        for player in rawplayerlist:
            TITLE = "&6&lSTART"
            GL = "&2&lHave fun!"
            player.sendTitle(ChatColor.translateAlternateColorCodes("&", TITLE), ChatColor.translateAlternateColorCodes("&", GL), 15, 50, 10)
        bingo["stage"] = "playing"
        bingo["allowmove"] = True
        for item in presets[bingo["preset"]]:
            tocollect.append(presets[bingo["preset"]][item])
        del tocollect[0]
        while bingo["timer"]["timerunning"]["min"] != bingo["timer"]["timetotal"] and stopstarter == False and bingo["stage"] != "end":
            runningsecs = bingo["timer"]["timerunning"]["sec"]
            runningmins = bingo["timer"]["timerunning"]["min"]
            if runningsecs == 59:
                bingo["timer"]["timerunning"]["sec"] = 0
                bingo["timer"]["timerunning"]["min"] = runningmins + 1
            else:
                bingo["timer"]["timerunning"]["sec"] = runningsecs + 1
            sleep(1)
        Bukkit.broadcastMessage(ChatColor.translateAlternateColorCodes("&", PREFIX + "&2The event ended. The server will shut down in 90 seconds."))
        while bingo["timerestart"] != 0:
            TIMERRAW = "&c" + str(bingo["timerestart"]) + " seconds until the server stops."
            TIMER = TextComponent("Time: " + TIMERRAW)
            TIMER.setColor(BungeeChatColor.GREEN)
            for player in Bukkit.getOnlinePlayers():
                player.spigot().sendMessage(ChatMessageType.ACTION_BAR, TIMER)
            bingo["timerestart"] = bingo["timerestart"] - 1


# "timer": {"timetotal": 0, "timerunning": {"sec": 0, "min": 0}}
    def gameruleinv(self):
        global bingo
        global NOTHING

        PVP_ENABLED = ItemStack(Material.DIAMOND_SWORD, 1)
        PVP_ENABLED_META = PVP_ENABLED.getItemMeta()
        if bingo["pvp"]["enabled"] == "True":
            PVP_ENABLED_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&c&lDisable PvP"))
            PVP_ENABLED_META.setLore(["Left click to confirm", "and turn on PvP.", "LightEvents", "z(pvpoffs)"])
        else:
            PVP_ENABLED_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&2&lEnable PVP"))
            PVP_ENABLED_META.setLore(["Left click to confirm", "and turn on PvP.", "LightEvents", "z(pvpon)"])
        PVP_ENABLED.setItemMeta(PVP_ENABLED_META)

        LEAVE_PANE = ItemStack(Material.LIME_STAINED_GLASS_PANE, 1)
        LEAVE_PANE_META = LEAVE_PANE.getItemMeta()
        LEAVE_PANE_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&2&lOK / Confirm"))
        LEAVE_PANE_META.setLore(["Left click to confirm", "and get back.", "LightEvents", "o(admininv)"])
        LEAVE_PANE.setItemMeta(LEAVE_PANE_META)

        gamerinv = Bukkit.createInventory(None, 45, "Gamerules")
        for i in range(0, 45):
            gamerinv.setItem(i, NOTHING)

        return gamerinv

    def teamgui(self, type, playername):
        global NOTHING
        global bingo
        global teams
        yourteam = False
        yourteamraw = False
        for entry in teams:
            if playername in teams[entry]:
                yourteam = entry
                yourteamraw = entry
                break
        if yourteam == False:
            yourteam = "&c&lYou haven't joined any team!"
            YOUR_TEAM = ItemStack(Material.WHITE_BED, 1)
            YOUR_TEAM_META = YOUR_TEAM.getItemMeta()
        else:
            yourteam = "&2&lYour team: " + yourteam
            YOUR_TEAM = ItemStack(Material.RED_BED, 1)
            YOUR_TEAM_META = YOUR_TEAM.getItemMeta()
        YOUR_TEAM_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", yourteam))
        if yourteamraw:
            teammemvers = ChatColor.translateAlternateColorCodes("&", "&a&lTeam members:")
            lore = [teammemvers]
            for player in teams[yourteamraw]:
                lore.append(ChatColor.translateAlternateColorCodes("&", "&f> " + str(player)))
        else:
            lore = ["You haven't joined a team yet!"]
        lore.append("LightEvents")
        YOUR_TEAM_META.setLore(lore)
        YOUR_TEAM.setItemMeta(YOUR_TEAM_META)
        teamview = False
        if type == "admin":
            if not bingo["join"]:
                REM_TEAM = ItemStack(Material.RED_DYE, 1)
            else:
                REM_TEAM = ItemStack(Material.GRAY_DYE, 1)
            REM_TEAM_META = REM_TEAM.getItemMeta()
            REM_TEAM_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&c&lRemove a team"))
            if not bingo["join"]:
                REM_TEAM_META.setLore(["Left click to confirm", "and get back.", "LightEvents", "z(remteam)"])
            else:
                REM_TEAM_META.setLore(["Left click to confirm", "and get back.", "LightEvents"])
            REM_TEAM.setItemMeta(REM_TEAM_META)

            if not bingo["join"]:
                ADD_TEAM = ItemStack(Material.LIME_DYE, 1)
            else:
                ADD_TEAM = ItemStack(Material.GRAY_DYE, 1)
            ADD_TEAM_META = ADD_TEAM.getItemMeta()
            ADD_TEAM_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&2&lAdd a team"))
            if not bingo["join"]:
                ADD_TEAM_META.setLore(["Left click to confirm", "and get back.", "LightEvents", "z(addteam)"])
            else:
                ADD_TEAM_META.setLore(["Left click to confirm", "and get back.", "LightEvents"])
            ADD_TEAM.setItemMeta(ADD_TEAM_META)

            if not bingo["join"]:
                ADD_TEAMSIZE = ItemStack(Material.LIME_DYE, 1)
            else:
                ADD_TEAMSIZE = ItemStack(Material.GRAY_DYE, 1)
            ADD_TEAMSIZE_META = ADD_TEAMSIZE.getItemMeta()
            ADD_TEAMSIZE_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&2&lIncrease team size"))
            if not bingo["join"]:
                ADD_TEAMSIZE_META.setLore(["Left click to confirm", "and get back.", "LightEvents", "z(addteamsiz)"])
            else:
                ADD_TEAMSIZE_META.setLore(["Left click to confirm", "and get back.", "LightEvents"])
            ADD_TEAMSIZE.setItemMeta(ADD_TEAMSIZE_META)

            if not bingo["join"]:
                REMOVE_TEAMSIZE = ItemStack(Material.RED_DYE, 1)
            else:
                REMOVE_TEAMSIZE = ItemStack(Material.GRAY_DYE, 1)
            REMOVE_TEAMSIZE_META = REMOVE_TEAMSIZE.getItemMeta()
            REMOVE_TEAMSIZE_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&c&lDecrease team size"))
            if not bingo["join"]:
                REMOVE_TEAMSIZE_META.setLore(["Left click to confirm", "and get back.", "LightEvents", "z(remteamsiz)"])
            else:
                REMOVE_TEAMSIZE_META.setLore(["Left click to confirm", "and get back.", "LightEvents"])
            REMOVE_TEAMSIZE.setItemMeta(REMOVE_TEAMSIZE_META)

            LEAVE_PANE = ItemStack(Material.LIME_STAINED_GLASS_PANE, 1)
            LEAVE_PANE_META = LEAVE_PANE.getItemMeta()
            LEAVE_PANE_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&2&lOK / Confirm"))
            LEAVE_PANE_META.setLore(["Left click to confirm", "and get back.", "LightEvents", "o(admininv)"])
            LEAVE_PANE.setItemMeta(LEAVE_PANE_META)

            INFO_PAPER = ItemStack(Material.PAPER, 1)
            INFO_PAPER_META = INFO_PAPER.getItemMeta()
            INFO_PAPER_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&2&lInformation"))
            dump = "Teams: " + str(len(teams))
            dump1 = "Team size: " + str(bingo["teamsize"])
            INFO_PAPER_META.setLore([dump, dump1, "LightEvents"])
            INFO_PAPER.setItemMeta(INFO_PAPER_META)

            ENABLE_JOIN = ItemStack(Material.LEVER, 1)
            ENABLE_JOIN_META = ENABLE_JOIN.getItemMeta()
            if not bingo["join"]:
                ENABLE_JOIN_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&2&lEnable joins"))
                ENABLE_JOIN_META.setLore(["Left click to confirm", "and enable joins", "LightEvents", "z(on)"])
            else:
                ENABLE_JOIN_META.setDisplayName(
                    ChatColor.translateAlternateColorCodes("&", "&c&lDisable joins & kick all players"))
                ENABLE_JOIN_META.setLore(["Left click to confirm", "and disable joins", "LightEvents", "z(off)"])
            ENABLE_JOIN.setItemMeta(ENABLE_JOIN_META)

            if not bingo["join"]:
                JOINS_STATUS = ItemStack(Material.RED_STAINED_GLASS_PANE, 1)
                JOINS_STATUS_META = JOINS_STATUS.getItemMeta()
                JOINS_STATUS_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&c&lJoins are disabled"))
            else:
                JOINS_STATUS = ItemStack(Material.LIME_STAINED_GLASS_PANE, 1)
                JOINS_STATUS_META = JOINS_STATUS.getItemMeta()
                JOINS_STATUS_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&2&lJoins are enabled"))
            JOINS_STATUS_META.setLore(["Click the lever to turn", "joins on / off", "LightEvents"])
            JOINS_STATUS.setItemMeta(JOINS_STATUS_META)

            teamview = Bukkit.createInventory(None, 45, "Team chooser")

            for i in range(0, 18):
                teamview.setItem(i, NOTHING)
            teamview.setItem(0, YOUR_TEAM)
            teamview.setItem(2, REM_TEAM)
            teamview.setItem(3, ADD_TEAM)
            teamview.setItem(4, INFO_PAPER)
            teamview.setItem(5, ADD_TEAMSIZE)
            teamview.setItem(6, REMOVE_TEAMSIZE)
            teamview.setItem(8, LEAVE_PANE)
            for i in range(36, 45):
                teamview.setItem(i, NOTHING)
            teamview.setItem(44, ENABLE_JOIN)
            teamview.setItem(43, JOINS_STATUS)
            num = 0
            # Bukkit.broadcastMessage("setting teams")
            for entry in teams:

                REM_SPECIFIC_TEAM = ItemStack(Material.BARRIER, 1)
                REM_SPECIFIC_TEAM_META = REM_SPECIFIC_TEAM.getItemMeta()
                dump = "&c&lKick team members of team " + entry
                REM_SPECIFIC_TEAM_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", dump))
                cmdump = "k(" + entry + ")"
                REM_SPECIFIC_TEAM_META.setLore(["Left click to", "kick all members", "LightEvents", cmdump])
                REM_SPECIFIC_TEAM.setItemMeta(REM_SPECIFIC_TEAM_META)
                slot = num + 27
                teamview.setItem(slot, REM_SPECIFIC_TEAM)

                TEAM = ItemStack(Material.RED_BED, 1)
                TEAM_META = TEAM.getItemMeta()
                TEAM_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", entry))
                members = ChatColor.translateAlternateColorCodes("&", "&a&lTeam members:")
                lore = [members]
                if len(teams[entry]) != 0:
                    # Bukkit.broadcastMessage("no not null!")
                    for player in teams[entry]:
                        # Bukkit.broadcastMessage("pane num" + str(num) + "appends player!")
                        newline = "&f> " + player
                        lore.append(ChatColor.translateAlternateColorCodes("&", newline))
                lore.append("LightEvents")
                if bingo["join"]:
                    cmdump = "!(" + entry + ")"
                    lore.append(cmdump)
                TEAM_META.setLore(lore)
                TEAM.setItemMeta(TEAM_META)
                slot = num + 18
                teamview.setItem(slot, TEAM)

                num = num + 1
        if type == "player":

            INFO_PAPER = ItemStack(Material.PAPER, 1)
            INFO_PAPER_META = INFO_PAPER.getItemMeta()
            INFO_PAPER_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&9&lInformation"))
            dump = "Teams: " + str(len(teams))
            dump1 = "Team size: " + str(bingo["teamsize"])
            INFO_PAPER_META.setLore([dump, dump1, "LightEvents"])
            INFO_PAPER.setItemMeta(INFO_PAPER_META)

            CLOSE_PANE = ItemStack(Material.LIME_STAINED_GLASS_PANE, 1)
            CLOSE_PANE_META = CLOSE_PANE.getItemMeta()
            CLOSE_PANE_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&2&lOK / Confirm"))
            CLOSE_PANE_META.setLore(["Left click to", "close this view", "LightEvents", "x()"])
            CLOSE_PANE.setItemMeta(CLOSE_PANE_META)

            if not bingo["join"]:
                JOINS_STATUS = ItemStack(Material.RED_STAINED_GLASS_PANE, 1)
                JOINS_STATUS_META = JOINS_STATUS.getItemMeta()
                JOINS_STATUS_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&c&lJoins are disabled"))
            else:
                JOINS_STATUS = ItemStack(Material.LIME_STAINED_GLASS_PANE, 1)
                JOINS_STATUS_META = JOINS_STATUS.getItemMeta()
                JOINS_STATUS_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&2&lJoins are enabled"))
            JOINS_STATUS_META.setLore(["Indicates wether joins are", "enabled or disabled.", "LightEvents"])
            JOINS_STATUS.setItemMeta(JOINS_STATUS_META)

            teamview = Bukkit.createInventory(None, 27, "Team chooser")

            for i in range(0, 9):
                teamview.setItem(i, NOTHING)

            for i in range(18, 27):
                teamview.setItem(i, NOTHING)

            teamview.setItem(4, YOUR_TEAM)
            teamview.setItem(22, INFO_PAPER)
            teamview.setItem(26, CLOSE_PANE)
            teamview.setItem(25, JOINS_STATUS)

            num = 0
            for entry in teams:
                if bingo["join"]:
                    TEAM = ItemStack(Material.RED_BED, 1)
                    TEAM_META = TEAM.getItemMeta()
                    TEAM_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", entry))
                else:
                    TEAM = ItemStack(Material.WHITE_BED, 1)
                    TEAM_META = TEAM.getItemMeta()
                    TEAM_META.setDisplayName(
                        ChatColor.translateAlternateColorCodes("&", "&c&lYou can't join any teams yet!"))
                members = ChatColor.translateAlternateColorCodes("&", "&a&lTeam members:")
                lore = [members]
                if len(teams[entry]) != 0:
                    for player in teams[entry]:
                        newline = "&f> " + player
                        lore.append(ChatColor.translateAlternateColorCodes("&", newline))
                lore.append("LightEvents")
                if bingo["join"]:
                    cmdump = "j(" + entry + ")"
                    lore.append(cmdump)
                TEAM_META.setLore(lore)
                TEAM.setItemMeta(TEAM_META)
                slot = num + 9
                teamview.setItem(slot, TEAM)

                num = num + 1
        return teamview

    def presetview(self, presetview, forplayer):
        global NOTHING
        global presets
        if forplayer == "admin":
            # Bukkit.broadcastMessage("hey im in")
            presview = Bukkit.createInventory(None, 45, "Preset Viewer")
            for i in range(0, 45):
                presview.setItem(i, NOTHING)
            # Bukkit.broadcastMessage("nothing set")
            slot = 0
            for i in range(1, 10):
                if 0 < i < 4:
                    slot = i + 9
                elif 3 < i < 7:
                    slot = i + 15
                elif 6 < i < 10:
                    slot = i + 21
                # Bukkit.broadcastMessage("setting type")
                # Bukkit.broadcastMessage(str(presets[str(presetview)][str(i)]))
                PRESET_SEE = ItemStack(Material.matchMaterial(str(presets[str(presetview)][str(i)])), 1)
                # Bukkit.broadcastMessage("type set!")
                PRESET_SEE_META = PRESET_SEE.getItemMeta()
                dump = "&2&lBlock " + str(i)
                PRESET_SEE_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", dump))
                # Bukkit.broadcastMessage("name set")
                PRESET_SEE_META.setLore(["", "", "LightEvents"])
                PRESET_SEE.setItemMeta(PRESET_SEE_META)
                presview.setItem(slot, PRESET_SEE)

            OK_PANE = ItemStack(Material.LIME_STAINED_GLASS_PANE, 1)
            OK_PANE_META = OK_PANE.getItemMeta()
            OK_PANE_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&2&lOK / Confirm"))
            cmdump = "l(" + presetview + ")"
            OK_PANE_META.setLore(["Left click to confirm", "and get back.", "LightEvents", cmdump])
            OK_PANE.setItemMeta(OK_PANE_META)

            LEAVE_PANE = ItemStack(Material.RED_STAINED_GLASS_PANE, 1)
            LEAVE_PANE_META = LEAVE_PANE.getItemMeta()
            LEAVE_PANE_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&c&lCancel / Go back"))
            LEAVE_PANE_META.setLore(["Left click to confirm", "and get back.", "LightEvents", "o(b_chooseinv)"])
            LEAVE_PANE.setItemMeta(LEAVE_PANE_META)

            presview.setItem(15, OK_PANE)
            presview.setItem(33, LEAVE_PANE)
            return presview

    def newpreset(self, forplayer, inv):
        presupd = True
        global NOTHING
        if forplayer == "inventory":
            CHECK_PANE = ItemStack(Material.RED_STAINED_GLASS_PANE, 1)
            CHECK_PANE_META = CHECK_PANE.getItemMeta()
            CHECK_PANE_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&c&lPreset not ready"))
            CHECK_PANE_META.setLore(["Fill in all empty", "spaces to proceed.", "LightEvents"])
            CHECK_PANE.setItemMeta(CHECK_PANE_META)

            RELOAD = ItemStack(Material.COMPARATOR, 1)
            RELOAD_META = RELOAD.getItemMeta()
            RELOAD_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&2&lCheck"))
            RELOAD_META.setLore(["Left click to", "check all items", "LightEvents", "z(rlcheck)"])
            RELOAD.setItemMeta(RELOAD_META)

            newpreset = Bukkit.createInventory(None, 45, "Create Preset")
            for i in range(0, 11):
                newpreset.setItem(i, NOTHING)
            newpreset.setItem(14, NOTHING)
            for i in range(16, 20):
                newpreset.setItem(i, NOTHING)
            for i in range(23, 29):
                newpreset.setItem(i, NOTHING)
            for i in range(32, 45):
                newpreset.setItem(i, NOTHING)
            newpreset.setItem(24, RELOAD)
            newpreset.setItem(33, CHECK_PANE)

            LEAVE_PANE = ItemStack(Material.RED_STAINED_GLASS_PANE, 1)
            LEAVE_PANE_META = LEAVE_PANE.getItemMeta()
            LEAVE_PANE_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&c&lCancel / Go back"))
            LEAVE_PANE_META.setLore(["Left click to confirm", "and get back.", "LightEvents", "o(b_chooseinv)"])
            LEAVE_PANE.setItemMeta(LEAVE_PANE_META)

            newpreset.setItem(44, LEAVE_PANE)

            return newpreset
        elif forplayer == "update":
            # Bukkit.broadcastMessage("checkfirstempty")
            if inv.getTopInventory().firstEmpty() == -1:
                # Bukkit.broadcastMessage("noempty")
                duplicate = []

                i11 = inv.getTopInventory().getItem(11).getType().getKey()
                i12 = inv.getTopInventory().getItem(12).getType().getKey()
                i13 = inv.getTopInventory().getItem(13).getType().getKey()

                i20 = inv.getTopInventory().getItem(20).getType().getKey()
                i21 = inv.getTopInventory().getItem(21).getType().getKey()
                i22 = inv.getTopInventory().getItem(22).getType().getKey()

                i29 = inv.getTopInventory().getItem(29).getType().getKey()
                i30 = inv.getTopInventory().getItem(30).getType().getKey()
                i31 = inv.getTopInventory().getItem(31).getType().getKey()

                duplicate.append(i11)
                duplicate.append(i12)
                duplicate.append(i13)
                duplicate.append(i20)
                duplicate.append(i21)
                duplicate.append(i22)
                duplicate.append(i29)
                duplicate.append(i30)
                duplicate.append(i31)

                if len(duplicate) == len(set(duplicate)):
                    # no duplicates
                    CHECK_PANE = ItemStack(Material.LIME_STAINED_GLASS_PANE, 1)
                    CHECK_PANE_META = CHECK_PANE.getItemMeta()
                    CHECK_PANE_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&2&lCreate Preset"))
                    CHECK_PANE_META.setLore(["Left click to confirm", "and get back.", "LightEvents", "z(creatpres)"])
                    CHECK_PANE.setItemMeta(CHECK_PANE_META)
                else:
                    # there are duplicates
                    CHECK_PANE = ItemStack(Material.YELLOW_STAINED_GLASS_PANE, 1)
                    CHECK_PANE_META = CHECK_PANE.getItemMeta()
                    CHECK_PANE_META.setDisplayName(
                        ChatColor.translateAlternateColorCodes("&", "&e&lDuplicates detected!"))
                    CHECK_PANE_META.setLore(["Please change all", "duplicate items and check again", "LightEvents"])
                    CHECK_PANE.setItemMeta(CHECK_PANE_META)
            else:
                CHECK_PANE = ItemStack(Material.RED_STAINED_GLASS_PANE, 1)
                CHECK_PANE_META = CHECK_PANE.getItemMeta()
                CHECK_PANE_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&c&lPreset not ready"))
                CHECK_PANE_META.setLore(["Fill in all empty", "spaces to proceed.", "LightEvents"])
                CHECK_PANE.setItemMeta(CHECK_PANE_META)
            # Bukkit.broadcastMessage("set!")
            inv.getTopInventory().setItem(33, CHECK_PANE)

    def binv(self, type):
        # Bukkit.broadcastMessage("called!")
        global NOTHING
        global bingo
        global presets
        if type == "admin":
            # Bukkit.broadcastMessage("match !")
            PRESET_SELECTED = ItemStack(Material.matchMaterial(presets[bingo["preset"]]["0"]), 1)
            # Bukkit.broadcastMessage("match ok!")
            PRESET_SELECTED_META = PRESET_SELECTED.getItemMeta()
            PRESET_SELECTED_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&a&lCurrently Selected"))
            cmdump = "p(" + str(bingo["preset"]) + ")"
            PRESET_SELECTED_META.setLore(["Preset number:", str(bingo["preset"]), "LightEvents", cmdump])
            PRESET_SELECTED.setItemMeta(PRESET_SELECTED_META)

            PREV_PAGE = ItemStack(Material.GRAY_DYE, 1)
            PREV_PAGE_META = PREV_PAGE.getItemMeta()
            PREV_PAGE_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&e&l< Previous page <"))
            PREV_PAGE_META.setLore(["Left click to the", "previos page", "LightEvents", "n(-1)"])
            PREV_PAGE.setItemMeta(PREV_PAGE_META)

            PAGENUM = ItemStack(Material.PAPER, 1)
            PAGENUM_META = PAGENUM.getItemMeta()
            dump = "&e&lPage &6&l" + str(bingo["page"])
            PAGENUM_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", dump))
            page = "Full Pages: " + str(round(len(presets) / 27))[0:]
            pres = "Presets: " + str(len(presets))
            PAGENUM_META.setLore([page, pres, "LightEvents"])
            PAGENUM.setItemMeta(PAGENUM_META)

            NEXT_PAGE = ItemStack(Material.GRAY_DYE, 1)
            NEXT_PAGE_META = NEXT_PAGE.getItemMeta()
            NEXT_PAGE_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&e&l> Next page >"))
            NEXT_PAGE_META.setLore(["Left click to the", "next page", "LightEvents", "n(1)"])
            NEXT_PAGE.setItemMeta(NEXT_PAGE_META)

            CREATE_PRESET = ItemStack(Material.NETHER_STAR, 1)
            CREATE_PRESET_META = CREATE_PRESET.getItemMeta()
            CREATE_PRESET_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&c&lCreate preset"))
            CREATE_PRESET_META.setLore(["Left click to", "create a preset", "LightEvents", "o(newpreset)"])
            CREATE_PRESET.setItemMeta(CREATE_PRESET_META)

            OK_PANE = ItemStack(Material.LIME_STAINED_GLASS_PANE, 1)
            OK_PANE_META = OK_PANE.getItemMeta()
            OK_PANE_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&2&lOK / Confirm"))
            OK_PANE_META.setLore(["Left click to confirm", "and get back.", "LightEvents", "o(admininv)"])
            OK_PANE.setItemMeta(OK_PANE_META)

            RELOAD = ItemStack(Material.FIREWORK_STAR, 1)
            RELOAD_META = RELOAD.getItemMeta()
            RELOAD_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&2&lReload"))
            RELOAD_META.setLore(["Left click to", "reload the presets", "LightEvents", "z(reload)"])
            RELOAD.setItemMeta(RELOAD_META)

            SAVE = ItemStack(Material.NAME_TAG, 1)
            SAVE_META = SAVE.getItemMeta()
            SAVE_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&2&lSave"))
            SAVE_META.setLore(["Left click to", "save the presets", "LightEvents", "z(save)"])
            SAVE.setItemMeta(SAVE_META)

            # Bukkit.broadcastMessage("projects browser")
            # Presets browser
            binv = Bukkit.createInventory(None, 45, "Preset Browser")
            GLIMMER = Enchantment.DURABILITY
            # god i hope ill be fine after this...
            for i in range(0, 27):
                slot = i + 18
                i = i + bingo["page"] * 27
                if unicode(str(i), 'utf-8') in presets:
                    # Bukkit.broadcastMessage("reading page")
                    # Bukkit.broadcastMessage("page ok")
                    # print(type(i))
                    thumb = presets[unicode(str(i), 'utf-8')]["0"]
                    # Bukkit.broadcastMessage("got the thumb")
                    PRESET = ItemStack(Material.matchMaterial(thumb))
                    # Bukkit.broadcastMessage("set it...")
                    PRESET_META = PRESET.getItemMeta()
                    dump = "&a&lPreset Number &b&l" + str(i)
                    PRESET_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", dump))
                    cmdump = "p(" + str(i) + ")"
                    PRESET_META.setLore(["Left click to", "view the contents", "LightEvents", cmdump])
                    PRESET.setItemMeta(PRESET_META)
                    # Bukkit.broadcastMessage("meta = ok")
                    if str(i) == bingo["preset"]:
                        PRESET.addUnsafeEnchantment(GLIMMER, 1)
                    elif PRESET.containsEnchantment(GLIMMER) == True and not i == bingo["preset"]:
                        PRESET.removeEnchantment(GLIMMER)
                    binv.setItem(slot, PRESET)

            for i in range(0, 18):
                binv.setItem(i, NOTHING)
            for i in range(27, 45):
                binv.setItem(i, NOTHING)

            binv.setItem(0, PRESET_SELECTED)
            binv.setItem(3, PREV_PAGE)
            binv.setItem(4, PAGENUM)
            binv.setItem(5, NEXT_PAGE)
            binv.setItem(8, CREATE_PRESET)
            binv.setItem(44, OK_PANE)
            binv.setItem(36, RELOAD)
            binv.setItem(37, SAVE)

            return binv

    def timeinv(self, forplayer):
        global NOTHING
        global bingo
        TIMER_CLOCK = ItemStack(Material.CLOCK, 1)
        TIMER_CLOCK_META = TIMER_CLOCK.getItemMeta()
        TIMERHEADER = "&9&lTimer: " + str(bingo["timer"]["timetotal"]) + " minutes"
        TIMER_CLOCK_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", TIMERHEADER))
        if bingo["timer"]["timerunning"]["min"] == 0:
            TIMERLORE1 = "The event doesn't run yet."
            TIMERLORE2 = "The event doesn't run yet."
        else:
            TIMERLORE1 = "Time left: " + str(
                bingo["timer"]["timerunning"]["min"] - bingo["timer"]["timetotal"]) + " min "
            TIMERLORE2 = "Time running: " + str(bingo["timer"]["timerunning"]["min"]) + " min " + str(
                bingo["timer"]["timerunning"]["sec"]) + " sec."
        TIMER_CLOCK_META.setLore([TIMERLORE1, TIMERLORE2, "LightEvents"])
        TIMER_CLOCK.setItemMeta(TIMER_CLOCK_META)
        if forplayer == "admin":
            OK_PANE = ItemStack(Material.LIME_STAINED_GLASS_PANE, 1)
            OK_PANE_META = OK_PANE.getItemMeta()
            OK_PANE_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&2&lOK / Confirm"))
            OK_PANE_META.setLore(["Left click to confirm", "and get back.", "LightEvents", "o(admininv)"])
            OK_PANE.setItemMeta(OK_PANE_META)
            RESET_PANE = ItemStack(Material.RED_STAINED_GLASS_PANE, 1)
            RESET_PANE_META = RESET_PANE.getItemMeta()
            RESET_PANE_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&c&lRESET"))
            RESET_PANE_META.setLore(["Left click to confirm", "and reset the timer", "LightEvents", "a(reset)"])
            RESET_PANE.setItemMeta(RESET_PANE_META)
            timer_set = Bukkit.createInventory(None, 45, "Time Menu")
            for i in range(0, 45):
                timer_set.setItem(i, NOTHING)
            timer_set.setItem(9, TIMER_CLOCK)
            timer_set.setItem(17, OK_PANE)
            mins = "ERROR"
            for i in range(1, 7):
                if i == 1:
                    mins = 1
                if i == 2:
                    mins = 3
                if i == 3:
                    mins = 5
                if i == 4:
                    mins = 10
                if i == 5:
                    mins = 30
                if i == 6:
                    mins = 60
                if i == 7:
                    mins = 90
                ADDTIME = ItemStack(Material.LIME_DYE, 1)
                ADDTIME_META = ADDTIME.getItemMeta()
                dump = "Add " + str(mins) + " minutes"
                ADDTIME_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", dump))
                dump = "Adds " + str(mins) + " minutes to the timer"
                cmdump = "a(" + str(mins) + ")"
                ADDTIME_META.setLore(["Left click to confirm", dump, "LightEvents", cmdump])
                ADDTIME.setItemMeta(ADDTIME_META)
                timer_set.setItem(i + 9, ADDTIME)
            for i in range(1, 7):
                if i == 1:
                    mins = 1
                if i == 2:
                    mins = 3
                if i == 3:
                    mins = 5
                if i == 4:
                    mins = 10
                if i == 5:
                    mins = 30
                if i == 6:
                    mins = 60
                if i == 7:
                    mins = 90
                ADDTIME = ItemStack(Material.RED_DYE, 1)
                ADDTIME_META = ADDTIME.getItemMeta()
                dump = "Remove " + str(mins) + " minutes"
                ADDTIME_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", dump))
                dump = "Removes " + str(mins) + " minutes from the timer"
                cmdump = "a(" + "-" + str(mins) + ")"
                ADDTIME_META.setLore(["Left click to confirm", dump, "LightEvents", cmdump])
                ADDTIME.setItemMeta(ADDTIME_META)
                timer_set.setItem(i + 27, ADDTIME)
            timer_set.setItem(27, TIMER_CLOCK)
            timer_set.setItem(35, RESET_PANE)
            return timer_set

    def admininv(self):
        global NOTHING
        ITEMS_DROPER = ItemStack(Material.CHEST, 1)
        ITEMS_DROPER_META = ITEMS_DROPER.getItemMeta()
        ITEMS_DROPER_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&2&lBingo items"))
        ITEMS_DROPER_META.setLore(["Left click to", "edit and view items", "LightEvents", "o(b_chooseinv)"])
        ITEMS_DROPER.setItemMeta(ITEMS_DROPER_META)

        TIMER_CLOCK = ItemStack(Material.CLOCK, 1)
        TIMER_CLOCK_META = TIMER_CLOCK.getItemMeta()
        TIMER_CLOCK_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&3&lTimer settings"))
        TIMER_CLOCK_META.setLore(["Left click to", "edit", "LightEvents", "o(timer_set)"])
        TIMER_CLOCK.setItemMeta(TIMER_CLOCK_META)

        GAMERULES_CMD = ItemStack(Material.COMMAND_BLOCK, 1)
        GAMERULES_CMD_META = GAMERULES_CMD.getItemMeta()
        GAMERULES_CMD_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&a&lGamerules"))
        GAMERULES_CMD_META.setLore(["Left click to", "edit and view gamerules", "LightEvents", "o(gamer_inv)"])
        GAMERULES_CMD.setItemMeta(GAMERULES_CMD_META)

        ADMIN_TEAMS = ItemStack(Material.RED_BED, 1)
        ADMIN_TEAMS_META = ADMIN_TEAMS.getItemMeta()
        ADMIN_TEAMS_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&e&lTeam options"))
        ADMIN_TEAMS_META.setLore(["Left click to", "see and add teams", "LightEvents", "o(adm_teams)"])
        ADMIN_TEAMS.setItemMeta(ADMIN_TEAMS_META)

        INFO_SIGN = ItemStack(Material.OAK_SIGN, 1)
        INFO_SIGN_META = INFO_SIGN.getItemMeta()
        INFO_SIGN_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&e&lOverview"))
        dump = "Preset selected: " + str(bingo["preset"])
        dump1 = "Timer length: " + str(bingo["timer"]["timetotal"])
        INFO_SIGN_META.setLore([dump, dump1, "LightEvents", "Thanks for using LightEvents!", "<3"])
        INFO_SIGN.setItemMeta(INFO_SIGN_META)

        if bingo["preset"] != "0" and bingo["timer"]["timetotal"] > 0 and bingo["join"]:
            STATUS_PANE = ItemStack(Material.LIME_STAINED_GLASS_PANE, 1)
            STATUS_PANE_META = STATUS_PANE.getItemMeta()
            STATUS_PANE_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&2&lConfirm and start event"))
            STATUS_PANE_META.setLore(
                ["You'll be able to interuppt", "the countdown until 30sec.", "LightEvents", "z(start)"])
            STATUS_PANE.setItemMeta(STATUS_PANE_META)
        else:
            STATUS_PANE = ItemStack(Material.RED_STAINED_GLASS_PANE, 1)
            STATUS_PANE_META = STATUS_PANE.getItemMeta()
            STATUS_PANE_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&c&lEvent not ready yet"))
            STATUS_PANE_META.setLore(
                ["Please see the information Sign", "to see which parameters are missing", "LightEvents"])
            STATUS_PANE.setItemMeta(STATUS_PANE_META)
        if bingo["stage"] == "countdown" or bingo["stage"] == "hold_teams":
            STATUS_PANE = ItemStack(Material.YELLOW_STAINED_GLASS_PANE, 1)
            STATUS_PANE_META = STATUS_PANE.getItemMeta()
            STATUS_PANE_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&e&lPause timer"))
            STATUS_PANE_META.setLore(
                ["You'll be able to interuppt", "the countdown until 30sec.", "LightEvents", "z(pausetimer)"])
            STATUS_PANE.setItemMeta(STATUS_PANE_META)
        elif bingo["stage"] == "hold_admin":
            STATUS_PANE = ItemStack(Material.LIME_STAINED_GLASS_PANE, 1)
            STATUS_PANE_META = STATUS_PANE.getItemMeta()
            STATUS_PANE_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&2&lResume timer"))
            STATUS_PANE_META.setLore(
                ["You'll be able to interuppt", "the countdown until 30sec.", "LightEvents", "z(resumetimer)"])
            STATUS_PANE.setItemMeta(STATUS_PANE_META)

        CLOSE_PANE = ItemStack(Material.RED_STAINED_GLASS_PANE, 1)
        CLOSE_PANE_META = CLOSE_PANE.getItemMeta()
        CLOSE_PANE_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&c&lClose"))
        CLOSE_PANE_META.setLore(["Left click to", "close this view", "LightEvents", "x()"])
        CLOSE_PANE.setItemMeta(CLOSE_PANE_META)
        # invs
        admininv = Bukkit.createInventory(None, 45, "Admin Menu")
        for i in range(1, 12):
            admininv.setItem((i - 1), NOTHING)
        admininv.setItem(11, ITEMS_DROPER)
        admininv.setItem(12, NOTHING)
        admininv.setItem(13, TIMER_CLOCK)
        admininv.setItem(14, NOTHING)
        admininv.setItem(15, GAMERULES_CMD)
        for i in range(1, 14):
            admininv.setItem((i - 1 + 16), NOTHING)
        admininv.setItem(29, ADMIN_TEAMS)
        admininv.setItem(30, NOTHING)
        admininv.setItem(31, INFO_SIGN)
        admininv.setItem(32, NOTHING)
        admininv.setItem(33, STATUS_PANE)
        for i in range(34, 45):
            admininv.setItem(i, NOTHING)
        admininv.setItem(44, CLOSE_PANE)
        return admininv


# Plugin
class LightEvents(PythonPlugin):
    def onEnable(self):
        global stopmanager
        global presets
        global JSON_DIR
        stopmanager = False
        LightEvents.log(self, "Enabeling LightEvents, please wait", True)
        LightEvents.log(self, "Registring events...", True)
        pm = self.getServer().getPluginManager()
        self.listener = JoinListener()
        pm.registerEvents(self.listener, self)
        self.listener = DropListener()
        pm.registerEvents(self.listener, self)
        self.listener = InventoryListener()
        pm.registerEvents(self.listener, self)
        self.listener = FoodListener()
        pm.registerEvents(self.listener, self)
        self.listener = QuitListener()
        pm.registerEvents(self.listener, self)
        self.listener = DamageEvent()
        pm.registerEvents(self.listener, self)
        self.listener = InteractListener()
        pm.registerEvents(self.listener, self)
        self.listener = MoveListener()
        pm.registerEvents(self.listener, self)
        self.listener = PickupEvent()
        pm.registerEvents(self.listener, self)
        self.listener = PlayerDeath()
        pm.registerEvents(self.listener, self)
        self.listener = CraftEvent()
        pm.registerEvents(self.listener, self)
        manager = threading.Thread(target=LightEvents.manager, args=(self,))
        manager.start()
        LightEvents.log(self, "Loading jsons", True)
        with open((JSON_DIR + "presets.json"), "r") as jsonloader:
            LightEvents.log(self, "File read", True)
            presets = json.load(jsonloader)
            LightEvents.log(self, "Jump'n run json loaded!", True)
        pass

    def onDisable(self):
        global stopmanager
        global stopstarter
        global randomcode
        stopmanager = True
        stopstarter = True

    def onCommand(self, sender, command, label, args):
        global bingo
        global randomcode
        global tocollect
        global teams
        commandlow = command.getName().lower()
        bingos = ["b", "bg", "bi", "bin", "bgo", "bingo"]
        if commandlow in bingos:
            if bingo["stage"] == "playing":
                bingoinv = Bukkit.createInventory(None, InventoryType.DROPPER, "Bingo items")
                name = sender.getPlayer().getDisplayName()
                slot = 0
                #Bukkit.broadcastMessage("making teams")
                for team in teams:
                    if name in teams[team]:
                        teamname = team
                #Bukkit.broadcastMessage(teamname)
                for item in tocollect:
                    if item not in teamscompleted[teamname]:
                        ITEM = ItemStack(Material.matchMaterial(item), 1)
                        ITEM_META = ITEM.getItemMeta()
                        ITEM_META.setLore(["One of the blocks you have to", "collect in order to win", "LightEvents"])
                        ITEM.setItemMeta(ITEM_META)
                    else:
                        ITEM = ItemStack(Material.LIME_STAINED_GLASS_PANE, 1)
                        ITEM_META = ITEM.getItemMeta()
                        ITEM_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&2&lAlready collected:"))
                        ITEM_META.setLore([item, "you don't have to collect this item.", "LightEvents"])
                        ITEM.setItemMeta(ITEM_META)
                    bingoinv.setItem(slot, ITEM)
                    slot = slot +  1
                sender.getPlayer().openInventory(bingoinv)

            else:
                NO = PREFIX + "&cYou can only open the bingo inventory when the game starts!"
                sender.getPlayer().sendMessage(ChatColor.translateAlternateColorCodes("&", NO))
            return True
        elif commandlow == "teams":
            if bingo["stage"] == "playing":
                global bingo
                global teams
                NOTHING2 = ItemStack(Material.GRAY_STAINED_GLASS_PANE, 1)
                NOTHING_META2 = NOTHING2.getItemMeta()
                NOTHING_META2.setDisplayName(ChatColor.translateAlternateColorCodes("&", " "))
                NOTHING_META2.setLore(["LightEvents"])
                NOTHING2.setItemMeta(NOTHING_META2)
                yourteam = False
                yourteamraw = False
                player = sender.getPlayer()
                playername = sender.getPlayer().getDisplayName()
                for entry in teams:
                    if playername in teams[entry]:
                        yourteam = entry
                        yourteamraw = entry
                        break
                if not yourteam:
                    yourteam = "&c&lYou haven't joined any team!"
                    YOUR_TEAM = ItemStack(Material.WHITE_BED, 1)
                    YOUR_TEAM_META = YOUR_TEAM.getItemMeta()
                else:
                    yourteam = "&2&lYour team: " + yourteam
                    YOUR_TEAM = ItemStack(Material.RED_BED, 1)
                    YOUR_TEAM_META = YOUR_TEAM.getItemMeta()
                YOUR_TEAM_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", yourteam))
                if yourteamraw:
                    teammemvers = ChatColor.translateAlternateColorCodes("&", "&a&lTeam members:")
                    lore = [teammemvers]
                    for player in teams[yourteamraw]:
                        lore.append(ChatColor.translateAlternateColorCodes("&", "&f> " + str(player)))
                else:
                    lore = ["You haven't joined a team yet!"]
                lore.append("LightEvents")
                YOUR_TEAM_META.setLore(lore)
                YOUR_TEAM.setItemMeta(YOUR_TEAM_META)
                teamview = False
                INFO_PAPER = ItemStack(Material.PAPER, 1)
                INFO_PAPER_META = INFO_PAPER.getItemMeta()
                INFO_PAPER_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&9&lInformation"))
                dump = "Teams: " + str(len(teams))
                dump1 = "Team size: " + str(bingo["teamsize"])
                INFO_PAPER_META.setLore([dump, dump1, "LightEvents"])
                INFO_PAPER.setItemMeta(INFO_PAPER_META)

                CLOSE_PANE = ItemStack(Material.LIME_STAINED_GLASS_PANE, 1)
                CLOSE_PANE_META = CLOSE_PANE.getItemMeta()
                CLOSE_PANE_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&2&lOK / Confirm"))
                CLOSE_PANE_META.setLore(["Left click to", "close this view", "LightEvents", "x()"])
                CLOSE_PANE.setItemMeta(CLOSE_PANE_META)


                teamview = Bukkit.createInventory(None, 27, "Team chooser")

                for i in range(0, 9):
                    teamview.setItem(i, NOTHING2)

                for i in range(18, 27):
                    teamview.setItem(i, NOTHING2)

                teamview.setItem(4, YOUR_TEAM)
                teamview.setItem(22, INFO_PAPER)
                teamview.setItem(26, NOTHING2)
                teamview.setItem(25, NOTHING2)

                num = 0
                for entry in teams:
                    TEAM = ItemStack(Material.RED_BED, 1)
                    TEAM_META = TEAM.getItemMeta()
                    TEAM_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", entry))
                    members = ChatColor.translateAlternateColorCodes("&", "&a&lTeam members:")
                    lore = [members]
                    if len(teams[entry]) != 0:
                        for player in teams[entry]:
                            newline = "&f> " + player
                            lore.append(ChatColor.translateAlternateColorCodes("&", newline))

                    teamcompl = "&a&lCollected &2" + str(len(teamscompleted[entry])) + "&f / 9"
                    lore.append(ChatColor.translateAlternateColorCodes("&", teamcompl))

                    lore.append("LightEvents")
                    TEAM_META.setLore(lore)
                    TEAM.setItemMeta(TEAM_META)
                    slot = num + 9
                    teamview.setItem(slot, TEAM)
                    num = num + 1

                sender.getPlayer().openInventory(teamview)
            else:
                NO = PREFIX + "&cYou can only open the team completation inventory when the game starts!"
                sender.getPlayer().sendMessage(ChatColor.translateAlternateColorCodes("&", NO))
            return True
        elif commandlow == "event":
            if bingo["admingui"] == True:
                ITEMS_DROPER = ItemStack(Material.CHEST, 1)
                ITEMS_DROPER_META = ITEMS_DROPER.getItemMeta()
                ITEMS_DROPER_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&2&lBingo items"))
                ITEMS_DROPER_META.setLore(["Left click to", "edit and view items", "LightEvents", "o(b_chooseinv)"])
                ITEMS_DROPER.setItemMeta(ITEMS_DROPER_META)

                TIMER_CLOCK = ItemStack(Material.CLOCK, 1)
                TIMER_CLOCK_META = TIMER_CLOCK.getItemMeta()
                TIMER_CLOCK_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&3&lTimer settings"))
                TIMER_CLOCK_META.setLore(["Left click to", "edit", "LightEvents", "o(timer_set)"])
                TIMER_CLOCK.setItemMeta(TIMER_CLOCK_META)

                GAMERULES_CMD = ItemStack(Material.COMMAND_BLOCK, 1)
                GAMERULES_CMD_META = GAMERULES_CMD.getItemMeta()
                GAMERULES_CMD_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&a&lGamerules"))
                GAMERULES_CMD_META.setLore(["Left click to", "edit and view gamerules", "LightEvents", "o(gamer_inv)"])
                GAMERULES_CMD.setItemMeta(GAMERULES_CMD_META)

                ADMIN_TEAMS = ItemStack(Material.RED_BED, 1)
                ADMIN_TEAMS_META = ADMIN_TEAMS.getItemMeta()
                ADMIN_TEAMS_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&e&lTeam options"))
                ADMIN_TEAMS_META.setLore(["Left click to", "see and add teams", "LightEvents", "o(adm_teams)"])
                ADMIN_TEAMS.setItemMeta(ADMIN_TEAMS_META)

                INFO_SIGN = ItemStack(Material.OAK_SIGN, 1)
                INFO_SIGN_META = INFO_SIGN.getItemMeta()
                INFO_SIGN_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&e&lOverview"))
                dump = "Preset selected: " + str(bingo["preset"])
                dump1 = "Timer length: " + str(bingo["timer"]["timetotal"])
                INFO_SIGN_META.setLore([dump, dump1, "LightEvents", "Thanks for using LightEvents!", "<3"])
                INFO_SIGN.setItemMeta(INFO_SIGN_META)

                if bingo["preset"] != "0" and bingo["timer"]["timetotal"] > 0 and bingo["join"]:
                    STATUS_PANE = ItemStack(Material.LIME_STAINED_GLASS_PANE, 1)
                    STATUS_PANE_META = STATUS_PANE.getItemMeta()
                    STATUS_PANE_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&2&lConfirm and start event"))
                    STATUS_PANE_META.setLore(
                        ["You'll be able to interuppt", "the countdown until 30sec.", "LightEvents", "z(start)"])
                    STATUS_PANE.setItemMeta(STATUS_PANE_META)
                else:
                    STATUS_PANE = ItemStack(Material.RED_STAINED_GLASS_PANE, 1)
                    STATUS_PANE_META = STATUS_PANE.getItemMeta()
                    STATUS_PANE_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&c&lEvent not ready yet"))
                    STATUS_PANE_META.setLore(
                        ["Please see the information Sign", "to see which parameters are missing", "LightEvents"])
                    STATUS_PANE.setItemMeta(STATUS_PANE_META)
                if bingo["stage"] == "countdown" or bingo["stage"] == "hold_teams":
                    STATUS_PANE = ItemStack(Material.YELLOW_STAINED_GLASS_PANE, 1)
                    STATUS_PANE_META = STATUS_PANE.getItemMeta()
                    STATUS_PANE_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&e&lPause timer"))
                    STATUS_PANE_META.setLore(
                        ["You'll be able to interuppt", "the countdown until 30sec.", "LightEvents", "z(pausetimer)"])
                    STATUS_PANE.setItemMeta(STATUS_PANE_META)
                elif bingo["stage"] == "hold_admin":
                    STATUS_PANE = ItemStack(Material.LIME_STAINED_GLASS_PANE, 1)
                    STATUS_PANE_META = STATUS_PANE.getItemMeta()
                    STATUS_PANE_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&2&lResume timer"))
                    STATUS_PANE_META.setLore(
                        ["You'll be able to interuppt", "the countdown until 30sec.", "LightEvents", "z(resumetimer)"])
                    STATUS_PANE.setItemMeta(STATUS_PANE_META)

                CLOSE_PANE = ItemStack(Material.RED_STAINED_GLASS_PANE, 1)
                CLOSE_PANE_META = CLOSE_PANE.getItemMeta()
                CLOSE_PANE_META.setDisplayName(ChatColor.translateAlternateColorCodes("&", "&c&lClose"))
                CLOSE_PANE_META.setLore(["Left click to", "close this view", "LightEvents", "x()"])
                CLOSE_PANE.setItemMeta(CLOSE_PANE_META)
                # invs
                admininv = Bukkit.createInventory(None, 45, "Admin Menu")
                for i in range(1, 12):
                    admininv.setItem((i - 1), NOTHING)
                admininv.setItem(11, ITEMS_DROPER)
                admininv.setItem(12, NOTHING)
                admininv.setItem(13, TIMER_CLOCK)
                admininv.setItem(14, NOTHING)
                admininv.setItem(15, GAMERULES_CMD)
                for i in range(1, 14):
                    admininv.setItem((i - 1 + 16), NOTHING)
                admininv.setItem(29, ADMIN_TEAMS)
                admininv.setItem(30, NOTHING)
                admininv.setItem(31, INFO_SIGN)
                admininv.setItem(32, NOTHING)
                admininv.setItem(33, STATUS_PANE)
                for i in range(34, 45):
                    admininv.setItem(i, NOTHING)
                admininv.setItem(44, CLOSE_PANE)
                sender.getPlayer().openInventory(admininv)
            else:
                NO = PREFIX + "&cYou can only open the admin until 30 seconds to the countdown!"
                sender.getPlayer().sendMessage(ChatColor.translateAlternateColorCodes("&", NO))
            # Bukkit.broadcastMessage("mainhand")
            # itmh = sender.getPlayer().getInventory().getItemInMainHand()
            # Bukkit.broadcastMessage("name")
            # name = str(itmh.getType().getKey())
            # Bukkit.broadcastMessage("print")
            # Bukkit.broadcastMessage(name)
            return True

    def manager(self):
        global stopmanager
        global bingo
        global teams
        global scoreboard_update
        title = True
        bf = False
        MSG = "&c&lERROR - MSG NOT SET!"
        COL = BarColor.WHITE
        while stopmanager != True:
            if bingo["stage"] == "setup":
                if bingo["join"] == False:
                    title = True
                    if bf == True:
                        TEAMTITLE = "&cTeams got disabled!"
                        TEAMSUBTITLE = "&4You got kicked out!"
                        for player in Bukkit.getOnlinePlayers():
                            player.sendTitle(ChatColor.translateAlternateColorCodes("&", TEAMTITLE),
                                             ChatColor.translateAlternateColorCodes("&", TEAMSUBTITLE), 15, 100, 15)
                        bf = False
                if bingo["timetostart"] == 0 and bingo["join"] == False:
                    MSG = "&c&lWaiting for admin to setup game..."
                    COL = BarColor.RED
                elif bingo["join"] == True:
                    MSG = "&3&lTeams enabled! Please use the team viewer to join a team!"
                    COL = BarColor.BLUE
                    if title == True:
                        bf = True
                        TEAMTITLE = "&2Teams are now enabled!"
                        TEAMSUBTITLE = "&6Use the team viewer to join a team!"
                        for player in Bukkit.getOnlinePlayers():
                            player.sendTitle(ChatColor.translateAlternateColorCodes("&", TEAMTITLE),
                                             ChatColor.translateAlternateColorCodes("&", TEAMSUBTITLE), 15, 100, 15)
                        title = False
            elif bingo["stage"] == "countdown":
                COL = BarColor.GREEN
                MSG = "&2&lBingo will start in " + str(bingo["timetostart"]) + " seconds"
                for player in Bukkit.getOnlinePlayers():
                    player.setLevel(bingo["timetostart"])

            elif bingo["stage"] == "hold_teams":
                COL = BarColor.YELLOW
                MSG = "&e&lTimer hold at " + str(bingo["timetostart"]) + " seconds, not every player is in a team!"
            elif bingo["stage"] == "hold_admin":
                COL = BarColor.YELLOW
                MSG = "&e&lTimer hold at " + str(bingo["timetostart"]) + " seconds, admin needs to change things!"
            elif bingo["stage"] == "playing":
                remainingmins = bingo["timer"]["timetotal"] - bingo["timer"]["timerunning"]["min"]
                secsin = bingo["timer"]["timerunning"]["sec"]
                if secsin == 0:
                    LEFT = str(remainingmins)[0:-2] + " min"
                else:
                    LEFT = str(remainingmins - 1)[0:-2] + " min " + str(60 - secsin) + " sec"
                MSG = "&2Time remaining: " + LEFT
                COL = BarColor.GREEN
            setupbar = Bukkit.createBossBar(ChatColor.translateAlternateColorCodes("&", MSG), COL,
                                            BarStyle.SOLID)
            if bingo["timer"]["timerunning"]["sec"] != 0:
                multiplywith = float(1.0/bingo["timer"]["timetotal"])
                secpercent = float(bingo["timer"]["timerunning"]["sec"]/60.0)
                percent = multiplywith * (bingo["timer"]["timerunning"]["min"] + secpercent)
                percent = 1 - percent
                setupbar.setProgress(percent)
            if bingo["timetostart"] != 0:
                multiplywith = float(100.0/6000.0)
                percent = multiplywith * int(bingo["timetostart"])
                setupbar.setProgress(percent)
            for player in Bukkit.getOnlinePlayers():
                setupbar.addPlayer(player.getPlayer())

            #Scoreboard

            sleep(1)
            scoreboard_update = True
            setupbar.removeAll()

# "timer": {"timetotal": 0, "timerunning": {"sec": 0, "min": 0}}
    def log(self, message, force=False):
        global DEBUG
        if DEBUG == True:
            self.getLogger().info(ChatColor.translateAlternateColorCodes("&", message))
        elif force == True:
            self.getLogger().info(ChatColor.translateAlternateColorCodes("&", message))
