# Data 
Vehicle data set downloaded from kaggle 9-10-2022. 
* Source: https://www.kaggle.com/datasets/nehalbirla/vehicle-dataset-from-cardekho?resource=download

# Creating requirements.txt file
```conda list -e > requirements.txt``` in PyCharm terminal

or if there is an error you can export as 

```conda env export > <environment-name>.yml```

In order to read the requirements
```conda env create -f <environment-name>.yml```