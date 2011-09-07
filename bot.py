from jabberbot import JabberBot, botcmd
import datetime, urllib, json

class SystemInfoJabberBot(JabberBot):
    @botcmd
    def serverinfo( self, mess, args):
        """Displays information about the server"""
        version = open('/proc/version').read().strip()
        loadavg = open('/proc/loadavg').read().strip()

        return '%s\n\n%s' % ( version, loadavg, )
    
    @botcmd
    def time( self, mess, args):
        """Displays current server time"""
        return str(datetime.datetime.now())

    @botcmd
    def rot13( self, mess, args):
        """Returns passed arguments rot13'ed"""
        return args.encode('rot13')

    @botcmd
    def whoami(self, mess, args):
        """Tells you your username"""
        return mess.getFrom().getStripped()
 
    @botcmd
    def btc(self,mess,args):
        """Returns latest mtGox USD rate"""
        # Get a file-like object for the Python Web site's home page.
        f = urllib.urlopen('http://mtgox.com/api/0/data/ticker.php')
        # Read from the object, storing the page's contents in 's'.
        line=f.read();
        u=line.decode('utf-8');
        s = json.loads(u)
        last=str(s['ticker']['last'])
	last += ' USD'
#	self.send_tune(last, True)
        return last


username = 'bot@joip.de'
password = 'wurstsalat110*'
bot = SystemInfoJabberBot(username,password)
bot.serve_forever()

