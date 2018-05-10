# remove greeting message
set fish_greeting

# fix locale for python and so on
set -x LC_ALL "en_US.UTF-8"
set -x LC_CTYPE "en_US.UTF-8"

# set appropriate umask (o=r+w,g=r)
umask 027
