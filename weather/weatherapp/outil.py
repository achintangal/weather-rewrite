"""
This module contains the OnooUtil class. OnooUtil object sets up a connection
to Onionoo and hands out information about routers.

"""

import logging
import requests

class OnooUtil:
    
    """
    A class which hands of information about onion routers using
    documents obtained from Onionoo

    """
    
    def __init__(self,bandwidth_doc = bandwidth_doc):
    
        self.bandwidth_doc = bandwidth_doc
        
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






