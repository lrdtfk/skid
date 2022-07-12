#!/usr/bin/env bash

# bash <(wget -qO- https://raw.githubusercontent.com/lrdtfk/skid/main/dotfiles.sh)


git clone --bare git@github.com:lrdtfk/.dotfiles.git $HOME/.dotfiles &> /dev/null

function config {
   /usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME $@
}


config checkout &> /dev/null
if [ $? = 0 ]; then
  echo "Checked out config.";
  else
    echo "removing pre-existing dot files.";
    config checkout 2>&1 | egrep "\s+\." | awk {'print $1'} | xargs -I{} rm -rf {}
fi;
config checkout &> /dev/null
config config status.showUntrackedFiles no

curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
