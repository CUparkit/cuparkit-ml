# cuparkit-ml
Machine learning tools and backend services for CUparkit

## Setup
* Create a virtual environment
```
virtualenv env/ -p python3
source env/bin/activate
```
* Install dependancies
```
pip install -r requirements.txt
```
* Prepreocess data
```
python preprocess/build_parking_dataset.py
```
* Train the model locally
```
python model/train.py
```
* Generate and deploy predictions
```
python model/predictor.py
```

## Dataset sources
In order to form a starting point for the model we used a dataset of parking lot availablity from Santa Monica, CA. We did this since no other data about Clemson parking lots was publically available. We then matched up parking lots in this dataset to parking lots in Clemson that fit in size and usage. Our model then uses this our dataset as a proxy for parking availaibity in Clemson.

## Online training
The frontend webapp incorporates functionality in order to crowd-source data from users about the current availability of parking lots on campus. As we collect more of this data we have built an online training routine that will take this crowd-sourced data and retrain the model to improve its accurary. 