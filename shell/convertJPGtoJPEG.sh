for i in *.jpg ; do convert "$i" "${i%.*}.JPEG" ; rm "$i"; done
