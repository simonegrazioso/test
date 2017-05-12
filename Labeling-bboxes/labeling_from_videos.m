Path = 'VIDEOS_DIR'; % Video dir
datadir = 'DATA_DIR'; % data dir
framesdir = 'FRAMES_DIR'; %frames dir
N = dir(Path);
N = N(3:end);
cont(1)=1;
cont(2)=1;
cont(3)=1;
% cont(4)=1;

for ii=1:length(N)
    Object = ii;
    
    N2 = dir([Path N(ii).name]);
    N2 = N2(3:end);
    for jj=1:length(N2)
        v = VideoReader([Path N(ii).name '/' N2(jj).name]);
        while hasFrame(v)
            bbox = zeros(1,4);
            frame = readFrame(v);
            imshow(frame);
            filestr = sprintf('%d_%05d',Object,cont(ii));
            frameName = [framesdir sprintf('%s.jpg',filestr)];
            saveas(gcf,frameName,'jpg');
	    while bbox(3)<=0 || bbox(4)<=0 || bbox(1) <= 0 || bbox(2) <= 0 || bbox(1) >= width || (bbox(1)+bbox(3)) >= width || bbox(2) >= height || (bbox(2)+bbox(4)) >= height
		bbox = getrect(gcf);
	    end
            
            xmin = bbox(1);
            ymin = bbox(2);
            xmax = bbox(1)+bbox(3);
            ymax = bbox(2)+bbox(4);
            annfid = fopen(fullfile(datadir,'Annotations',sprintf('%s.txt',filestr)),'w');
            fprintf(annfid,'%s\n%s\n%d\n%d\n%d\n%.0f\n%.0f\n%.0f\n%.0f\n',...
                    Object,filestr,size(frame,2),size(frame,1),size(frame,3),xmin,ymin,xmax,ymax)
            fclose(annfid);
            cont(ii) = cont(ii)+1;
        end
    end
end
