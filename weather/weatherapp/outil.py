"""
This module contains the OnooUtil class. OnooUtil object sets up a connection
to Onionoo and hands out information about routers.

"""

import logging
import requests
import json
import string
import re

## CONSTANTS ##
UNPARSABLE = 'unparsable-mail.log'


def deobfuscate_mail(contact):
    """
    Parse the email address from an individual router descriptor string.

    @type contact: str
    @param contact: Email address from the server descriptor.
    @rtype: str
    @return: The email address in desc. If the email address cannot be
    parsed, the empty string.
    """

    punct = string.punctuation
    clean_line = contact.replace('<', '').replace('>', '')

    email = re.search('[^\s]+'
                      '(?:@|[' + punct + '\s]+at[' + punct + '\s]+).+'
                      '(?:\.|[' + punct + '\s]+dot[' + punct + '\s]+)[^\n\s\)\(]+',
                      clean_line, re.IGNORECASE)

    if email is None or email == "":
        logger.debug("Couldn't parse an email address from line:\n%s" % contact)
        unparsable = open(UNPARSABLE, 'a')
        unparsable.write(contact.encode('utf-8') + '\n')
        unparsable.close()
        email = ""
    else:
        email = email.group()
        email = email.lower()
        email = re.sub('[' + punct + '\s]+(at|ta)[' + punct + '\s]+', '@', email)
        email = re.sub('[' + punct + '\s]+(dot|tod|d0t)[' + punct + '\s]+', '.', email)
        email = re.sub('[' + punct + '\s]+hyphen[' + punct + '\s]+', '-', email)

    return email



class OUtil:
    
    """
    A class which hands of information about onion routers using
    documents obtained from Onionoo

    """
    
    def __init__(self,document):
    
        self.bandwidth_doc = json.loads(document)
        
    def is_up_or_hibernating(self,fingerprint):
        
        """
        Checks if the router in up or hibernating 
        """
        
        for relay in self.bandwidth_doc["relays"]:
            if relay["fingerprint"] == fingerprint:
                return True
                
        return False
        
    def get_finger_name_list(self):
        """
        Returns list of router tuples (fingerprint,nickname)
        """
        
        relays=[]
        for relay in self.bandwidth_doc["relays"]:
            if relay["fingerprint"]:
                relays.append((relay["fingerprint"], relay["nickname"]))
        return relays
        
    def is_stable(self, fingerprint):

        """ 
        Checks if the relay is stable or not
        """
        
        for relay in self.bandwidth_doc["relays"]:
            if relay["fingerprint"] == fingerprint:
                if "Stable" in relay["flags"]:
                    return True
                return False

    def is_exit(self,fingerprint):
        
        for relay in self.bandwidth_doc["relays"]:
            if relay["fingerprint"] == fingerprint:
                if "Exit" in relay["flags"]:
                    return True
                return False

    def is_recommended_version(self, fingerprint):
        """
        Checks if a relay is running the recomended version
        of tor
        """
        
        for relay in self.bandwidth_doc["relays"]:
            if relay["fingerprint"] == fingerprint:
                if relay["recommended_version"]:
                    return True
                return False 
    
    
    def get_observed_bandwidth(self, fingerprint):
        """
        Gets the observed bandwidth of router
        """
        
        for relay in self.bandwidth_doc["relays"]:
            if relay["fingerprint"] == fingerprint:
                return relay["observed_bandwidth"]


    def get_contact(self,fingerprint):
        """
        returns contact information
        """
        for relay in self.bandwidth_doc["relays"]:
            if relay["fingerprint"] == fingerprint:
                return deobfuscate_mail(relay["contact"])
                
        return None
