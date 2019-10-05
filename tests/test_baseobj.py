
import os
import pytest

from baseobj import hobject
from utils import find, search


class TestClass_hobject:

    msgs = [
        ('This is a critical message!', 'critical'),
        ('This is a debug message!', 'debug'),
        ('This is a error message!', 'error'),
        ('This is a fuck message!', 'error')

    ]

    def obj_init(self):
        os.remove(os.path.join(os.getcwd(), 'test_hobject.log'))
        hobj = hobject(logname='test_hobject.log')
        for item in self.msgs:
            hobj.log(item[0], item[1])

    def test_logfile(self):
        self.obj_init()
        assert os.path.join(os.getcwd(),'test_hobject.log') in find(os.getcwd(), 'test', 'log')
        assert os.path.join(os.getcwd(),'test_hobject.log') == search(os.getcwd(), 'test_hobject.log')

    def test_content(self):
        with open(os.path.join(os.getcwd(), 'test_hobject.log')) as FR:
            line_cnt = 0
            for line in FR:
                line_cnt += 1
                assert self.msgs[line_cnt-1][0] in line


if __name__ == "__main__":
    pytest.main(['-q', '--html=test_hobject_report.html','test_baseobj.py'])