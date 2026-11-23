# Публикация КТ5 в GitHub и Streamlit Community Cloud

Сначала проверьте локальную работу через `run_windows.bat`. В полной версии архива `KT5_models_and_preprocessing.joblib` уже включён. Проверьте его наличие рядом с `app.py` перед публикацией.

## 1. Подготовка GitHub

1. Создайте пустой репозиторий в https://github.com/new (например, `kt5-housing-predictor`). Учитывайте, что **публичный репозиторий делает код и модель доступными всем**.
2. На компьютере установите **Git for Windows** (https://git-scm.com/downloads/win) и **Git LFS** (https://git-lfs.com/), если они ещё не установлены.
3. **Самый простой вариант:** запустите `upload_to_github.bat` в папке проекта, введите адрес созданного репозитория (например `https://github.com/USERNAME/kt5-housing-predictor.git`) и подтвердите публикацию.
4. **Ручной вариант:** в CMD откройте папку проекта, в которой лежит модель, и выполните команды ниже. Замените `<ВАШ_ЛОГИН>` на логин GitHub.

```cmd
git init
git lfs install
git lfs track "KT5_models_and_preprocessing.joblib"
git add .
git commit -m "KT5: Housing Price Predictor"
git branch -M main
git remote add origin https://github.com/<ВАШ_ЛОГИН>/kt5-housing-predictor.git
git push -u origin main
```

GitHub может попросить подтвердить вход. **Не вводите GitHub пароль в чат**. Если репозиторий уже создан / git init сделан, выполняйте только недостающие команды.

Почему Git LFS? Файлы больше 25 MiB нельзя добавить через веб-форму GitHub; свыше 50 MiB обычный git выдаёт предупреждение. Для очень больших файлов нужен LFS. Streamlit Community Cloud поддерживает LFS при развертывании из GitHub.

После `git push` проверьте в GitHub, что файл `.gitattributes` присутствует, а большой файл модели указан как Git LFS. Не загружайте большой файл через браузер GitHub.

## 2. Публикация Streamlit

1. Откройте https://share.streamlit.io/ и войдите через GitHub.
2. Нажмите **Create app** → **Yup, I have an app**.
3. Выберите репозиторий `<ВАШ_ЛОГИН>/kt5-housing-predictor`, ветку `main`, путь к файлу `app.py`.
4. В дополнительных настройках выберите **Python 3.12**, если такой выбор доступен (под него подготовлены зависимости).
5. Нажмите **Deploy**. Полученный адрес будет вида `https://<НАЗВАНИЕ>.streamlit.app/`. Это и есть ссылка для преподавателя.
6. Проверьте все 4 модели, ручной расчёт, загрузку `examples/sample_data.csv`, скачивание прогнозов и проверку `examples/invalid_data.csv`.

## 3. Если приложение не запускается

- Ошибка «Файл обученных моделей не найден»: файл `.joblib` не попал в репозиторий, не подтянулся через Git LFS или лежит не рядом с `app.py`.
- Ошибка при `joblib.load`: несовместимая версия scikit-learn или повреждённый файл. Попробуйте закрепить версию scikit-learn, под которой файл работал на Windows.
- Ошибка нехватки памяти: большие ансамбли Random Forest могут превышать ресурсы бесплатного хостинга. Для публикации может потребоваться облегчённый набор моделей или другой тариф/хостинг; это отдельное изменение и должно быть проверено.
- Если репозиторий закрытый, подключите доступ к приватным репозиториям в настройках Streamlit.

Официальная документация:
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/file-organization
- https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository

## Конфиденциальность и факт публикации
Публичный GitHub-репозиторий делает содержимое файлов доступным всем, включая файл модели. Не добавляйте пароли, токены и личные данные. Публичная ссылка Streamlit считается созданной только после успешного Deploy в вашем аккаунте.
