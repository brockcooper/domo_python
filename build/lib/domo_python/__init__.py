import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
from datetime import date, timedelta
import json
import time
import pysftp
from io import StringIO

def get_access_token( client_id, client_secret ) :
    response = requests.get("https://api.domo.com/oauth/token?grant_type=client_credentials&scope=data", auth = HTTPBasicAuth(client_id, client_secret))
    return json.loads(response.content.decode("utf-8"))["access_token"]

def export_domo_dataset ( dataset_id, access_token, include_header='true'  ) :
    http_headers = {'content-type': 'application/json',
                        'Authorization' : 'bearer ' + access_token}
    return requests.get('https://api.domo.com/v1/datasets/' + dataset_id + '/data?includeHeader=' + include_header, headers = http_headers).text

def import_data_to_domo ( dataset_id, csv, access_token  ) :
    http_headers = {'content-type': 'text/csv',
                   'Authorization' : 'bearer ' + access_token}
    return requests.put('https://api.domo.com/v1/datasets/' + dataset_id + '/data?updateMethod=REPLACE', data = csv, headers = http_headers).text

def domo_csv_to_dataframe ( domo_dataset_id, domo_client_id, domo_client_secret ) :
    # Import CSV and turn into Pandas Dataframe
    return pd.read_csv(StringIO(export_domo_dataset(domo_dataset_id, get_access_token( domo_client_id, domo_client_secret ))))

def dataframe_to_domo_dataset ( dataframe, to_domo_dataset_id, domo_client_id, domo_client_secret ) :
    return import_data_to_domo ( to_domo_dataset_id, dataframe.to_csv(header=False,index=False), get_access_token( domo_client_id, domo_client_secret)  )

def create_new_domo_dataset ( access_token, dataset_schema, dataset='') :
    if dataset == "" :
        http_headers = {'Content-Type': 'application/json',
                       'Accept': 'application/json',
                       'Authorization' : 'bearer ' + access_token}
        response = requests.post('https://api.domo.com/v1/datasets', data = dataset_schema, headers = http_headers)
        j = json.loads(response.content.decode("utf-8"))
        print("Your new dataset id is: ", j["id"])
        return j["id"]

def domo_to_sftp(filename, host,username,password,port=22):

    df = domo_csv_to_dataframe ( dataset_id, client_id, client_secret )

    # Download to local file path
    df.to_csv('{filename}.csv'.format(filename=filename),header=True,index=False)

    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y.%m.%d')

    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    with pysftp.Connection(host=host, username=username, password=password, port=port, cnopts=cnopts) as sftp:
        with sftp.cd('incoming'):
            rename_file_name = 'archive/{filename}{datestamp}.csv'.format(filename=filename, datestamp=st)
            try:

                # Delete current archive file if it exists
                try:
                    sftp.remove(rename_file_name)
                    print('removed todays archive')
                except:
                    print('old file does not exist')

                # put last file upload into archive
                sftp.rename('{filename}.csv'.format(filename=filename), rename_file_name)
                print('renamed yesterday upload')
            except:
                print('no file to rename')
                pass
            finally:

                # upload file and remove the csv from local file path
                sftp.put('{filename}.csv'.format(filename=filename))
                os.remove('{filename}.csv'.format(filename=filename))
                print('Successful put')


    # Example of a Domo dataset schema needed for the API
    # dataset_schema = """{
    #   "name" : "Domo API | Sample Domo Dataset Name",
    #   "description" : "This dataset came from the Domo API",
    #   "rows" : 0,
    #   "schema" : {
    #     "columns" : [ {
    #       "type" : "STRING",
    #       "name" : "Row Number"
    #     },{
    #       "type" : "DATETIME",
    #       "name" : "ds"
    #     }, {
    #       "type" : "LONG",
    #       "name" : "yhat"
    #     }, {
    #       "type" : "LONG",
    #       "name" : "yhat_lower"
    #     }, {
    #       "type" : "LONG",
    #       "name" : "yhat_upper"
    #     }, {
    #       "type" : "STRING",
    #       "name" : "group"
    #     }, {
    #       "type" : "LONG",
    #       "name" : "y"
    #     } ]
    #   }
    # }"""
