#!/bin/bash
# -----------------------------------------------------------------------------
#
#                               build-weechat.sh
# 
# Author   : Florian Besser <fbesser@gmail.com>
# Datum   : 2011-09-08
# Version : 0.1
# Lizenz  : GPL3 
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
SRC_DIR=/home/floh/dev/weechat
BUILD_DIR=$SRC_DIR/build
WEECHAT_CONFIG=/home/floh/.weechat
CMAKE_OPTIONS="-DCMAKE_BUILD_TYPE=Debug -DPREFIX=/home/floh/usr -DPYTHON_EXECUTABLE=/usr/bin/python2 -DPYTHON_LIBRARY=/usr/lib/libpython2.7.so"

#export PATH="/usr/lib/ccache/bin/:$PATH"

# SCRIPT

cd $SRC_DIR
GIT_COMMIT=$(git rev-list --max-count=1 HEAD)
GIT_STATUS=$(git pull)

GIT_COMMIT_ACT=$(git rev-list --max-count=1 HEAD)
if [ "$GIT_COMMIT" = "$GIT_COMMIT_ACT" ]; then
    echo $GIT_STATUS
    git log --pretty=oneline -n 1
    exit 0
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
