# fruit-builder-and-detector
2 applications, one for building fruit dataset, one for detecting fruit image
# installation
create your new pycharm project.

download all files from this repository and move to your project's folder.

terminate to the project's folder and run 'pip install -r setup.txt'
# fruit dataset builder - IT worker edition
Run 'datasetBuilder.py' file

step 1. choose an image from path.

step 2. use your mouse to crop a bounding box that bounds only one fruit per box.

step 3. make sure the cropped image is in a good quality then classify the correct class for the fruit.

step 4. save the cropped image, you can see it in the 'train' folder.
# fruit detector 
step 1. run 'main.py' file.

step 2. choose an image from path.

step 3. if you click:

"Manual": you can manually crop a bounding box that bound the fruit you want to clasify, and see the result.

"Automatic": the waterShed will automatically predict all possible bounding boxs then classify the fruit appears on each box.

"Preprocessed": to classify a preprocessed-and-segmented image (a 100x100 image which contain only one fruit that maximum horizontally or vertically streched, with a white background).

for more informations, contact me fb.com/nhatrongbp dotrungtuann@gmail.com
