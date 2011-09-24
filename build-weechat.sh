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
#                                 ~~~\\://~~~
#                                 ~~~\¸·¸/~~~
#                                   @ 0 0 @
#------------------------------oOOo---(¸)---oOOo-----------------------------

#Options
SRC_DIR=/home/floh/dev/weechattt
BUILD_DIR=$SRC_DIR/build
WEECHAT_CONFIG=/home/floh/.weechat
INSTALL_DIR=/home/floh/usr
CMAKE_OPTIONS="-DCMAKE_BUILD_TYPE=Debug -DPYTHON_EXECUTABLE=/usr/bin/python2 -DPYTHON_LIBRARY=/usr/lib/libpython2.7.so"
VERBOSE=0
SAVE=0
GIT_REPO="git://git.sv.gnu.org/weechat.git"
#export PATH="/usr/lib/ccache/bin/:$PATH"

# SCRIPT

# Kommandozeilen Argumente auswerten
while getopts ":vps" flag
do
  case $flag in
    v) VERBOSE=1;;
    s) SAVE=1;;
    i) INSTALL_DIR=$OPTARG;;
    \?) echo "Unbekannte Option: -$OPTARG. $0 -h für Hilfe"
        exit 1;;
    :) echo "Option: -$OPTARG verlangt ein Argument. $0 -h für Hilfe"
        exit 1;;
  esac
done
shift $((OPTIND-1))
CMAKE_OPTIONS="-DPREFIX=$INSTALL_DIR $CMAKE_OPTIONS"
if [ ! -d $SRC_DIR ]; then
    mkdir -p $SRC_DIR
    git clone $GIT_REPO $SRC_DIR
    cd $SRC_DIR
else
    cd $SRC_DIR
    GIT_COMMIT=$(git rev-list --max-count=1 HEAD)
    GIT_STATUS=$(git pull)

    GIT_COMMIT_ACT=$(git rev-list --max-count=1 HEAD)
    if [ "$GIT_COMMIT" = "$GIT_COMMIT_ACT" ]; then
        echo $GIT_STATUS
        git log --pretty=oneline -n 1
        exit 0
    fi
fi

git log --pretty=oneline $GIT_COMMIT..$GIT_COMMIT_ACT

if [ ! -d $BUILD_DIR ]; then
  mkdir -p $BUILD_DIR
fi

cd build

cmake .. $CMAKE_OPTIONS 
make
if [ $? -ne 0 ]; then
    echo "Fehler in make"
    exit 1
fi

make install

echo -e "*/upgrade" >$WEECHAT_CONFIG/weechat_fifo_$(ps -e | grep weechat-curses | awk '{print $1;}')

exit 0
