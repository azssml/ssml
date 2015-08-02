Stupid Simple Mailing List
==========================

The Stupid Simple Mailing List software package is meant to provide a very
simple mailing list - subscribe/unsubscribe, archiving, moderation. It is
written in the Python language.


Motivation
----------

Why write 'yet another mailing list' package? Simple; I needed something that
could be configured quickly on any python enabled system and could fetch mail
from an exchange server, forward it around, and do basic mailing list stuff.

``Mailman`` is the premier package in this realm. It's so good that most folks
grin and bear it with the nightmare that is postfix and sendmail configurations
to just do simple IMAP fetch and forward. I'd love to say that I'm patient
enough to get all the various pieces configured. I'm not. Further, the place
where this will be used doesn't have enough people in IT support to be able to
maintain such a system. Simpler == better, in my opinion.


Setup
-----

To setup a mailing list, edit an INI file which will take the form

   [listname]
   imapserver=IMAP-SERVERADDR
   imapuser=IMAP-USERNAME
   imappass=IMAP-PASSWORD
   smtpserver=SMTP-SERVERADDR
   smtpuser=SMTP-USERNAME
   smtppass=SMTP-PASSWORD
   userlist=/path/to/userlist

The above minimal config will tell the *MailForwarder.Forward* object to log in
to IMAP-SERVERADDR with the supplied credentials, scan the INBOX for unseen
messages, and process those messages by updating, and forwarding to the
addresses listed in */path/to/userlist*. It's important to note that the entries
in */path/to/userlist* should be email addresses, one per line.



Running
-------

To invoke the engine, use **/path/to/MailForwarder /path/to/config mlist**
either manually, or by using a cronjob set to periodically run.



Web Archives
------------

As a todo, I'll be enhancing the script to be able to intelligently use the
``mhonarc`` package, converting emails to threaded views as static HTML pages.
