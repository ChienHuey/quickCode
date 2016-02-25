#!/bin/bash
# script to create a branch for each subdirectory
# assumptions:
#	- directories either have sub-directories or files, not both
#
# @param	 
function traverse_directory() {
# track which directory we're in
cur_dir=$1
for entry in *
do
	echo "cur_dir:" $cur_dir
	echo "entry:" $entry
	subdircount=`find "${cur_dir}/$entry" -maxdepth 1 -type d | wc -l`
	echo "number of subdirs:" $subdircount
	# do nothing if it's a file
	if [ -f "${entry}" ]; then
		echo "it's a file"
		break
	fi
	# if there are no subdirectories, then create a branch
	if [ "$subdircount" -le 1 ] ; then
		echo "no subdirectories"
		git branch "${entry}"
		git checkout "${entry}"
		git add "${entry}"/*.vcl
		git commit -m '"${entry}" commit'
		git push --set-upstream origin "${entry}"
		git checkout master
	# recurse if it's a directory
	else
		echo "go to subdirectory"
		echo "entry:" $entry
		cd $entry
		cur_dir=$(pwd)
		echo "cur_dir:" $cur_dir
		echo "inside directory call ${cur_dir}"
		traverse_directory "${cur_dir}"
		cd ..
		cur_dir=$(pwd)
	fi
done
}

traverse_directory $1