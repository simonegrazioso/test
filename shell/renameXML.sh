# preparing CNN dataset 

OBJ=hand
a=66
cd annotations/n00007846
for i in *.xml ; do 
	new=$(printf "%s_%05d.xml" "$OBJ" "$a") #04 pad to length of 5
	mv -i -- "$i" "$new"
  	let a=a+1 ;
done

