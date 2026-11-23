"""Локальная проверка архива КТ5 с ДОВЕРЕННЫМ joblib-файлом."""
from pathlib import Path
import joblib
import pandas as pd
import numpy as np

base=Path(__file__).resolve().parent
p=base/'KT5_models_and_preprocessing.joblib'
if not p.is_file():
    raise SystemExit('Отсутствует KT5_models_and_preprocessing.joblib. Скопируйте свой файл в папку проекта.')

# Запускать только для файла, который вы создали сами в Google Colab.
b=joblib.load(p)
required={'models','scaler','outlier_bounds','feature_names','metrics','best_model_name'}
assert required.issubset(b), f'Нет ключей: {required-set(b)}'
expected=['Linear Regression','Ridge Regression','Random Forest Regressor','Random Forest Optimized']
assert set(expected).issubset(b['models']), b['models'].keys()
features=b['feature_names']
assert len(features)==8, features
x=pd.DataFrame([{'MedInc':3.5,'HouseAge':29,'AveRooms':5.2,'AveBedrms':1.05,'Population':1166,'AveOccup':2.8,'Latitude':34.26,'Longitude':-118.49}],columns=features)
for feature,(low,high) in b['outlier_bounds'].items():
    x[feature]=x[feature].clip(low,high)
for name in expected:
    values=pd.DataFrame(b['scaler'].transform(x),columns=features) if name in ('Linear Regression','Ridge Regression') else x
    predicted=float(b['models'][name].predict(values)[0])*100000
    assert np.isfinite(predicted)
    print(f'{name}: ${predicted:,.2f}')
print('Проверка прошла; модель по умолчанию:',b['best_model_name'])
