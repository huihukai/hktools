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
    assert str(fname).split('.')[-1] in ('txt', 'csv', 'xls', 'xlsx'), 'file must be txt/csv/excel format!'
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


def dict2df(dict_in, header):
    """
    Convert multi-dimensional dict to pandas DataFrame

    :param dict_in: ``dict``, input dict
    :param header: ``list``, list of headers, usually of description of every dict's dimension
    :return: ``DataFrame``, converted DataFrame

    example:
    multi-dimensional dict (2 dimensional):
    {
        'a': {
            1: 'abc',
            2: 'def',
            3: 'ghi',
        },
        'b': {
            1: 'cba',
            2: 'fed',
            3: 'ihg',
        },
        'c' {
            1: 'bca',
            2: 'efd',
            3: 'hig',
        },
    }

    head: ['alph', 'num', 'value']

    df:
        alph    num     value
    1   a       1       abc
    2   a       2       def
    3   a       3       ghi
    4   b       1       cba
    5   b       2       fed
    6   b       3       ihg
    7   c       1       bca
    8   c       2       efd
    9   c       3       hig

    """
    df_out = pd.DataFrame(columns= header)
    df_line_dict = dict()
    for item in dict_in.keys():
        if isinstance(dict_in[item], dict):
            df_temp = dict2df(dict_in= dict_in[item], header= header[1:])
            line_list =  [item for row in df_temp.index]
            df_temp.insert(loc= 0, column= header[0], value = line_list)
            df_out = pd.concat([df_out, df_temp], axis=0, ignore_index=True)
        else:
            df_line_dict[header[0]] = item
            df_line_dict[header[1]] = dict_in[item]
            df_out = df_out.append(df_line_dict, ignore_index=True)
    return df_out