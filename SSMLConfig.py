#!/usr/bin/env python

"""Configuration loader / storage for SSML"""

import ConfigParser

__authors__   = ["Aaron Conole"]
__copyright__ = "Copyright 2015, Aaron Conole"
__credits__   = ["Aaron Conole"]
__license__   = "GPL"
__version__   = "0.1"
__email__     = "aaron@bytheb.org"
__status__    = "Development"


class NoConfigFileSpecified(Exception):
    pass

class NoMailingListInConfigFile(Exception):
    pass

class MissingUserListConfig(Exception):
    pass

class MissingIMAPServerConfig(Exception):
    pass

class MissingSMTPServerConfig(Exception):
    pass

class MissingIMAPUserConfig(Exception):
    pass

class MissingIMAPPassConfig(Exception):
    pass

class ConfigFile(object):
    def __init__(self, maillist, filename):
        if filename is None or filename is '':
            raise NoConfigFileSpecified

        self.section = maillist

        self.config = ConfigParser.ConfigParser()
        self.config.read(filename)

        if self.section not in self.config.sections():
            raise NoMailingListInConfigFile

    def __repr__(self):
        srepr = "[%s]\n" % self.section
        
        for ItemName,ItemVal in self.config.items(self.section):
            srepr += "%s: %s\n" % (ItemName, ItemVal)

        return srepr

    def FindOptionValue(self, OptionName):
        for option in self.config.options(self.section):
            if option.lower() == OptionName.lower():
                return self.config.get(self.section, OptionName)

        return None

    def GetUserList(self):
        ret = self.FindOptionValue("userlist")
        if ret is None:
            raise MissingUserListConfig

        return ret

    def GetDelete(self):
        ret = self.FindOptionValue("expunge")
        if ret is None or ret.lower() == "false":
            return False
        
        return True

    def GetIMAPServer(self):
        ret = self.FindOptionValue("imapserver")
        if ret is None:
            raise MissingIMAPServerConfig

        return ret

    def GetIMAPServerPort(self):
        return self.FindOptionValue("imapport")
        
    def GetIMAPUser(self):
        ret = self.FindOptionValue("imapuser")
        if ret is None:
            raise MissingIMAPUserConfig

        return ret

    def GetIMAPPass(self):
        ret = self.FindOptionValue("imappass")
        if ret is None:
            raise MissingIMAPPassConfig

        return ret
        
    def GetIMAPMailbox(self):
        ret = self.FindOptionValue("imapbox")
        if ret is None:
            ret = "INBOX"

        return ret
        
    def SubjectPrefix(self):
        ret = self.FindOptionValue("subjpref")
        if ret is None:
            ret = self.section
        
        return ret

    def GetSMTPServer(self):
        ret = self.FindOptionValue("smtpserver")
        if ret is None:
            raise MissingSMTPServerConfig
            
        return ret

    def GetSMTPServerPort(self):
        ret = self.FindOptionValue("smtpport")
        if ret is None:
            ret = "587"
        return ret

    def GetSMTPUser(self):
        return self.FindOptionValue("smtpuser")

    def GetSMTPPass(self):
        return self.FindOptionValue("smtppass")

    def GetOutdirConfig(self):
        return self.FindOptionValue("outdir")
        
