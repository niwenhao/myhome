ls -1d myhome/_* | while read f; do ln -s $f .${f#*_}; done

setw synchronize-panes on
