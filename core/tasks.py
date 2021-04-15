
import requests
from datetime import date, timedelta
import zipfile
import json
import redis
import pandas as pd


from django.utils import timezone

from celery.decorators import task




@task
def process_csv(tried_once = False):
    '''
        Runs every weekday at 8 PM 
        Makes a get request to BSE to fetch CSV File, then stores the data from CSV into Redis DB
    '''
    print('Started Processing CSV')
    r = redis.Redis(host='localhost', port=6379, db=2)

    todays_date = date.today()
    day = todays_date.strftime('%d')
    month = todays_date.strftime('%m')
    year = todays_date.strftime('%y')
    full_year = todays_date.strftime('%Y')


   
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    url = f'https://www.bseindia.com/download/BhavCopy/Equity/EQ{day}{month}{year}_CSV.ZIP'

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(response.status_code)
        if not tried_once:
            process_csv.apply_async((True,), eta=timezone.now() + timedelta(minutes=5))
        return
    
    print("Downloaded CSV")

    file_name = f'./EQ{day}{month}{year}_CSV.ZIP'

    with open(file_name, 'wb') as f:
        f.write(response.content)


    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall()

    csv_file_name = f'./EQ{day}{month}{year}.CSV'

    data = pd.read_csv(f'./EQ{day}{month}{year}.CSV')

    with r.pipeline() as pipe:
        for index, row in data.iterrows():
            dict_row = { 'CODE': row['SC_CODE'], 'NAME': row['SC_NAME'].strip(),'OPEN': row['OPEN'], 'HIGH': row['HIGH'], 'LOW': row['LOW'], 'CLOSE' : row['CLOSE']}
            company_name = row['SC_NAME'].strip()
            pipe.set(f'{full_year}-{month}-{day} {company_name}',json.dumps(dict_row) )
        pipe.execute()

    print('completed')
    return

