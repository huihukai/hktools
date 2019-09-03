"""
Commonly used operations and methods
"""

import os, re, copy, xlsxwriter
import pandas as pd

def file2df(fname):
    """
    load a table like file to a DataFrame object, the input file must be txt/csv/xls/xlsx format

    :param fname: ``str``, input table like file full path
    :return: ``DataFrame``, DataFrame object load from input
    """
    assert str(fname).split('.')[-1] in ('txt', 'csv', 'xls', 'xlsx'), 'file must be txt or csv or excel format!'
    # Load data table
    if str(fname).split('.')[-1] == 'txt':
        data = pd.read_table(fname, header=0, index_col=False, encoding='utf-8')
    elif str(fname).split('.')[-1] == 'csv':
        data = pd.read_csv(fname, header=0, index_col=False, encoding='utf-8')
    else:
        data = pd.read_excel(fname, header=0, index_col=False, engine= xlsxwriter)
    return data


def df2file(df, fname, outpath = None):
    """
    Convert DataFrame object into table like file

    :param df: ``DataFrame``, input DataFrame type data
    :param fname: ``str``, outfile name, if suffix is not detected, .xlsx file will dafult
    :param outpath: ``str``, output path
    :return: None
    """
    outpath = os.getcwd() if not outpath else outpath
    assert isinstance(df, pd.DataFrame), 'Input is not a pandas DataFrame type!'
    suffix = 'xlsx' if len(str(fname).split('.')) == 1 else str(fname).split('.')[-1]
    assert suffix in ('txt','csv', 'xls', 'xlsx'), 'Error file type: must be excel/csv/txt'
    outname = fname + '.' + suffix if len(str(fname).split('.')) == 1 else fname
    if suffix == 'xlsx':
        df.to_excel(os.path.join(outpath, outname), sheet_name=outname, index=False, engine= 'xlsxwriter')
    elif suffix == 'csv':
        df.to_csv(os.path.join(outpath, outname), index=False)
    elif suffix == 'txt':
        df.to_csv(os.path.join(outpath, outname), index=False, sep= '\t')
    else:
        return False
    return True


def find(path, start_str, end_str):
    """
    find files in given folder with given start and end
    :param path: ``str``, folder to find
    :param start_str: ``str``, start string to find
    :param end_str: ``str``, end string to find
    :return: ``list``, full path file list of rearching results
    """
    file_list = []
    pat = re.compile(r'^' + start_str + r'.*?' + end_str +r'$')
    for file_name in os.listdir(path):
        if os.path.isfile(os.path.join(path, file_name)) and pat.search(file_name):
            file_list.append(os.path.join(path, file_name))
    return file_list