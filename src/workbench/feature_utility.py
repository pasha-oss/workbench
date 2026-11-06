import re
import pandas as pd
import numpy as np
from . import key
from scipy import stats

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
    def rationing(self, name: str,  numerator: str, denumerator: str):
        self.data[name] = self.data[numerator]*((self.data[denumerator])**-1)

    def transform(self, which: str|list[str], transform: str):
        if isinstance(which, str):
            if transform == 'Log Natural':
                self.data['ln_' + f'{which}'] = np.log1p(self.data[which])
            elif transform == 'Box-Cox':
                _min = 0
                for i in range(len(self.data.index)):
                    if self.data[which][i] < 0:
                        _min += 1
                    else:
                        continue
                if _min > 0:
                    raise ValueError("Box-Cox assumes all instances has positive values, instead use 'Yeo-Johnson'")
                else:
                    _transformed = stats.boxcox(self.data[which])
                    _temp = self.data[[f for f in list(self.data.columns)]]
                    _bc = pd.DataFrame(_transformed[0].reshape(-1, 1), columns = ['bc_'+f'{which}'])
                    self.data = pd.concat([_temp, _bc], axis = 1)
            elif transform == 'Yeo-Johnson':
                _transformed = stats.yeojohnson(self.data[which])
                _temp = self.data[[f for f in list(self.data.columns)]]
                _bc = pd.DataFrame(_transformed[0].reshape(-1, 1), columns = ['yj_'+ f'{which}'])
                self.data = pd.concat([_temp, _bc], axis = 1)
            else:
                pass
        if isinstance(which, list):
            for feature in which:
                if transform == 'Log Natural':
                    self.data['ln_' + f'{feature}'] = np.log1p(self.data[feature])
                elif transform == 'Box-Cox':
                    _min = 0
                    for i in range(len(self.data[feature].index)):
                        if self.data[feature][i] < 0:
                            _min += 1
                        else:
                            continue
                    if _min > 0:
                        raise ValueError("Box-Cox assumes all instances has positive values, instead use 'Yeo-Johnson'")
                    else:
                        _transformed = stats.boxcox(self.data[feature])
                        _bc = pd.DataFrame(_transformed[0].reshape(-1, 1), columns = ['bc_' + f'{feature}'])
                        _temp = self.data[[f for f in list(self.data.columns)]]
                        self.data = pd.concat([_temp, _bc], axis = 1)
                elif transform == 'Yeo-Johnson':
                    _transformed = stats.yeojohnson(self.data[feature])
                    _bc = pd.DataFrame(_transformed[0].reshape(-1, 1), columns = ['yj_' + f'{feature}'])
                    _temp = self.data[[f for f in list(self.data.columns)]]
                    self.data = pd.concat([_temp, _bc], axis = 1)
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
