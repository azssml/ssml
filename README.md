Stupid Simple Mailing List
==========================

The Stupid Simple Mailing List software package is meant to provide a very
simple mailing list - subscribe/unsubscribe, archiving, moderation. It is
written in the Python language.


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
