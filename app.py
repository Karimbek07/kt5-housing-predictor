
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Housing Price Predictor",
    page_icon="🏠",
    layout="wide"
)

MODEL_FILE = Path(__file__).parent / "KT5_models_and_preprocessing.joblib"

@st.cache_resource
def load_bundle():
    return joblib.load(MODEL_FILE)

if not MODEL_FILE.exists():
    st.error("Файл обученных моделей не найден.")
    st.stop()

try:
    bundle = load_bundle()
except Exception as error:
    st.error(f"Ошибка загрузки моделей: {error}")
    st.stop()

models = bundle["models"]
scaler = bundle["scaler"]
bounds = bundle["outlier_bounds"]
features = list(bundle["feature_names"])
metrics = bundle["metrics"]

def validate_data(data):
    missing = [c for c in features if c not in data.columns]
    if missing:
        raise ValueError("Отсутствуют признаки: " + ", ".join(missing))

    values = data[features].apply(pd.to_numeric, errors="coerce")

    if values.empty:
        raise ValueError("Нет строк для прогнозирования.")

    if not np.isfinite(values.to_numpy()).all():
        raise ValueError("Обнаружены пропуски или некорректные числа.")

    positive = ["MedInc", "HouseAge", "AveRooms",
                "AveBedrms", "Population", "AveOccup"]

    if (values[positive] <= 0).any().any():
        raise ValueError("Характеристики района должны быть положительными.")

    if not values["Latitude"].between(32.54, 41.95).all():
        raise ValueError("Широта вне диапазона California Housing.")

    if not values["Longitude"].between(-124.35, -114.31).all():
        raise ValueError("Долгота вне диапазона California Housing.")

    return values

def make_prediction(data, name):
    cleaned = data.copy()

    for column, limits in bounds.items():
        low, high = limits
        cleaned[column] = cleaned[column].clip(low, high)

    if name in ("Linear Regression", "Ridge Regression"):
        values = pd.DataFrame(
            scaler.transform(cleaned),
            columns=features,
            index=cleaned.index
        )
    else:
        values = cleaned

    return models[name].predict(values)

st.title("🏠 Прогнозирование стоимости недвижимости")
st.caption("КТ5 — Алгоритмы и модели машинного обучения | Университет «Туран»")

st.info(
    "Учебная модель California Housing: прогноз медианной стоимости "
    "жилья в районе на основе данных 1990 года. "
    "Не предназначена для определения текущей цены квартиры."
)

model_name = st.selectbox(
    "Выберите модель машинного обучения",
    list(models.keys()),
    index=list(models.keys()).index(bundle["best_model_name"])
)

tab1, tab2, tab3 = st.tabs([
    "Ручной прогноз", "Загрузка CSV", "Сравнение моделей"
])

with tab1:
    st.subheader("Введите характеристики района")

    defaults = {
        "MedInc": 3.5,
        "HouseAge": 29.0,
        "AveRooms": 5.2,
        "AveBedrms": 1.05,
        "Population": 1166.0,
        "AveOccup": 2.8,
        "Latitude": 34.26,
        "Longitude": -118.49
    }

    with st.form("prediction_form"):
        left, right = st.columns(2)
        values = {}

        for i, feature in enumerate(features):
            with (left if i % 2 == 0 else right):
                values[feature] = st.number_input(
                    feature,
                    value=float(defaults[feature]),
                    format="%.4f"
                )

        submitted = st.form_submit_button(
            "Рассчитать стоимость", type="primary"
        )

    if submitted:
        try:
            data = validate_data(pd.DataFrame([values]))
            prediction = float(make_prediction(data, model_name)[0])

            st.success("Прогноз успешно выполнен")
            st.metric(
                "Прогноз медианной стоимости жилья",
                f"${prediction * 100000:,.2f}"
            )
            st.caption("Историческая стоимость, не актуальная рыночная оценка.")
        except Exception as error:
            st.error(str(error))

with tab2:
    st.subheader("Пакетное прогнозирование")
    uploaded = st.file_uploader("Загрузите CSV-файл", type=["csv"])

    if uploaded is not None:
        try:
            original = pd.read_csv(uploaded)
            data = validate_data(original)
            prediction = make_prediction(data, model_name)

            result = original.copy()
            result["Prediction_MedHouseVal"] = prediction
            result["Prediction_USD"] = prediction * 100000

            st.success(f"Обработано строк: {len(result)}")
            st.dataframe(result, use_container_width=True)

            st.download_button(
                "Скачать результаты CSV",
                data=result.to_csv(index=False).encode("utf-8-sig"),
                file_name="housing_predictions.csv",
                mime="text/csv"
            )

            if "MedHouseVal" in original.columns:
                actual = pd.to_numeric(
                    original["MedHouseVal"], errors="coerce"
                )
                if np.isfinite(actual.to_numpy()).all():
                    st.subheader("Фактические и прогнозируемые значения")
                    chart = pd.DataFrame({
                        "Факт": actual.to_numpy(),
                        "Прогноз": prediction
                    })
                    st.scatter_chart(chart, x="Факт", y="Прогноз")

        except Exception as error:
            st.error(f"Ошибка обработки CSV: {error}")

with tab3:
    st.subheader("Метрики качества на тестовой выборке")
    st.dataframe(metrics, use_container_width=True, hide_index=True)

    left, right = st.columns(2)

    with left:
        st.subheader("Сравнение RMSE")
        st.bar_chart(metrics.set_index("Модель")[["RMSE"]])

    with right:
        st.subheader("Сравнение R²")
        st.bar_chart(metrics.set_index("Модель")[["R²"]])

    st.success(
        "Лучшая модель по результатам оптимизации КТ5: "
        + bundle["best_model_name"]
    )
