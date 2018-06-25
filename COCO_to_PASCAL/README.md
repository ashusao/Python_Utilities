This script extract the images of mentioned categories from COCO detection dataset copies it into `../JPEGImages/`. 
It also converts the **corresponding annotation into PASCAL VOC format** and save it into `../annotations_pascalformat/`.
Also it generates the **train/val.txt** required containing the image Ids of image in training and validation set which is saved in `../ImageSets/Main/`

To modify the category list
	- Update the line 30 `catNms=['scissors','suitcase','toilet','laptop','umbrella']`.
