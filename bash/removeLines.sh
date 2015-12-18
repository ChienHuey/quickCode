#!/bin/bash
# script that removes lines from files containing the regex expressions
#
# @param 			filename of file with regex to base removal of
#	@param			directory/file(s) to be processed, wildcards ok
#
search_fields_file=$1
array=($2)
echo "${arr[@]}"
while read search_field; do
	for file_to_parse in "${array[@]}"; do
		sed -i.bak "/$search_field/d" $file_to_parse
	done
done < $search_fields_file