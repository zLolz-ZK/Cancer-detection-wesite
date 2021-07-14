# Cancer-detection-wesite
Final Year project implementation using django The model is not kept here as the size is too big and I'll add a link to it later in google drive.

The models are made using Transfer Learning using InceptionResNetv2 as a feature Extactor. 

There are 2 models both of which must be downloaded for this to work.(Total size of models is around 500-600MB). 

One for detection other for Visualization(Feature extractor of detector stored seperately because of some issues I faced while accessing the final Conv2D layer, so i kept it seperate).

The visualiztion algo used in the gradcam algo from the official keras docs, all credits to them and respective authors.
