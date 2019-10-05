"""
    define the base object

"""
import logging

class hobject(object):

    def __init__(self, logname = None):

        self.mylogger = self.logger_init(logname=logname)

    def logger_init(self, logname=None):

        # -------------------Define logger------------------#
        mylogger = logging.getLogger('mylogger')
        mylogger.setLevel(logging.DEBUG)

        # Define logger format
        formatter = logging.Formatter(fmt='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')

        # Define logger file handler
        log_fname = logname if logname else './hobject.log'
        fh = logging.FileHandler(filename=log_fname, mode='a')
        fh.setFormatter(formatter)

        # logger1.addFilter(filter)
        mylogger.addHandler(fh)
        # ---------------End of Define logger--------------#

        return mylogger


    def log(self, msg, level):
        dict_level = {
            'CRITICAL'  : self.mylogger.critical,
            'ERROR'     : self.mylogger.error,
            'WARNING'   : self.mylogger.warning,
            'INFO'      : self.mylogger.info,
            'DEBUG'     : self.mylogger.debug,
        }
        assert str(level).upper() in dict_level.keys(), 'Not supported msg level type: %s' % level
        dict_level[str(level).upper()](msg)

