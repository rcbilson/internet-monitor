#!/bin/bash

set -e

case $1 in
"start") sudo iptables --append OUTPUT --destination 8.8.8.8 --jump DROP ;;
*) sudo iptables --delete OUTPUT --destination 8.8.8.8 --jump DROP ;;
esac

sudo iptables --list
