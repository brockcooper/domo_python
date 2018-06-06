# domo_python

This is a series of important Python functions that will allow you to easy work with the Domo API, including exporting and importing data.

## Examples of Functions Available

### Creating an Access Token

For each request you make to the Domo API, you will need to include an Access Token. For most tasks, you will only need to do this once for all of your calls to the Domo API but the Token can timeout so you will see that we will automatically be creating new Access Tokens for certain tasks like importing and exporting data to ensure a new Access Token has been created

```python
token = domo_python.get_access_token( client_id, client_secret )
print(token)
```
### Creating a New Dataset

In order to import data into Domo, you will need to create a Domo dataset first. You will need to follow Domo's schema rules, which are passed to Domo as a JSON object. The following shows an example of how to do this, but you can find more examples in the Domo API documentation as well.

[Creating Domo Dataset from Domo API Documentation](https://developer.domo.com/docs/dataset-api-reference/dataset#Create%20a%20DataSet)

```python
dataset_schema = """{
       "name" : "Domo API | Sample Domo Dataset Name",
       "description" : "This dataset came from the Domo API",
       "rows" : 0,
       "schema" : {
         "columns" : [ {
           "type" : "STRING",
           "name" : "group"
         },{
           "type" : "DATETIME",
           "name" : "ds"
         },{
           "type" : "LONG",
           "name" : "y"
         } ]
       }
     }"""

domo_python.create_new_domo_dataset ( token, dataset_schema)
```

### Exporting Data from Domo into a Pandas Dataframe

The following shows how to get your Domo dataset into a Pandas dataframe, which you can then use for any further analysis or ETL work.

```python
df = domo_python.domo_cav_to_dataframe ( historicalDatasetId, client_id, client_secret )
df.head()
```

### Importing Data from a Pandas Dataframe into Domo

The following shows how to import data from a dataframe into Domo. You will need to first create the dataset as shown above in the *Creating a New Dataset* section.

```python
domo_python.dataframe_to_domo_dataset ( df, timeseriesForecastDatasetID, client_id, client_secret  )
```

### Jupyter Notebooks Example

This repo also contains an example Jupyter Notebook with pre-written examples in the *domo-python-examples.ipynb* file. To access this, you will need to install Jupyter Notebooks, I recommend doing this through [Anaconda](https://www.anaconda.com/download/#macos).

After you've installed Jupyter Notebooks, you will navigate in your Terminal to the folder where you downloaded this repo and run the following command:

```
jupyter notebooks
```