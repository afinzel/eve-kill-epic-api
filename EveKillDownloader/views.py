
from django.http import HttpResponse
from EveKillDownloader import EveKillMask, EveKillCommands
from EveKillDownloader.EveKill import EveKill

def home(request):
    eveKill = EveKill()
    eveKill.addEveKillMask(EveKillMask.VICTIM_SHIP_NAME)
    eveKill.addEveKillMask(EveKillMask.ITEMS_DROPPED)
    eveKill.addCommand(EveKillCommands.MAIL_LIMIT,500)
    return HttpResponse(eveKill.getURL())

#    url = "http://eve-kill.net/?a=idfeed&pilotname=DocD2";
#    eveFeed = urllib.urlopen(url);
#
#
#    root = etree.fromstring(eveFeed.read());
#    context = etree.iterparse(BytesIO(eveFeed.read().encode("utf-8")));
#    for action, elem in context:
#        if not elem.text:
#            text = "None"
#        else:
#            text = elem.text
#        print elem.tag + " => " + text
#
#    return HttpResponse(eveFeed) ;







