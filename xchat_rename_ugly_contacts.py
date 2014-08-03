__module_name__ = "Rename Facebook and Google Talk (or Hangouts whatever) Contacts" 
__module_version__ = "0.1" 
__module_description__ = "Rename Bitlbee Facebook contacts to the name they have on Facebook (http://hofnar.ro)" 

import xchat 

# this function renames the ugly name
def rename_name(word, word_eol, userdata):
    # get the facebook name from whois, decode with string-escape, decode as utf-8,
    # encode to ascii and trim all spaces so you get the final name
    name = word[3].decode('string-escape').decode("utf-8").encode("ascii","ignore").replace(" ", "")
    # issue a command on channel &bitlbee to rename the ugly name to the new name
    xchat.command("msg &bitlbee rename %s %s" % (word[0], name))
    # unhooking (use global variable)
    global rename_hook
    # if there is a hook
    if rename_hook is not None:
        # unhook
        xchat.unhook(rename_hook)
        # and set to None
        rename_hook = None
    # catch this print in other windows or something
    return xchat.EAT_ALL

# this function will be called on join
def on_join(word, word_eol, userdata):
    # use global variable for unhooking
    global rename_hook
    # for comfort instead of word[0], word[1] and word[2]
    triggernick, triggerchannel, triggerhost = word
    # get the context
    destination = xchat.get_context()
    # if the channel is bitlbees channel and the nick begins with a dash
    if ((triggerchannel == "&bitlbee") and ((triggernick[0] == "-") or (triggernick[0] == "_"))):
        # send a whois on the nick
        xchat.command("whois %s" % triggernick)
        # make a handler that hooks the Name Line of the whois and calls rename_name with this line
        rename_hook = xchat.hook_print("Whois Name Line", rename_name)
        # unhook the whois
    return

# this hooks on Join
xchat.hook_print('Join', on_join)
