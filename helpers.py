""" Helper functions """
import argparse

from exceptions import ModuleLoadError, DetectorNotFoundError


""" Parse commandline arguments """
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--detector", help="anomaly detector or ML model to use", default="Gaussian1D or Gaussian mixture models")
    parser.add_argument("--modules", help="Python modules that define additional anomaly " "detectors",
                        nargs='+', default=[])

    parser.add_argument("--es", help="Stream to Elasticsearch", action="store_true")
    parser.add_argument("--es-uri", help="Output Elasticsearch URI", 
                        default="http://localhost:9200/")
    parser.add_argument("--kibana-uri", help="Kibana URI", 
                        default="http://localhost:5601/app/kibana")
    parser.add_argument("--bokeh-port", help="Bokeh server port", default="5001")
    parser.add_argument("--es-index", help="Elasticsearch index name")
    parser.add_argument("--entry-type", help="Entry type name", default="measurement")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    parser.add_argument("-s", '--sensors', help="Select specific sensor names",
                        nargs='+')
    parser.add_argument("-t", "--timefield",
                        help="name of the column in the data that defines the time",
                        default="")
    parser.add_argument("--speed", help="Restreamer speed",
                        default="1.0")
    parser.add_argument("--cols", help="Dashboard columns",
                        default="3")
    parser.add_argument('input', help='input file or stream')
    return parser.parse_args()




def load_detector(name, modules):
    """ Evaluate modules as Python code and load selecter anomaly detector """
    # Try to load modules
    for module in modules:
        if module.endswith('.py'):
            code = open(module).read()
        else:
            code = 'import %s' % module
        try:
            exec(code)
        except Exception as exc:
            raise ModuleLoadError('Failed to load module %s. Exception: %r', (module, exc))

    # Load selected anomaly detector
    for detector in AnomalyMixin.__subclasses__():
        if detector.__name__.lower() == name.lower():
            return detector

    raise DetectorNotFoundError("Can't find detector: %s" % name)


def init_detector_models(sensors, training_set, detector):
    """ Initialize anomaly detector models """
    models = {}
    for sensor in sensors:
        models[sensor] = detector()
        models[sensor].fit(training_set[sensor])
    return models
