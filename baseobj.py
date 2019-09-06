"""
    define the base object

"""
import logging

class hobject(object):

    def __init__(self, logname = None):

        #-------------------Define logger------------------#
        self.mylogger = logging.getLogger('mylogger')
        self.mylogger.setLevel(logging.DEBUG)

        #Define logger format
        formatter = logging.Formatter(fmt='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')

        #Define logger file handler
        log_fname = logname if logname else './hobject.log'
        fh = logging.FileHandler(filename=log_fname, mode='a')
        fh.setFormatter(formatter)

        # logger1.addFilter(filter)
        self.mylogger.addHandler(fh)
        # ---------------End of Define logger--------------#

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



if __name__ == '__main__':
    hobj = hobject()
    hobj.log('This is a critical message!', 'critical')
    hobj.log('This is a debug message!', 'debug')
    hobj.log('This is a error message!', 'error')
