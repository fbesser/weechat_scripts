# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 by Florian Besser <fbesser@gmail.com
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
#
# Quick hack, to get to know hsignals 

import weechat

SCRIPT_NAME = "whois"
SCRIPT_AUTHOR = "Banton"
SCRIPT_VERSION = "0.1"
SCRIPT_LICENSE = "GPL3"
SCRIPT_DESC = "whois via mouse in chat area"

keys = { "@chat(irc.*):w": "hsignal:chat_whois;/cursor stop" }

def whois_hsignal(data, signa, myhash):
    if not myhash["_chat_line_nick"]:
        return weechat.WEECHAT_RC_OK

    whois = "/whois %s" % myhash["_chat_line_nick"]
    weechat.command(myhash["_buffer_name"], whois)
    return weechat.WEECHAT_RC_OK

weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE,
SCRIPT_DESC, "", "")

weechat.key_bind("cursor", keys)

weechat.hook_hsignal("chat_whois", "whois_hsignal", "")

