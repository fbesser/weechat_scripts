# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 by Florian Besser <fbesser@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

#
# (this script requires WeeChat 0.3.6 or newer)

import weechat,re

SCRIPT_NAME = "high_lines"
SCRIPT_AUTHOR = "Banton"
SCRIPT_VERSION = "0.1"
SCRIPT_LICENSE = "GPL3"
SCRIPT_DESC = "high_lines:Highlight entire line"

weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, "", "")


def modify(data, signal, signal_data, string):
    if not "irc_privmsg" in signal_data:
        return string
    plugin, buffer_name, tags = signal_data.split(";")
    server, channel = buffer_name.split(".", 1)
    prefix, msg = string.split("\t")
    nick = weechat.info_get("irc_nick", server)
    #highcolor = weechat.config_color(weechat.config_get("weechat.color.chat_highlight"))
    if nick in msg:
        weechat.string_remove_color(string, "")
        return "%s\t%s%s" % (prefix, weechat.color('chat_highlight'), msg)
    return string 
    


weechat.hook_modifier("weechat_print", "modify", "")
