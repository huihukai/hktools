"""
Commonly used operations and methods
"""

import os, re, copy, xlsxwriter
import pandas as pd
import numpy as np
import json

__all__ = ['find', 'search', 'list2str',
           'file2df', 'df2file', 'dict2df', 'df2dict', 'df2json', 'json2df', 'dict2df_flat', 'df2dict_flat' ]


def find(path, start_str, end_str):
    """
    find files in given folder with given start and end
    :param path: ``str``, folder to find
    :param start_str: ``str``, start string to find
    :param end_str: ``str``, end string to find
    :return: ``list``, full path file list of found results
    """
    file_list = []
    pat = re.compile(r'^' + start_str + r'.*?' + end_str +r'$')
    for file_name in os.listdir(path):
        if os.path.isfile(os.path.join(path, file_name)) and pat.search(file_name):
            file_list.append(os.path.join(path, file_name))
    return file_list


def search(path, fname):
    """
    find the file name in the path and its subpath

    :param path: ``str``, start path
    :param name: ``str``, target file name
    :return: ``str``, full path of the file
    """
    return_fname = ''
    for root, dirs, files in os.walk(path, topdown=True):
        for name in files:
            if name == fname:
                return os.path.join(root,name)
        for dir_name in dirs:
            return_fname = search(dir_name, fname)
    return return_fname


def list2str(in_list, delimeter = '', container = ''):
    """
    convert a list object into a string,
    each in_list element is separated by delimeter and contained by container

    :param in_list:  ``list``, input list
    :param delimeter:  ``str``, delimeter
    :param container:  ``str``, container
    :return:  ``str``, converted string

    example:
    in_list = ['a', 2, 43, 'sdf']
    delimeter = ';'
    container = '"'

    then, return:
    '"a";"2";"43";"sdf"'

    """
    out_str = ''
    for item in in_list:
        out_str += container + str(item) + container + delimeter
    return out_str[:-1]


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

    header: ['alph', 'num', 'value']

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


def df2dict(df_in):
    """
    Convert DataFrame into multi-dimentional dict

    :param df_in: ``DataFrame`` Input DataFrame
    :return: (dict, header)

    example:df:
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

    header: ['alph', 'num', 'value']

    """
    dict_out = dict()
    header_out = list()
    header = list(df_in.columns)
    if len(header) == 1:
        assert len(df_in[header[0]]) == 1, "More then 1 value in last recurrence!"
        return (list(df_in[header[0]])[0], header)
    else:
        for item in set(df_in[header[0]]):
            (dict_out[item], header_out) = df2dict(df_in[df_in[header[0]] == item][header[1:]])
        header_out = [header[0]] + header_out
        return (dict_out, header_out)


def df2json(df, fname, outpath = None):
    """
    Convert DataFrame object into json file

    :param df: ``DataFrame``, input DataFrame type data
    :param fname: ``str``, outfile name
    :param outpath: ``str``, output path
    :return: None
    """
    pat_json = re.compile(r'(.*?)\.json?')
    outname = fname + '.json' if not pat_json.search(fname) else fname
    outname = os.path.join(outpath, outname) if outpath else fname
    with open(outname, 'w') as FW:
        json.dump(df2dict_flat(df), fp=FW, indent=4)


def json2df(fname):
    """
    Convert table json file into DataFrame object, the input file must be json format

    :param fname: ``str``, input table like file full path
    :return: None
    """
    assert str(fname).split('.')[-1] in ('json'), 'file must be json format!'
    # Load data table
    with open(fname, 'r') as load_f:
        load_dict = json.load(load_f)
    return dict2df_flat(load_dict)


def dict2df_flat(dict_in):
    """
    Conver flat type of dict into DataFrame

    Example:
    flat dict:
    {
        0: {
            'a':1,
            'b':2,
            'c':3
            }
        1: {
            'a':3,
            'b':4,
            'c':5
            }
        2: {
            'a':5,
            'b':6,
            'c':7
            }
    }

    df:
        'a' 'b' 'c'
    0   1   2   3
    1   3   4   5
    2   5   6   7


    :param dict_in:
    :return:
    """
    col_name = list(dict_in[list(dict_in.keys())[0]].keys())
    df_out = pd.DataFrame(columns= col_name)
    for row_index in dict_in.keys():
        df_out = df_out.append(dict_in[row_index], ignore_index= True)
    return df_out.infer_objects()


def df2dict_flat(df):
    """
    Conver DataFrame data type into flat dict
    flat dict: 1st level keys are df index, 2nd level keys are columns

    example:
    df:
        'a' 'b' 'c'
    0   1   2   3
    1   3   4   5
    2   5   6   7

    flat dict:
    {
        0: {
            'a':1,
            'b':2,
            'c':3
            }
        1: {
            'a':3,
            'b':4,
            'c':5
            }
        2: {
            'a':5,
            'b':6,
            'c':7
            }
    }

    :param df: `DataFrame``, input DataFrame type data
    :return: flat_dict
    """
    df = df.infer_objects()
    for col in df.columns:
        if df[col].dtype in [np.int64, np.int32, np.float]:
            df[col] = df[col].apply(float)  # convert int64, int32 type into float
        else:
            df[col] = df[col].apply(str)  # convert int64, int32 type into float

    dict_df_out = dict()
    for item in df.index:
        dict_df_out[item] = dict(df.loc[item])
    return dict_df_out
