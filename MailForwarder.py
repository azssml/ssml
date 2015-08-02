#!/usr/bin/env python

"""A simple tool to fetch and forward mail

The MailForwarder module exists to read mail messages, forward them on to the
group, and finally resubmit them to a month/year separated mailbox in mbox 
format"""

import sys
import datetime
import imaplib
import smtplib
import mailbox

from email.parser import Parser
from email.utils import parseaddr

from SSMLConfig import ConfigFile

__authors__   = ["Aaron Conole"]
__copyright__ = "Copyright 2015, Aaron Conole"
__credits__   = ["Aaron Conole"]
__license__   = "GPL"
__version__   = "0.1"
__email__     = "aaron@bytheb.org"
__status__    = "Development"

class Forwarder(object):

    def __init__(self, mailinglist, configfile):
        self.users = []

        self.Config = ConfigFile(mailinglist, configfile)

        ### Port argument seems to fail.. 
        ### TODO: look into the port argument
        self.mail = imaplib.IMAP4_SSL(self.Config.GetIMAPServer())

        try:
            self.mail.login(self.Config.GetIMAPUser(), self.Config.GetIMAPPass())
        except:
            self.mail = None
            print "Unable to log in"
            return

        self.mail.select(self.Config.GetIMAPMailbox())

        try:
            [self.users.append(line.rstrip('\n')) for line in open(self.Config.GetUserList())]
        except IOError:
            self.mail = None
            print "Bad user data text file"
            return
        
        self.mbox = None

    def SaveUserList(self):
        try:
            open(self.Config.GetUserList(), "w").writelines(["%s\n" % user for user in self.users])
        except IOError:
            print "Bad user data text file"

    def Unsubscribe(self, mail):

        try:
            mailaddr = parseaddr(mail['from'])[1]
            if mailaddr in self.users:
                self.users.remove(mailaddr)
        except:
            pass

        self.SaveUserList()

    def Subscribe(self, mail):
        
        try:
            mailaddr = parseaddr(mail['from'])[1]

            if mailaddr not in self.users:
                self.users.append(mailaddr)
        except:
            pass

        self.SaveUserList()

    def ProcessEmail(self, mail):

        mailaddr = parseaddr(mail['from'])[1]

        if mailaddr not in self.users:
            print "Will not forward from addr %s" % mailaddr
            return

        if self.Config.GetOutdirConfig() is not None:
            d = datetime.datetime.now()
            mboxname = self.Config.GetOutdirConfig() + '/' + d.strftime("%Y-%m") + ".mbox"
            mbox = mailbox.mbox(mboxname)
            mbox.lock()
            mbox.add(mail)
            mbox.unlock()

        print "Connecting..."
        s = smtplib.SMTP(self.Config.GetSMTPServer(), self.Config.GetSMTPServerPort())
        print "Connected..."
        s.starttls()
        print "TLS..."
        s.login(self.Config.GetSMTPUser(), self.Config.GetSMTPPass())
        print "Logged in..."
        subj = mail['subject'].lower()
        expectedprefix = "[%s]" % self.Config.SubjectPrefix()
        
        if expectedprefix not in subj:
            subj = expectedprefix + " " + subj
            del mail['subject']
            del mail['Subject']
            mail['Subject'] = subj

        for user in self.users:
            print "Sending mail to: %s" % user
            s.sendmail(mail['from'], user, mail.as_string())
            print "Sent"


    def FetchMail(self):

        delete_ids = []

        # Handle unsubscribe requests
        result, data = self.mail.search(None, '(UNSEEN SUBJECT "unsubscribe")')
        if result.lower() == "ok":
            ids = data[0].split()
            for eml in ids:
                result, maildata = self.mail.fetch(eml, '(RFC822)')
                if result.lower() == "ok":
                    self.Unsubscribe(Parser().parsestr(maildata[0][1]))
                    delete_ids.append(eml)


        # Handle subscribe requests
        result, data = self.mail.search(None, '(UNSEEN SUBJECT "subscribe")')
        if result.lower() == "ok":
            ids = data[0].split()
            for eml in ids:
                result, maildata = self.mail.fetch(eml, '(RFC822)')
                if result.lower() == "ok":
                    self.Subscribe(Parser().parsestr(maildata[0][1]))
                    delete_ids.append(eml)

        try:
            result, data = self.mail.uid('search', None, "(UNSEEN)")
            ids = [x for x in data[0].split(' ') if x != '']
            for eml in ids:
                result, maildata = self.mail.uid('FETCH', eml, '(BODY[])')
                if result.lower() == "ok":
                    if maildata[0] is not None:
                        self.ProcessEmail(Parser().parsestr(maildata[0][1]))
                        self.mail.store(eml, '+FLAGS', '(\Seen)')
                if self.Config.GetDelete():
                    self.mail.uid('STORE', eml, '+FLAGS', '(\Deleted)')
            if self.Config.GetDelete():
                self.mail.expunge()
        finally:
            print "Done..."

if __name__ == "__main__":
    iniPath=sys.argv[1]
    mlist=sys.argv[2]
    
    fwd = Forwarder(mlist, iniPath)
    fwd.FetchMail()

