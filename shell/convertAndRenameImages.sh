# preparing CNN dataset 


if [ "$#" -ne 3 ]; then
  echo echo "Usage: [obj] [image_ext_from] [image_ext_to]"
  exit 1
fi

OBJ=$1
a=1
ext_1=$(printf ".%s" "$2")
ext_2=$(printf ".%s" "$3")


cd $OBJ
for i in *$ext_1 ; do 
	echo $i
	new_1=$(printf "%s_%05d.%s" "$OBJ" "$a" "$2") #04 pad to length of 5
	convert "$i" "${new_1%.*}.$3"
  	let a=a+1 ;
done

a=1
for i in *$ext_2 ; do 

	new_2=$(printf "%s_%05d.%s" "$OBJ" "$a" "$3") #04 pad to length of 5
	mv -i -- "$i" "$new_2"
	echo $new_2
	let a=a+1 ;
done

rm *$ext_1


