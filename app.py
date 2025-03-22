# app.py — обновлённая версия с логотипом, переключением тем и ограничением на 5 МБ
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import re

# === Настройки страницы ===
st.set_page_config(
    page_title="Сфиральная квантовая система",
    layout="centered",
    page_icon="🌀"
)

# === Переключатель темы (светлая/тёмная) ===
theme = st.toggle("\U0001F319 Тёмная тема")
if theme:
    st.markdown("""
        <style>
        body { background-color: #0e1117; color: #fafafa; }
        </style>
    """, unsafe_allow_html=True)

# === Логотип по центру ===
st.markdown("""
    <div style='text-align: center;'>
        <img src='https://raw.githubusercontent.com/Nigrasab/SfiralSolve/main/logo.png' width='60'>
    </div>
""", unsafe_allow_html=True)

# === Описание проекта ===
st.title("Сфиральная квантовая система")
st.subheader("🌀 О проекте")
st.markdown("""
    Это приложение анализирует частотное распределение квантовых состояний, полученных из экспериментов.
    Оно предназначено для визуализации, фильтрации и интерпретации вероятностной структуры данных,
    отражающих поведение систем во времени и их связь с моделями мышления, сознания и фрактальной динамики. 
    Формат файла — `.json`, содержащий список состояний под ключом `statevector`.
    **Максимальный размер файла: 5 МБ.**
""")

# === Загрузка файла ===
st.markdown("\n**📁 Загрузите JSON с данными измерений**")
uploaded_file = st.file_uploader("Перетащите файл сюда", type="json")

# === Обработка данных ===
if uploaded_file:
    if uploaded_file.size > 5 * 1024 * 1024:
        st.error("Файл слишком большой. Максимальный размер: 5 МБ.")
    else:
        try:
            df = pd.read_json(uploaded_file)
            if len(df) > 50000:
                st.warning("Файл слишком большой. Разделите его на части для корректной обработки.")
            else:
                df_counts = df["statevector"].value_counts().reset_index()
                df_counts.columns = ["Состояние", "Частота"]

                # === Фильтрация по шаблону ===
                pattern_input = st.text_input("🔍 Фильтр по битовому шаблону (* для любых значений):", value="")
                if pattern_input:
                    try:
                        regex = re.compile("^" + pattern_input.replace("*", ".") + "$")
                        df_counts = df_counts[df_counts["Состояние"].apply(lambda x: bool(regex.match(x)))]
                    except:
                        st.error("Неверный шаблон регулярного выражения.")

                # === Сортировка ===
                sort_order = st.radio("Сортировать по частоте:", ["По убыванию", "По возрастанию"], horizontal=True)
                ascending = sort_order == "По возрастанию"
                df_counts = df_counts.sort_values("Частота", ascending=ascending)

                # === Слайдер топ-N ===
                top_n = st.slider("Количество отображаемых состояний:", 1, min(50, len(df_counts)), 10)
                df_top = df_counts.head(top_n)

                # === График ===
                fig, ax = plt.subplots(figsize=(10, 4))
                sns.barplot(x="Состояние", y="Частота", data=df_top, palette="Blues_r", ax=ax)
                ax.set_title(f"Частота появления топ-{top_n} состояний")
                ax.set_xlabel("Состояние")
                ax.set_ylabel("Частота")
                plt.xticks(rotation=45)
                st.pyplot(fig)

                # === Таблица ===
                st.dataframe(df_top, use_container_width=True)

                # === Кнопки скачивания ===
                csv_buffer = io.BytesIO()
                df_top.to_csv(csv_buffer, index=False)
                st.download_button("⬇️ Скачать CSV", csv_buffer.getvalue(), "топ_состояний.csv", mime="text/csv")

                img_buffer = io.BytesIO()
                plt.savefig(img_buffer, format="png")
                img_buffer.seek(0)
                st.download_button("🖼️ Скачать график PNG", img_buffer, "гистограмма_состояний.png", mime="image/png")

                # === Комментарий результатов ===
                st.success("✅ Данные успешно загружены и обработаны!")
                st.markdown("""
                    🧠 **Комментарий:**
                    Полученные распределения отражают вероятностную структуру измеряемых квантовых состояний.
                    Повторяющиеся паттерны могут указывать на устойчивые состояния, фрактальную периодику или 
                    поведение, связанное с динамикой сознания. Анализ временных рядов состояния позволяет выявлять
                    закономерности, лежащие в основе мышления или биологических циклов.
                """)

        except Exception as e:
            st.error(f"Ошибка при обработке файла: {e}")
