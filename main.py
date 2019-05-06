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



from helpers import parse_arguments

from .helpers import load_detector
from .exceptions import UdataError

# Main function
def main():
    args = parse_arguments()

    try:
        detector = load_detector(args.detector, args.modules)
        #Generate a index name based on input
        index_name = args.input.split('/')[-1].split('.')[0].split('_')[0]
        if not index_name:
            index_name = 'Uuata'
    
    except UdataError as exc:
        print(repr(exc))
        sys.exit(exc.code)




if __name__ == '__main__':
    main()