test=imread('iob.png');
SE=strel('rectangle',[3 3]);
BW1=imdilate(test,SE);
BW2=imerode(BW1,SE);
