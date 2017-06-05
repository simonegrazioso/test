# preparing CNN dataset 

OBJ=hand
a=233
cd hand2
for i in *.jpg ; do 
	new=$(printf "%s_%05d.jpg" "$OBJ" "$a") #04 pad to length of 5
	convert "$i" -resize 800x600 "${new%.*}.JPEG"
  	let a=a+1 ;
done

rm *.jpg

