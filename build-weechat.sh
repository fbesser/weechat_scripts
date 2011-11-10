#!/bin/bash
# -----------------------------------------------------------------------------
#
#                               build-weechat.sh
# 
# Author  : Florian Besser <fbesser@gmail.com>
# Date    : 2011-09-08
# Version : 0.1
# License : GPL3
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

# Usage:
# build-weechat [-v] [-w] [-u] [-f][-i <install dir>]
#
#               -v : make output verbode
#               -w : write weechat config of running weechat before UPGRADE
#               -u : upgrade running weechat after make install
#               -f : force compilation, even if there is nothing to update
# -i <install dir> : install weechat into <install dir>
#

# History:
# DATE:
#     version 0.2: added commandline arguments (-s, -v, -i)
#                  added git clone if SRC_DIR not exists
# 2011-09-08 
#     version 0.1: script created
#   
#                                 ~~~\\://~~~
#                                 ~~~\¸·¸/~~~
#                                   @ 0 0 @
#------------------------------oOOo---(¸)---oOOo-----------------------------
#Options
SRC_DIR=/home/floh/dev/weechat
BUILD_DIR=$SRC_DIR/build
WEECHAT_CONFIG=/home/floh/.weechat
INSTALL_DIR=/home/floh/usr

CMAKE_OPTIONS="-DCMAKE_BUILD_TYPE=Debug -DPYTHON_EXECUTABLE=/usr/bin/python2 -DPYTHON_LIBRARY=/usr/lib/libpython2.7.so"

FORCE=false
VERBOSE=false
SAVE=false
UPGRADE=false
GIT_REPO="git://git.sv.gnu.org/weechat.git"
WEECHAT_FIFO=($WEECHAT_CONFIG/weechat_fifo_*)
# SCRIPT


HELP="Usage:\n
 $0 [-v] [-w] [-u] [-f] [-i <install dir>]\n
\n
               -v : make output verbode\n

               -w : write weechat config of running weechat before UPGRADE\n
               -u : upgrade running weechat after make install\n
               -f : force compilation, even if there is nothing to update\n
 -i <install dir> : install weechat into <install dir>\n"

while getopts ":vwufhi:" flag
do
  case  $flag in
    v) VERBOSE=true;;
    w) SAVE=true;;
    u) UPGRADE=true;;
    i) INSTALL_DIR=$OPTARG;;
    f) FORCE=true;;
    h) echo $HELP
        exit 0;;
    \?) echo "Unbekannte Option: -$OPTARG. $0 -h für Hilfe"
        exit 1;;
    :) echo "Option: -$OPTARG verlangt ein Argument. $0 -h für Hilfe"
        exit 1;;
  esac
done
shift $((OPTIND-1))

CMAKE_OPTIONS="-DPREFIX=$INSTALL_DIR $CMAKE_OPTIONS"

if [ ! -d $SRC_DIR ]; then
    git clone $GIT_REPO $SRC_DIR
    cd $SRC_DIR
else
    cd $SRC_DIR
    GIT_COMMIT=$(git rev-list --max-count=1 HEAD)
    GIT_STATUS=$(git pull)

    GIT_COMMIT_ACT=$(git rev-list --max-count=1 HEAD)
    if [ "$GIT_COMMIT" = "$GIT_COMMIT_ACT" ]; then
        echo $GIT_STATUS
        if $VERBOSE ; then
            git log --pretty=oneline -n 1
        fi
        if ! $FORCE ; then
            exit 0
        fi
    fi
fi

if $VERBOSE ; then
    git log --pretty=oneline $GIT_COMMIT..$GIT_COMMIT_ACT
fi

if [ ! -d $BUILD_DIR ]; then
  mkdir -p $BUILD_DIR
fi

cd build

cmake .. $CMAKE_OPTIONS || exit 1 
make
if [ $? -ne 0 ]; then
    echo "Fehler in make"
    exit 1
fi

make install
if [ -e $WEECHAT_FIFO ];then
    if  $SAVE ;then
        echo -e "*/save" >$WEECHAT_FIFO

    fi
    if $UPGRADE ;then
        echo -e "*/upgrade" > $WEECHAT_FIFO
    fi
fi
exit 0
