import re
import pandas as pd
import numpy as np
from . import key

class FeatureUtility:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def consolidate(self):
        for i in [f for f in list(self.data.columns) if f != 'iso3']:
            _temp_float = 0
            _temp_integer = 0
            _temp_string = 0
            for j in range(len(self.data.index)):
                if re.search(r'[0-9]\.', self.data.loc[j, i]):
                    _temp_float += 1
                elif re.search(r'[0-9].+', self.data.loc[j, i]):
                    _temp_integer += 1
                elif (
                    re.search(r'[a-z].+[A-Z].+', self.data.loc[j, i]) or 
                    re.search(r'[A-Z].+', self.data.loc[j, i]) or 
                    re.search(r'[a-z].+', self.data.loc[j, i])
                    ):
                    _temp_string += 1
                else:
                    continue
            if _temp_float != 0 and _temp_float == len(self.data.index):
                self.data[i] = self.data[i].astype('float64')
            elif _temp_integer != 0 and _temp_integer == len(self.data.index):
                self.data[i] = self.data[i].astype('int64')
            elif _temp_string != 0 and _temp_string == len(self.data.index):
                self.data[i] = self.data[i].astype('str')
            else:
                pass
    
    @staticmethod
    def MakeIdentity():
        ref = key._feature_char_2015
        _nullable = ['..', ' ', '.', '...', 'NULL', 'null', 'NAN', 'NaN', 'Null']
        masterdict = dict()
        for feature in list(ref.keys()):
            _temp = dict()
            for _iso in key._iso_master:
                if _iso in list(ref[feature].keys()) and ref[feature][_iso] not in _nullable:
                    _temp[_iso] = ref[feature][_iso]
                elif _iso in list(ref[feature].keys()) and ref[feature][_iso] in _nullable:
                    _temp[_iso] = 'NaN'
                elif _iso not in list(ref[feature].keys()):
                    _temp[_iso] = 'NaN'
                else:
                    continue
            masterdict[feature] = _temp
        masterdata = pd.DataFrame(masterdict)
        return masterdata