import pandas as pd
import re
from _iso import _iso_master
from _iso import _name_to_iso_master

class BaseUtility:
    def __init__(self, first_path: str , second_path: str, delimiter = None, decimal = None):
        if delimiter is None and decimal is None:
            self.data0 = pd.read_csv(first_path)
            self.data1 = pd.read_csv(second_path)
            self.masterdata = None
        else:
            self.data0 = pd.read_csv(first_path, delimiter = delimiter[0], decimal = decimal[0])
            self.data1 = pd.read_csv(second_path, delimiter = delimiter[1], decimal = decimal[1])
            self.masterdata = None
    
    def sanitize(self,  which: str, before: tuple, after: tuple):
        which = which.lower()
        if which == 'first':
            _temp = dict()
            for i in range(len(before)):
                _temp[before[i]] = after[i]
            self.data0 = self.data0.rename(
                columns = _temp)
        elif which == 'second':
            _temp = dict()
            for i in range(len(before)):
                _temp[before[i]] = after[i]
            self.data1 = self.data1.rename(
                columns = _temp)
        else:
            raise ValueError("The instances parameter of 'which' should either 'first' or 'second', that is not case sensitive.")

    def arrange(self):
        _templ_0 = [self.data0['iso3'].name]
        _templ_1 = [self.data0['iso3'].name]
        for label in list(self.data0.columns):
            if label != 'iso3':
                _templ_0.append(label)
            else:
                continue   
        for label in list(self.data1.columns):
            if label != 'iso3':
                _templ_1.append(label)
            else:
                continue
        self.data0 = self.data0[_templ_0]
        self.data1 = self.data1[_templ_1]

    def popout(self, which: str,  drop: list):
        which = which.lower()
        if which == 'first':
            if len(drop) == 1:
                self.data0 = self.data0.drop(
                    columns = drop[0])
            elif len(drop) > 1:
                self.data0 = self.data0.drop(
                    columns = drop)
            else:
                return
        elif which == 'second':
            if len(drop) == 1:
                self.data1 = self.data1.drop(
                    columns = drop[0])
            elif len(drop) > 1:
                self.data1 = self.data1.drop(
                    columns = drop)
        else:
            raise ValueError("The instances parameter of 'which' should either 'first' or 'second', that is not case sensitive.")

    def orchestrate(self, commit = None, special = None, which_special = None):
        self.dict0 = dict()
        self.dict1 = dict()
        self.masterdict = dict()
        if special is None and which_special is None:
            _data0 = self.data0.drop(columns = 'iso3').copy()
            _data1 = self.data1.drop(columns = 'iso3').copy()
        else:
            if isinstance(special, str) and isinstance(which_special, str):
                which_special = which_special.lower()
                special = special.lower()
                if special == 'imf' and which_special == 'first':
                    for i in range(len(self.data0.index)):
                        _element = self.data0['iso3'][i]
                        _temp_iso = re.search(r'([A-Z]{3})', _element)
                        self.data0.at[i, 'iso3'] = _temp_iso.group(1)
                elif special == 'imf' and which_special == 'second':
                    for i in range(len(self.data1.index)):
                        _element = self.data0['iso3'][i]
                        _temp_iso = re.search(r'([A-Z]{3})', _element)
                        self.data1.at[i, 'iso3'] = _temp_iso.group(1)
                elif special == 'oecd' and which_special == 'first':
                    for i in range(len(self.data0['iso3'].index)):
                        if self.data0['iso3'][i] in list(_name_to_iso_master.keys()):
                            self.data0.at[i, 'iso3'] = _name_to_iso_master[self.data0['iso3'][i]]
                        else:
                            continue
                elif special == 'oecd' and which_special == 'second':
                    for i in range(len(self.data1.index)):
                        if self.data1['iso3'][i] in list(_name_to_iso_master.keys()):
                            self.data1.at[i, 'iso3'] = _name_to_iso_master[self.data1['iso3'][i]]
                        else:
                            continue
                elif special == 'scimago' and which_special == 'first':
                    for i in range(len(self.data0.index)):
                        if self.data0['iso3'][i] in list(_name_to_iso_master.keys()):
                            self.data0.at[i, 'iso3'] = _name_to_iso_master[self.data0['iso3'][i]]
                        else:
                            continue
                elif special == 'scimago' and which_special == 'second':
                    for i in range(len(self.data1.index)):
                        if self.data1['iso3'][i] in list(_name_to_iso_master.keys()):
                            self.data1.at[i, 'iso3'] = _name_to_iso_master[self.data1['iso3'][i]]
                        else:
                            continue
                else:
                    pass
            elif isinstance(special, tuple) and isinstance(which_special, tuple):
                _options = {
                    'first': (special[0), which_special[0]), 
                    'second': (special[1], which_special[1])
                }
                for k in list(_options.keys()):
                    special = _options[k][0].lower()
                    which_special = _options[k][1].lower()
                    if special == 'imf' and which_special == 'first':
                        for i in range(len(self.data0.index)):
                            _element = self.data0['iso3'][i]
                            _temp_iso = re.search(r'([A-Z]{3})', _element)
                            self.data0.at[i, 'iso3'] = _temp_iso.group(1)
                    elif special == 'imf' and which_special == 'second':
                        for i in range(len(self.data1.index)):
                            _element = self.data0['iso3'][i]
                            _temp_iso = re.search(r'([A-Z]{3})', _element)
                            self.data1.at[i, 'iso3'] = _temp_iso.group(1)
                    elif special == 'oecd' and which_special == 'first':
                        for i in range(len(self.data0['iso3'].index)):
                            if self.data0['iso3'][i] in list(_name_to_iso_master.keys()):
                                self.data0.at[i, 'iso3'] = _name_to_iso_master[self.data0['iso3'][i]]
                            else:
                                continue
                    elif special == 'oecd' and which_special == 'second':
                        for i in range(len(self.data1.index)):
                            if self.data1['iso3'][i] in list(_name_to_iso_master.keys()):
                                self.data1.at[i, 'iso3'] = _name_to_iso_master[self.data1['iso3'][i]]
                            else:
                                continue
                    elif special == 'scimago' and which_special == 'first':
                        for i in range(len(self.data0.index)):
                            if self.data0['iso3'][i] in list(_name_to_iso_master.keys()):
                                self.data0.at[i, 'iso3'] = _name_to_iso_master[self.data0['iso3'][i]]
                            else:
                                continue
                    elif special == 'scimago' and which_special == 'second':
                        for i in range(len(self.data1.index)):
                            if self.data1['iso3'][i] in list(_name_to_iso_master.keys()):
                                self.data1.at[i, 'iso3'] = _name_to_iso_master[self.data1['iso3'][i]]
                            else:
                                continue
                    else:
                        pass
            else:
                pass
                
            _data0 = self.data0.drop(columns = 'iso3').copy()
            _data1 = self.data1.drop(columns = 'iso3').copy()
        
        _nullable_list = [' ', '..', '...', 'NaN', 'NULL', 'Null', '_']
        
        for _feature_key in list(_data0.columns):
            _temp = dict()
            for i in range(len(self.data0.index)):
                _temp[self.data0['iso3'][i]] = str(self.data0[_feature_key][i])
            self.dict0[_feature_key] = _temp
        for _feature_label in list(_data1.columns):
            _temp = dict()
            for i in range(len(self.data1.index)):
                _temp[self.data1['iso3'][i]] = str(self.data1[_feature_label][i])
            self.dict1[_feature_label] = _temp
        for _feature_key in list(self.dict0.keys()):
            _temp = dict()
            for __iso in _iso_master:
                if __iso in self.dict0[_feature_key] and self.dict0[_feature_key][__iso] not in _nullable_list:
                    _temp[__iso] = self.dict0[_feature_key][__iso]
                elif __iso in self.dict0[_feature_key] and self.dict0[_feature_key][__iso] in _nullable_list:
                    _temp[__iso] = 'NaN'
                elif __iso not in self.dict0[_feature_key]:
                    _temp[__iso] = 'NaN'
                else:
                    continue
            self.masterdict[_feature_key] = _temp
        for _feature_key in list(self.dict1.keys()):
            _temp = dict()
            for __iso in _iso_master:
                if __iso in self.dict1[_feature_key] and self.dict1[_feature_key][__iso] not in _nullable_list:
                    _temp[__iso] = self.dict1[_feature_key][__iso]
                elif __iso in self.dict1[_feature_key] and self.dict1[_feature_key][__iso] in _nullable_list:
                    _temp[__iso] = 'NaN'
                elif __iso not in self.dict1[_feature_key]:
                    _temp[__iso] = 'NaN'
                else:
                    continue
            self.masterdict[_feature_key] = _temp
        self.masterdata = pd.DataFrame(self.masterdict)
        if commit is not None:
            commit = commit.lower()
            self.masterdata = self.masterdata.reindex()
            self.masterdata = self.masterdata.rename(
                columns = {
                    'index': 'iso3'
                }
            )
        else: pass



    

