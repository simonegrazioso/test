# preparing CNN dataset 

OBJ=hand
a=233
cd hand2
for i in *.JPEG ; do 
	new=$(printf "%s_%05d.JPEG" "$OBJ" "$a") #04 pad to length of 5
	mv -i -- "$i" "$new"
  	let a=a+1 ;
done

#rm *.jpg


#renaming
#a=1
#for i in *.jpg; do
#  new=$(printf "%04d.jpg" "$a") #04 pad to length of 4
#  mv -i -- "$i" "$new"
#  let a=a+1
#done
