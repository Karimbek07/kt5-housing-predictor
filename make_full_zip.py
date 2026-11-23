"""Собрать готовый офлайн ZIP после добавления своего файла модели."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

root=Path(__file__).resolve().parent
model=root/'KT5_models_and_preprocessing.joblib'
if not model.is_file():
    raise SystemExit('Сначала скопируйте KT5_models_and_preprocessing.joblib рядом с app.py.')
result=root/'KT5_Housing_FULL.zip'
include=['app.py','KT5_California_Housing.ipynb','requirements.txt','README.md','DEPLOY.md','check_project.py','install_windows.bat','run_windows.bat','make_full_zip.py','make_full_zip.bat',model.name]
include += [str(x.relative_to(root)) for x in sorted((root/'examples').rglob('*.csv'))]
with ZipFile(result,'w',ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
    for item in include:
        p=root/item
        if p.exists(): z.write(p, arcname='KT5_Housing/'+item)
with ZipFile(result) as z:
    bad=z.testzip()
    if bad: raise RuntimeError('Повреждён: '+bad)
print('Готов полный архив:',result, '| размер:',round(result.stat().st_size/1024/1024,1),'МБ')
