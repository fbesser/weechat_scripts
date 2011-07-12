# load_avg.py: Displays load in statusbar
#
# Put [load] in weechat.bar.status.items to view it in your statusbar
# Possible Values for items are 1, 5, 15 and all

# Version 0.1:
# Just working under Linux for now.

SCRIPT_NAME = "load_avg"
SCRIPT_AUTHOR = "Banton"
SCRIPT_VERSION = "0.1"
SCRIPT_LICENSE = "GPL"
SCRIPT_DESC = "Displays load in statusbar"

settings = {
        "items"           : "3",
}


weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, "", "")

#def color_load(load):
    #if load < 0.3:
        #return "%s%s" % (weechat.color(), load)
    #if 0.3 < load > 0.6:

    #return load

def load_item(data, item, window):
    loadproc = open("/proc/loadavg")
    load_data = loadproc.read().split(" ")
    loadproc.close()
    first_load = load_data[0]
    second_load = load_data[1]
    third_load = load_data[2]
    return "%s %s %s" % (load_data[0], load_data[1], load_data[2])


def load_timer(data, calls):
    weechat.bar_item_update('load')
    return weechat.WEECHAT_RC_OK

if weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, "", ""):


weechat.bar_item_new('load', 'load_item', '')
weechat.bar_item_update('load')
weechat.hook_timer(1000*20, 0, 0, 'load_timer', '')

