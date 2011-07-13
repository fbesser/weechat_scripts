# load_avg.py: Displays load in statusbar
#
# Put [load] in weechat.bar.status.items to view it in your statusbar
# Possible Values for items are 1, 5, 15 and all

# Version 0.1:
# Just working under Linux for now.

import weechat

SCRIPT_NAME = "load_avg"
SCRIPT_AUTHOR = "Banton"
SCRIPT_VERSION = "0.1"
SCRIPT_LICENSE = "GPL3"
SCRIPT_DESC = "Displays load in statusbar"

settings = {
        "items"           : "all",
}



#def color_load(load):
    #if load < 0.3:
        #return "%s%s" % (weechat.color(), load)
    #if 0.3 < load > 0.6:

    #return load

def load_item(data, item, window):
    loadproc = open("/proc/loadavg")
    load_data = loadproc.read().split(" ")
    loadproc.close()
    config_items = weechat.config_get_plugin("items")
    first_load = load_data[0]
    second_load = load_data[1]
    third_load = load_data[2]
    if config_items == "1":
        return load_data[0]
    if config_items == "5":
        return load_data[1]
    if config_items == "15":
        return load_data[2]
    if config_items == "all":
        return "%s %s %s" % (load_data[0], load_data[1], load_data[2])



def load_timer(*args):
    weechat.bar_item_update('load')
    return weechat.WEECHAT_RC_OK

if weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, "", ""):
    
    for option, default_value in settings.iteritems():
        if not weechat.config_is_set_plugin(option):
            weechat.config_set_plugin(option, default_value)
    weechat.bar_item_new('load', 'load_item', '')
    weechat.bar_item_update('load')
    weechat.hook_timer(1000*20, 0, 0, 'load_timer', '')

