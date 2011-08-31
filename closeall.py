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
# (this script requires WeeChat 0.3.0 or newer)
#
#

import weechat

SCRIPT_NAME = "closeall"
SCRIPT_AUTHOR = "florianb"
SCRIPT_VERSION = "0.1"
SCRIPT_LICENSE = "GPL3"
SCRIPT_DESC = "Closes all buffers that don't start with a certain char"

settings = {
        "channel_prefix"           : "#&",
}
def closeall_query():
    """ Closes all IRC Buffers which do not start with channel_prefix """

    infolist = weechat.infolist_get("buffer", "", "")
    while weechat.infolist_next(infolist):
        if weechat.infolist_string(infolist, "plugin_name") == "irc":
            pref = tuple(weechat.config_get_plugin("channel_prefix").split(","))
            channel = weechat.infolist_string(infolist, "name").split(".", 1)
            if not channel[1].startswith(pref) and channel[0] != "server":
                weechat.command('', '/buffer close irc.%s.%s' % (channel[0], channel[1]))
    weechat.infolist_free(infolist)

    return weechat.WEECHAT_RC_OK

def closeall_command_cb(data, buffer, args):
    """ Callback for /closeall """
    argv = args.strip().split(" ", 1)
    if argv[0] == "query":
        closeall_query()

    return weechat.WEECHAT_RC_OK

if weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, "", ""):
    
    for option, default_value in settings.iteritems():
        if not weechat.config_is_set_plugin(option):
            weechat.config_set_plugin(option, default_value)
    weechat.hook_command('closeall', SCRIPT_DESC, 'query', '', '', 'closeall_command_cb', '')
