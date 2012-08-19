from StringIO import StringIO
from io import BytesIO
import json
from django.utils import unittest
import urllib
import mox
from EveKillDownloader.EveKill import EveKillCommands, EveKillMask
from EveKillDownloader.EveKill import EveKill
from EveKillDownloader.KillMailModels import KillMail


class EveKillDownloaderTestCase(unittest.TestCase):
    def setUp(self):
        self.EveKill = EveKill()
        self.defaultURL = "http://eve-kill.net/epic/"
        self.mockOneKill = '[{"url":"http:\/\/eve-kill.net\/?a=kill_detail&kll_id=14384295","timestamp":"2012-08-19 16:19:00","internalID":14384295,"externalID":25294196,"victimName":"Traktorustos","victimExternalID":429140584,"victimCorpName":"BABYLON 5.","victimAllianceName":"Babylon 5..","victimShipName":"Heron","victimShipClass":"Frigate","victimShipID":605,"FBPilotName":"Bender BRaU","FBCorpName":"Sacred Temple","FBAllianceName":"Out of Sight.","involvedPartyCount":1,"solarSystemName":"NRT4-U","solarSystemSecurity":-0.32698,"regionName":"Stain","ISK":2061020,"involved":[{"characterID":1592196699,"characterName":"Bender BRaU","corporationID":1406475932,"corporationName":"Sacred Temple","allianceID":99001011,"allianceName":"Out of Sight.","factionID":0,"factionName":"","securityStatus":5,"damageDone":675,"finalBlow":1,"weaponTypeID":3170,"shipTypeID":606}],"items":{"destroyed":[],"dropped":[{"typeName":"Cynosural Field Generator I","typeID":21096,"itemSlot":"1","qtyDropped":1,"qtyDestroyed":0}]},"eveKillID":14384295,"eveKillExternalID":"25294196","corpName":"BABYLON 5.","allianceName":"Babylon 5..","factionName":"None","shipDestroyed":"Heron","systemName":"NRT4-U","systemSecurity":-0.32698,"damageTaken":675,"involvedParties":[{"characterID":1592196699,"characterName":"Bender BRaU","corporationID":1406475932,"corporationName":"Sacred Temple","allianceID":99001011,"allianceName":"Out of Sight.","factionID":0,"factionName":"","securityStatus":5,"damageDone":675,"finalBlow":1,"weaponTypeID":3170,"shipTypeID":606}]}]'

    def test_getURL_without_changes(self):
        """
        Tests that the default url is correct
        """
        self.assertEqual("%smask:0" % (self.defaultURL), self.EveKill.getURL())

    def test_adding_a_single_command(self):
        """
        Test that checks adding a single command acts correctly
        """
        self.EveKill.addCommand(EveKillCommands.MIN_KILL_ID,1)
        self.assertEqual("%smask:0/minKillId:1" % (self.defaultURL), self.EveKill.getURL())

    def test_adding_multiple_commands(self):
        """
        Test that adding multiple works correctly
        """
        self.EveKill.addCommand(EveKillCommands.MIN_KILL_ID,1)
        self.EveKill.addCommand(EveKillCommands.MAIL_LIMIT,500)
        self.assertEqual("%smask:0/minKillId:1/mailLimit:500" % (self.defaultURL), self.EveKill.getURL())

    def test_removing_a_command_works(self):
        """
        Test that removing a command works
        """
        self.EveKill.addCommand(EveKillCommands.MIN_KILL_ID,1)
        self.EveKill.removeCommand(EveKillCommands.MIN_KILL_ID,1)
        self.assertEqual("%smask:0" % (self.defaultURL),self.EveKill.getURL())

    def test_adding_a_mask_gets_added_to_the_url(self):
        """
        Test that adding a mask works correctly
        """
        self.EveKill.addEveKillMask(EveKillMask.KILLURL)
        self.assertEqual("%smask:1" % (self.defaultURL),self.EveKill.getURL())

    def test_adding_multiple_masks_gets_added_to_the_url(self):
        """
        Test that adding multiple masks works correctly
        """
        self.EveKill.addEveKillMask(EveKillMask.KILLURL)
        self.EveKill.addEveKillMask(EveKillMask.TIMESTAMP)
        self.assertEqual("%smask:3" % (self.defaultURL),self.EveKill.getURL())

    def test_kills_get_returned(self):
        """
        Test that adding multiple masks works correctly
        """

        m = mox.Mox()
        m.StubOutWithMock(urllib, 'urlopen')
        urllib.urlopen('http://eve-kill.net/epic/mask:0').AndReturn(StringIO(self.mockOneKill))
        m.ReplayAll()

        killMail = self.EveKill.getKills()[0]
        self.assertEqual('http://eve-kill.net/?a=kill_detail&kll_id=14384295', killMail.url)
        self.assertEqual('2012-08-19 16:19:00', killMail.timestamp)
        self.assertEqual(14384295, killMail.internalId)
        self.assertEqual(25294196, killMail.externalId)
        self.assertEqual('Traktorustos', killMail.victimName)
        self.assertEqual(429140584, killMail.victimExternalId)
        self.assertEqual('BABYLON 5.', killMail.victimCorpName)
        self.assertEqual('Babylon 5..', killMail.victimAllianceName)
        self.assertEqual('Heron', killMail.victimShipName)
        self.assertEqual('Frigate', killMail.victimShipClass)
        self.assertEqual(605, killMail.victimShipId)
        self.assertEqual('Bender BRaU',killMail.fbPilotName)
        self.assertEqual('Sacred Temple',killMail.fbCorpName)
        self.assertEqual('Out of Sight.',killMail.fbAllianceName)
        self.assertEqual(1,killMail.involvedPartyCount)
        self.assertEqual('NRT4-U',killMail.solarSystemName)
        self.assertEqual('Stain',killMail.regionName)
        self.assertEqual(2061020,killMail.isk)
        self.assertEqual(1592196699, killMail.involvedParties[0].characterId)
        self.assertEqual(21096, killMail.itemsDropped[0].typeId)


    def test_pilot_is_correctly_populated(self):
        involvedParty = self.EveKill.mapJSONtoPilot(json.loads('{"characterID":1592196699,"characterName":"Bender BRaU","corporationID":1406475932,"corporationName":"Sacred Temple","allianceID":99001011,"allianceName":"Out of Sight.","factionID":0,"factionName":"","securityStatus":5,"damageDone":675,"finalBlow":1,"weaponTypeID":3170,"shipTypeID":606}'))
        self.assertEqual(1592196699,involvedParty.characterId)
        self.assertEqual("Bender BRaU",involvedParty.characterName)
        self.assertEqual(1406475932,involvedParty.corporation.corporationId)

    def test_corporation_is_correctly_populated(self):
        corporation = self.EveKill.mapJSONPilotToCorporation(json.loads('{"characterID":1592196699,"characterName":"Bender BRaU","corporationID":1406475932,"corporationName":"Sacred Temple","allianceID":99001011,"allianceName":"Out of Sight.","factionID":0,"factionName":"","securityStatus":5,"damageDone":675,"finalBlow":1,"weaponTypeID":3170,"shipTypeID":606}'))
        self.assertEqual(1406475932, corporation.corporationId)
        self.assertEqual("Sacred Temple", corporation.corporationName)
        self.assertEqual(99001011, corporation.alliance.allianceId)

    def test_corporation_is_correctly_populated(self):
        alliance = self.EveKill.mapJSONPilotToAlliance(json.loads('{"characterID":1592196699,"characterName":"Bender BRaU","corporationID":1406475932,"corporationName":"Sacred Temple","allianceID":99001011,"allianceName":"Out of Sight.","factionID":0,"factionName":"","securityStatus":5,"damageDone":675,"finalBlow":1,"weaponTypeID":3170,"shipTypeID":606}'))
        self.assertEqual(99001011, alliance.allianceId)
        self.assertEqual("Out of Sight.", alliance.allianceName)

    def test_item_is_correctly_populated(self):
        item = self.EveKill.mapJSONtoItem(json.loads('{"typeName":"test destroyed","typeID":9999,"itemSlot":"1","qtyDropped":2,"qtyDestroyed":0}'))
        self.assertEqual('test destroyed', item.typeName)
        self.assertEqual(9999, item.typeId)
        self.assertEqual(1, item.itemSlot)
        self.assertEqual(2, item.qnty)


