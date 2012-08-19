import urllib
import json
from EveKillDownloader.KillMailModels import KillMail, Pilot, Corporation, Alliance, Item

class EveKill:
    def __init__(self):
        self._eveKillMasks = 0
        self._eveKillCommands = []

    def addEveKillMask(self,mask):
        self._eveKillMasks += mask

    def removeEveKillMask(self,mask):
        self._eveKillMasks -= mask

    def addCommand(self, eveKillCommand, value):
        eveKillCommand = "%s:%s" % (eveKillCommand, value)
        try :
            self._eveKillCommands.index(eveKillCommand)
        except ValueError:
            self._eveKillCommands.append(eveKillCommand)

    def removeCommand(self, eveKillCommand, value):
        eveKillCommand = "%s:%s" % (eveKillCommand, value)

        try :
            if self._eveKillCommands.index(eveKillCommand) != -1:
                self._eveKillCommands.remove(eveKillCommand)
        except ValueError:
            raise ValueError("eveKillCommand does not exist")

    def getURL(self):
        url = "http://eve-kill.net/epic/mask:%i" % (self._eveKillMasks)
        for eveKillCommand in self._eveKillCommands:
            url = "%s/%s" % (url, eveKillCommand)

        return url

    def getKills(self):
        url = self.getURL()

        killsResponse = urllib.urlopen(url)
        kills = json.load(killsResponse)

        return self.mapJSONtoKillMail(kills)

    def mapJSONtoKillMail(self, kills):
        killMails = []

        for kill in kills:
            killMail = KillMail()
            killMail.victimName = kill['victimName']
            killMail.url = kill['url']
            killMail.timestamp = kill['timestamp']
            killMail.internalId = kill['internalID']
            killMail.externalId = kill['externalID']
            killMail.victimExternalId = kill['victimExternalID']
            killMail.victimCorpName = kill['victimCorpName']
            killMail.victimAllianceName = kill['victimAllianceName']
            killMail.victimShipName = kill['victimShipName']
            killMail.victimShipClass = kill['victimShipClass']
            killMail.victimShipId = kill['victimShipID']
            killMail.fbPilotName = kill['FBPilotName']
            killMail.fbCorpName = kill['FBCorpName']
            killMail.fbAllianceName = kill['FBAllianceName']
            killMail.involvedPartyCount = kill['involvedPartyCount']
            killMail.solarSystemName = kill['solarSystemName']
            killMail.regionName = kill['regionName']
            killMail.isk = kill['ISK']

            for pilotJSON in kill['involvedParties']:
                pilot = self.mapJSONtoPilot(pilotJSON)
                killMail.involvedParties.append(pilot)

            items = kill['items']

            for itemJSON in items['destroyed']:
                item = self.mapJSONtoItem(itemJSON)
                killMail.itemsDestroyed.append(item)

            for itemJSON in items['dropped']:
                item = self.mapJSONtoItem(itemJSON)
                killMail.itemsDropped.append(item)

            killMails.append(killMail)
        return killMails

    def mapJSONtoPilot(self, pilotJson):
        pilot = Pilot()
        pilot.characterId = int(pilotJson['characterID'])
        pilot.characterName = pilotJson['characterName']
        pilot.corporation = self.mapJSONPilotToCorporation(pilotJson)
        return pilot

    def mapJSONPilotToCorporation(self, pilotJson):
        corporation = Corporation()
        corporation.corporationId = pilotJson['corporationID']
        corporation.corporationName = pilotJson['corporationName']
        corporation.alliance = self.mapJSONPilotToAlliance(pilotJson)
        return corporation

    def mapJSONPilotToAlliance(self, pilotJson):
        alliance = Alliance()
        alliance.allianceId = pilotJson['allianceID']
        alliance.allianceName = pilotJson['allianceName']
        return alliance

    def mapJSONtoItem(self, itemJson):
        item =  Item()
        item.typeId = itemJson['typeID']
        item.typeName = itemJson['typeName']
        item.itemSlot = int(itemJson['itemSlot'])
        item.qnty = int(itemJson['qtyDropped'])
        return item

class EveKillCommands(object) :
    MAIL_LIMIT = "mailLimit"
    WEEK = "week"
    YEAR = "year"
    MIN_KILL_ID = "minKillId"

class EveKillMask(object):
    KILLURL = 1
    TIMESTAMP = 2
    INTERNAL_EVE_KILL_ID = 4
    CCP_API_KILL_ID = 8
    VICTIM_NAME = 16
    VICTIM_EXTERNAL_ID = 32
    VICTIM_CORP_NAME = 64
    VICTIM_ALLIANCE_NAME = 128
    VICTIM_SHIP_NAME = 256
    VICTIM_SHIP_CLASS = 512
    VICTIM_SHIP_EXTERNAL_ID = 1024
    FINAL_BLOW_PILOT_NAME = 2048
    FINAL_BLOW_CORP_NAME = 4096
    FINAL_BLOW_ALLIANCE_NAME = 8192
    COUNT_INVOLVED_PLAYERS = 16384
    SOLAR_SYSTEM_OF_KILL = 32768
    SOLAR_SYSTEM_SECURITY = 65536
    REGION_OF_KILL = 131072
    ISK_VALUE = 131072
    INVOLVED_PILOTS = 524288
    ITEMS_DROPPED = 1048576
    RAWMAIL = 2097152