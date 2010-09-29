// $Id: ConfigEntry.java 6843 2005-07-14 20:26:11Z nickm $
// Copyright 2005 Nick Mathewson, Roger Dingledine
// See LICENSE file for copying information
package net.freehaven.tor.control;

/** A single key-value pair from Tor's configuration. */
public class ConfigEntry {
    public ConfigEntry(String k, String v) {
        key = k;
        value = v;
    }
    public final String key;
    public final String value;
}
