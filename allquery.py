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
# (this script requires WeeChat 0.3.0 or newer)
#
#

SCRIPT_NAME = "allquery"
SCRIPT_AUTHOR = "florianb"
SCRIPT_VERSION = "0.1"
SCRIPT_LICENSE = "GPL3"
SCRIPT_DESC = "Executes command on all irc query buffer"

SCRIPT_COMMAND = "allquery"

import_ok = True

try:
    import weechat
except ImportError:
    print('This script must be run under WeeChat.')
    print('Get WeeChat now at: http://www.weechat.org/')
    import_ok = False

try:
    import re
except ImportError, message:
    print('Missing package(s) for %s: %s' % (SCRIPT_NAME, message))
    import_ok = False

def allquery_command_cb(data, buffer, args):
    """ Callback for /allquery command """
    
    args = args.strip()
    if args == "":
        weechat.command("", "/help %s" % SCRIPT_COMMAND)
        return weechat.WEECHAT_RC_OK
    argv = args.split(" ")
    exe_server = ""
    if argv[0] == "-server":
        exe_server = argv[1]
        command = " ".join(argv[2::])
        #weechat.prnt('', command)
        #return weechat.WEECHAT_RC_OK
    else:
        command = args
    
    infolist = weechat.infolist_get("buffer", "", "")
    while weechat.infolist_next(infolist):
        if weechat.infolist_string(infolist, "plugin_name") == "irc":
            server, query = weechat.infolist_string(infolist, "name").split(".", 1)
            if weechat.buffer_get_string(
                    weechat.infolist_pointer(infolist, "pointer"),
                    "localvar_type") == "private":
                if exe_server is not None:
                    if server == exe_server:
                        #comm = re.sub(r'\$nick', query, args)
                        weechat.command(weechat.infolist_pointer(infolist, "pointer"), command)
                else:
                    comm = re.sub(r'\$nick', query, args)
                    weechat.command(weechat.infolist_pointer(infolist, "pointer"), comm)
    weechat.infolist_free(infolist)
    return weechat.WEECHAT_RC_OK

if __name__ == '__main__' and import_ok:
    if weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION,
                        SCRIPT_LICENSE, SCRIPT_DESC, "", ""):

        weechat.hook_command(SCRIPT_COMMAND, SCRIPT_DESC,
                             '[-server <server>] command <arguments>',
                             '   command: command executed in query buffers\n'
                             '     $nick: gets replaced by query buffer nick\n\n'
                             'Examples:\n'
                             '  close all query buffers:\n'
                             '    /' + SCRIPT_COMMAND + ' /buffer close\n'
                             '  msg to all query buffers:\n'
                             '    /' + SCRIPT_COMMAND + ' /say Hello\n'
                             '  notice to all query buffers:\n'
                             '    /' + SCRIPT_COMMAND + ' /notice $nick Hello',
                             '/%(commands)',
                             'allquery_command_cb', '')
