# Author: Banton
#
#
#
#

import weechat,re

weechat.register("high_lines", "Banton", "0.0.2", "GPL", "high_lines:Highlight entire line", "", "")

def modify(data, signal, signal_data, string):
    if not "irc_privmsg" in signal_data:

        return string
    list=signal_data.split(";")
    server = list[1].split(".")
    msg = string.split("\t")
    nick = weechat.info_get("irc_nick", server[0])
    #highcolor = weechat.config_color(weechat.config_get("weechat.color.chat_highlight"))
    if nick in msg[1]:
        weechat.string_remove_color(string, "")
        return "%s\t%s%s" % (msg[0], weechat.color('chat_highlight'), msg[1])
    return string 
    


weechat.hook_modifier("weechat_print", "modify", "")
