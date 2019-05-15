"""
1. Udata - Understanding your data (This is a generic data cleansing solution with bonus unsupervised learning added to it.)
( we will keep adding anomaly detector, and new unsupervised models into it. You can add your own models/code.These should inherit 
anomaly detector abstract base class ) 
2. Read an input datastream that consists of sensor data or text file
3. Cleanse the incoming data
4. Applies scores to the incoming data using selected ML models
5. Restreams input data and scores to ElasticSearch and/or Bokeh server 
"""
import sys
import datetime
import time
import threading
import math
import webbrowser

from queue import Queue

import pandas as pd
import numpy as np

from restream.elasticsearch import init_elasticsearch



from helpers import parse_arguments

from helpers import load_detector, init_detector_models
from exceptions import UdataError


MAX_BATCH_SIZE = 1000

# sys.path.append("/home/cssdesk/Desktop/Udata/")

def restream_dataframe(
        dataframe, detector, sensors=None, timefield=None,
        speed=10, es_uri=None, kibana_uri=None, index_name='',
        entry_type='', bokeh_port=5001, cols=3):
    """
        Restream from an input pandas dataframe to an existing Elasticsearch instance and/or to a
        built-in Bokeh server.
        Generates respective Kibana & Bokeh dashboard apps to visualize the
        stream in the browser
    """
    if es_uri:
        es_conn = init_elasticsearch(es_uri)
        # Generate dashboard with selected fields and scores
        print("generate a kibana dashboard!")
    else:
        es_conn = None

    # Queue to communicate between restreamer and dashboard threads
    update_queue = Queue()
    print("generate a bokeh dashboard!")

    restream_thread = threading.Thread(
        target=threaded_restream_dataframe,
        args=(dataframe, sensors, detector, timefield, es_conn,
              index_name, entry_type, bokeh_port, update_queue)
    )
    restream_thread.start()

def threaded_restream_dataframe(dataframe, sensors, detector, timefield,
                                es_conn, index_name, entry_type, bokeh_port,
                                update_queue, interval=3, sleep_interval=1):
    """ Restream dataframe to bokeh and/or Elasticsearch """
    # Split data into batches
    batches = np.array_split(dataframe, math.ceil(dataframe.shape[0]/MAX_BATCH_SIZE))

    # Initialize anomaly detector models, train using first batch
    models = init_detector_models(sensors, batches[0], detector)

    

# Main function
def main():
    args = parse_arguments()

    try:
        detector = load_detector(args.detector, args.modules)
        #Generate a index name based on input
        index_name = args.input.split('/')[-1].split('.')[0].split('_')[0]
        if not index_name:
            index_name = 'Udata'

        print('loading data...')
        """
        This will be the core of Udata
        Detect inputdata, 
        if type csv:  load into pandas dataframe
        if type text: find out how to load the file (To be decided)
        """
        dataframe = pd.read_csv(args.input, sep=',')
        print('Loaded into dataframe.\n')
        
        restream_dataframe(dataframe, detector=detector, 
            speed=int(float(args.speed)),
            es_uri=args.es and args.es_uri, kibana_uri=args.kibana_uri, 
            index_name=index_name, entry_type=args.entry_type, bokeh_port=int(args.bokeh_port),
            cols=int(args.cols)
        )


    except UdataError as exc:
        print(repr(exc))
        sys.exit(exc.code)




if __name__ == '__main__':
    main()
    