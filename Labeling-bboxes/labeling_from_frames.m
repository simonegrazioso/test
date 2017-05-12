framesdir = 'PATH_TO_FRAMES_DIR';

N = dir(framesdir);
N = N(3:end);

Object = 'n0003242'; #class label

for jj=1:length(N)
    counter = 0;
    bbox = zeros(1,4);
    filename = strcat(framesdir,N(jj).name);
    frame = imread(filename);
    imshow(frame);
    str = N(jj).name;
    fprintf('FILE n°%d di %d: %s\n',jj,length(N),str);
    str = strrep(str,'.JPEG','');
    filestr = sprintf('%s', str);
    %frameName = [framesdir sprintf('%s.jpg',filestr)];
    %saveas(gcf,frameName,'jpg');
    width = size(frame,2);
    height = size(frame,1);
    depth = size(frame,3);
    while bbox(3)<=0 || bbox(4)<=0 || bbox(1) <= 0 || bbox(2) <= 0 || bbox(1) >= width || (bbox(1)+bbox(3)) >= width || bbox(2) >= height || (bbox(2)+bbox(4)) >= height
        bbox = getrect(gcf);
    end
    
    xmin = bbox(1);
    ymin = bbox(2);
    xmax = bbox(1)+bbox(3);
    ymax = bbox(2)+bbox(4);
    
    annfid = fopen(fullfile('Annotations',sprintf('%s.txt',filestr)),'w');
    fprintf(annfid,'%s\n%s\n%d\n%d\n%d\n%.0f\n%.0f\n%.0f\n%.0f\n',...
        Object,str,width,height,depth,xmin,ymin,xmax,ymax);
    fclose(annfid);
end
disp('END')
