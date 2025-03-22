import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import io

# Настройки страницы (первая команда обязательно!)
st.set_page_config(page_title="Сфиральная квантовая система", layout="centered")

# Название организации
st.markdown("<div style='text-align:center; font-size:18px;'>Некоммерческий Фонд исследования природы времени</div>", unsafe_allow_html=True)

# Основной заголовок
st.title("Сфиральная квантовая система")

# Описание проекта
with st.expander("ℹ️ О проекте"):
    st.markdown("""
        Это приложение анализирует частотное распределение квантовых состояний, полученных из экспериментов. 
        Оно предназначено для визуализации, фильтрации и интерпретации вероятностной структуры данных, отражающих поведение систем во времени.

        **Почему это важно:**
        - Вероятностные состояния — это сигнатуры квантовых процессов.
        - Анализ частот даёт понимание устойчивых форм (узлов), которые могут моделировать мышление, сознание или биологические паттерны.
        - Сфиральная структура описывает переходные состояния между уровнями, как это бывает в памяти, сне, интуиции.

        **Формат данных:** `.json`, поле `statevector`. 
        **Максимальный размер файла:** 5 МБ.
    """)

# Загрузка файла
st.markdown("### 📁 Загрузите JSON с данными измерений")
uploaded_file = st.file_uploader("Перетащите файл сюда", type="json", help="Ограничение 5 МБ на файл • JSON")

if uploaded_file:
    try:
        df = pd.read_json(uploaded_file)

        if len(df) > 50000:
            st.warning("Файл слишком большой. Разделите его на части для корректной обработки.")
        else:
            df_counts = df["statevector"].value_counts().reset_index()
            df_counts.columns = ["Состояние", "Частота"]

            # Фильтр по шаблону
            pattern_input = st.text_input("🔍 Фильтр по битовому шаблону (используйте * для любых значений):", value="")
            if pattern_input:
                try:
                    regex = re.compile("^" + pattern_input.replace("*", ".") + "$")
                    df_counts = df_counts[df_counts["Состояние"].apply(lambda x: bool(regex.match(x)))]
                except re.error:
                    st.error("Неверный шаблон регулярного выражения.")

            # Сортировка
            sort_order = st.radio("Сортировать по частоте:", ["По убыванию", "По возрастанию"], horizontal=True)
            ascending = sort_order == "По возрастанию"
            df_counts = df_counts.sort_values("Частота", ascending=ascending)

            # Слайдер количества
            top_n = st.slider("Количество отображаемых состояний:", min_value=1, max_value=50, value=min(10, len(df_counts)))
            df_top = df_counts.head(top_n)

            # График
            fig, ax = plt.subplots(figsize=(10, 4))
            sns.barplot(x="Состояние", y="Частота", data=df_top, palette="Blues_r", ax=ax)
            ax.set_title("Частота появления топ-{} состояний".format(top_n))
            ax.set_xlabel("Состояние")
            ax.set_ylabel("Частота")
            plt.xticks(rotation=45)
            st.pyplot(fig)

            # Таблица
            st.dataframe(df_top, use_container_width=True)

            # Скачивание CSV
            csv_buffer = io.BytesIO()
            df_top.to_csv(csv_buffer, index=False)
            st.download_button(
                label="💾 Скачать CSV",
                data=csv_buffer.getvalue(),
                file_name="топ_состояний.csv",
                mime="text/csv"
            )

            # Скачивание PNG
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png')
            img_buffer.seek(0)
            st.download_button(
                label="🖼 Скачать график PNG",
                data=img_buffer,
                file_name="гистограмма_состояний.png",
                mime="image/png"
            )

            # Комментарий результата
            st.markdown("""
                ---
                #### 🧠 Смысловой комментарий
                Результаты показывают наиболее устойчивые вероятностные состояния. Эти состояния можно интерпретировать как **узлы Сфиральной структуры**, отражающие стабильные конфигурации во временных квантовых процессах. 

                Такие узлы могут быть аналогами **переходных фаз в мышлении**, **устойчивых образов сознания** или даже **биологических паттернов** (например, в нервных системах).

                Анализ их структуры помогает лучше понять природу **интерференции, фрактальности и времени**. 
            """)

            st.success("\u0414анные успешно загружены и обработаны!")

    except Exception as e:
        st.error(f"Ошибка при обработке файла: {e}")
