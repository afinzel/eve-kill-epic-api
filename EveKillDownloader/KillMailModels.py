class KillMail(object):
    def __init__(self):
        self.url = ""
        self.timestamp = ''
        self.internalId = 0
        self.externalId = 0
        self.victimName = ''
        self.victimExternalId = 0
        self.victimCorpName = ''
        self.victimAllianceName = ''
        self.victimShipName = ''
        self.victimShipClass = ''
        self.victimShipId = 0
        self.fbCorpName = ''
        self.fbAllianceName = ''
        self.involvedPartyCount = 0
        self.solarSystemName = ''
        self.regionName = ''
        self.ISK = 0
        self.involvedParties = []
        self.itemsDestroyed = []
        self.itemsDropped = []

class Pilot(object):
    def __init__(self):
        self.characterId = 0
        self.characterName = ''
        self.corparation = Corporation()

class Corporation(object):
    def __init__(self):
        self.corporationId = 0
        self.corporationName = ''
        self.alliance = Alliance()

class Alliance(object):
    def __init__(self):
        self.allianceId = 0
        self.allianceName = ''

class Item(object):
    def __init__(self):
        self.typeId = 0
        self.typeName =''
        self.itemSlot = 0
        self.qnty = 0

