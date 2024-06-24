import threading
import pandas as pd
from influxdb import InfluxDBClient
from datetime import datetime
import time


client = InfluxDBClient(host='10.244.0.244', port=8086, username='admin', password='1234', database='RIC_Test')
result = client.query('show measurements;')
#print("Result: {0}".format(result))

def insert_liveUE():
    while True:
        df = pd.read_csv('UEoutput_2.csv')
        df.fillna(0, inplace=True)
        batch_size = 5000
        num_batches = len(df) // batch_size + (1 if len(df) % batch_size > 0 else 0)
        for i in range(num_batches):
            start_idx = i * batch_size
            end_idx = start_idx + batch_size
            batch_df = df.iloc[start_idx:end_idx]
            json_body =[{
        "measurement": "liveUE",
        "tags": {"du-id": row['du-id']},
        "time": datetime.utcnow().isoformat(),
        #"time": current_time,
        "fields": {
            "nrCellIdentity": row['nrCellIdentity'],
            "RRU.PrbUsedDl": row['RRU.PrbUsedDl'],
            "DRB.UEThpDl": row['DRB.UEThpDl'],
            "x": row['x'],
            "y": row['y'],
            "RF.serving.RSRP": row['RF.serving.RSRP'],
            "RF.serving.RSRQ": row['RF.serving.RSRQ'],
            "RF.serving.RSSINR": row['RF.serving.RSSINR'],
            "nbCellIdentity_0": row['nbCellIdentity_0'],
            "nbCellIdentity_1": row['nbCellIdentity_1'],
            "nbCellIdentity_2": row['nbCellIdentity_2'],
            "nbCellIdentity_3": row['nbCellIdentity_3'],
            "nbCellIdentity_4": row['nbCellIdentity_4'],
            "rsrp_nb0": row['rsrp_nb0'],
            "rsrq_nb0": row['rsrq_nb0'],
            "rssinr_nb_0": row['rssinr_nb_0'],
            "rsrp_nb1": row['rsrp_nb1'],
            "rsrq_nb1": row['rsrq_nb1'],
            "rssinr_nb_1": row['rssinr_nb_1'],
            "rsrp_nb2": row['rsrp_nb2'],
            "rsrq_nb2": row['rsrq_nb2'],
            "rssinr_nb_2": row['rssinr_nb_2'],
            "rsrp_nb3": row['rsrp_nb3'],
            "rsrq_nb3": row['rsrq_nb3'],
            "rssinr_nb_3": row['rssinr_nb_3'],
            "rsrp_nb4": row['rsrp_nb4'],
            "rsrq_nb4": row['rsrq_nb4'],
            "rssinr_nb_4": row['rssinr_nb_4'],
            "targetTput": row['targetTput'],
            "ue-id":row['ue-id']
        }
    }
    for _, row in batch_df.iterrows()
    ]
        client.write_points(json_body)
        time.sleep(5)

    
    #res=client.write_points(json_body)
    #print(res)
    #print(client.write_points(json_body))

def insert_liveCell():
    while True:
        df = pd.read_csv('liveCell.csv')
        df.fillna(0, inplace=True) 
        json_body = []
        for _,row in df.iterrows():
            json_body.append(
            {
            "measurement": "liveCell",
            "tags": {"du-id": row['du-id']},
            "time": datetime.utcnow().isoformat(),
            "fields":{
            "nrCellIdentity": row['nrCellIdentity'],
            "throughput": row['throughput'],
            "x": row['x'],
            "y": row['y'],
            "availPrbDl": row['availPrbDl'],
            "availPrbUl": row['availPrbUl'],
            "measPeriodPrb": row['measPeriodPrb'],
            "pdcpBytesUl": row['pdcpBytesUl'],
            "pdcpBytesDl": row['pdcpBytesDl'],
            "measPeriodPdcpBytes": row['measPeriodPdcpBytes']
            }
            }
        )
        client.write_points(json_body)
        time.sleep(5)
    #res=client.write_points(json_body)
    #print(res)
    #print(client.write_points(json_body))

thread1=threading.Thread(target=insert_liveUE)
thread2=threading.Thread(target=insert_liveCell)


print("start")
thread1.start()
thread2.start()
thread1.join()
thread2.join()
