#!/bin/bash -x

BASE=$0
BASE=${BASE%/*}

ls -1d ${BASE}/_* | while read f; do ln -s $f .${f#*_}; done

sudo aptitude install -y build-essential
sudo aptitude install -y libsqlite3-dev
sudo aptitude install -y mysql-client
sudo aptitude install -y libmysqlclient-dev
sudo aptitude install -y vim
sudo aptitude install -y imagemagick
sudo aptitude install -y libmagick-dev
sudo aptitude install -y libmagickcore-dev
sudo aptitude install -y libmagickwand-dev
sudo aptitude install -y pkg-config
sudo aptitude install -y curl
sudo aptitude install -y net-tools
sudo aptitude install -y locales
sudo aptitude install -y locales-all
sudo aptitude install -y git
sudo aptitude install -y procps
sudo aptitude install -y libssl-dev
sudo aptitude install -y libreadline-dev
sudo aptitude install -y zlib1g-dev
sudo aptitude install -y ncurses-dev

git clone https://github.com/rbenv/rbenv.git .rbenv
git clone https://github.com/rbenv/ruby-build.git ~/.rbenv/plugins/ruby-build


#setw synchronize-panes on
