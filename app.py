import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import io

# ------------------------------
# ВЕРХНЯЯ ИНФОРМАЦИЯ О ПРОЕКТЕ
# ------------------------------
st.set_page_config(page_title="Сфиральная квантовая система", layout="centered")
st.title("Сфиральная квантовая система")

st.markdown(
    """
    🌀 **Проект "СфиральСоль"** — это инструмент анализа квантовых измерений, 
    отображающих структуру состояний, связанных с моделями времени, сознания и мышления. 
    Вы можете загрузить JSON-файл (до 5 МБ) с данными векторов состояний, и система визуализирует 
    наиболее часто встречающиеся конфигурации.
    """
)

# ------------------------------
# ЗАГРУЗКА ФАЙЛА
# ------------------------------
uploaded_file = st.file_uploader("\U0001F4C2 Загрузите JSON с данными измерений", type="json")

if uploaded_file:
    try:
        df = pd.read_json(uploaded_file)

        if df.memory_usage(deep=True).sum() > 5 * 1024 * 1024:
            st.warning("\U000026A0 Файл превышает лимит 5 МБ. Пожалуйста, уменьшите размер файла.")
        else:
            # Подсчёт частот
            df_counts = df["statevector"].value_counts().reset_index()
            df_counts.columns = ["Состояние", "Частота"]

            # Фильтрация по шаблону
            pattern_input = st.text_input("\U0001F50D Фильтр по битовому шаблону (используйте * для любых значений):", value="")
            if pattern_input:
                try:
                    regex = re.compile("^" + pattern_input.replace("*", ".") + "$")
                    df_counts = df_counts[df_counts["Состояние"].apply(lambda x: bool(regex.match(x)))]
                except re.error:
                    st.error("Неверный шаблон регулярного выражения")

            # Сортировка
            sort_order = st.radio("Сортировать по частоте:", ["По убыванию", "По возрастанию"], horizontal=True)
            ascending = sort_order == "По возрастанию"
            df_counts = df_counts.sort_values("Частота", ascending=ascending)

            # Слайдер для выбора количества отображаемых состояний
            max_n = min(50, len(df_counts))
            top_n = st.slider("Количество отображаемых состояний:", 1, max_n, value=min(10, max_n))
            df_top = df_counts.head(top_n)

            # Визуализация
            fig, ax = plt.subplots(figsize=(10, 4))
            sns.barplot(x="Состояние", y="Частота", data=df_top, palette="Blues_r", ax=ax)
            ax.set_title(f"Частота появления топ-{top_n} состояний")
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
                label="\U0001F4E5 Скачать CSV",
                data=csv_buffer.getvalue(),
                file_name="топ_состояний.csv",
                mime="text/csv"
            )

            # Скачивание PNG
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png')
            img_buffer.seek(0)
            st.download_button(
                label="\U0001F5BC Скачать график PNG",
                data=img_buffer,
                file_name="гистограмма_состояний.png",
                mime="image/png"
            )

            st.success("\U0001F4C1 Данные успешно загружены и обработаны!")

            # -----------------------------------
            # НИЖНИЙ СМЫСЛОВОЙ КОММЕНТАРИЙ
            # -----------------------------------
            st.markdown("""
            ---
            ### 🧠 Комментарий к результатам
            Полученные частотные распределения отражают устойчивые конфигурации квантовых состояний,
            которые могут быть связаны с фрактальной структурой времени или паттернами мышления. 
            Сфиральная модель позволяет интерпретировать эти состояния как ритмичные узлы сознания, 
            проявляющиеся в измерениях. Повторяемость определённых состояний может указывать 
            на глубинные закономерности восприятия или эволюции систем мышления.
            """)

    except Exception as e:
        st.error(f"Ошибка при обработке файла: {e}")
