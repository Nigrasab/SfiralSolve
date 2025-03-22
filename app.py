import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import io

# Настройка страницы
st.set_page_config(page_title="Сфиральная квантовая система", layout="centered")
st.title("Сфиральная квантовая система")

# Загрузка JSON-файла
uploaded_file = st.file_uploader("\U0001F4C2 Загрузите JSON с данными измерений", type="json")

if uploaded_file:
    try:
        df = pd.read_json(uploaded_file)

        if len(df) > 50000:
            st.warning("Файл слишком большой. Разделите его на части для корректной обработки.")
        else:
            df_counts = df["statevector"].value_counts().reset_index()
            df_counts.columns = ["Состояние", "Частота"]

            # Фильтр по шаблону
            pattern_input = st.text_input("\U0001F50D Фильтр по битовому шаблону (используйте * для любых значений):", value="")
            if pattern_input:
                try:
                    regex = re.compile("^" + pattern_input.replace("*", ".") + "$")
                    df_counts = df_counts[df_counts["Состояние"].apply(lambda x: bool(regex.match(x)))]
                except re.error:
                    st.error("Неверный шаблон регулярного выражения.")

            # Сортировка
            sort_order = st.radio("Сортировать по частоте:", ["По убыванию", "По возрастанию"], horizontal=True)
            ascending = sort_order == "По возрастанию"
            df_counts = df_counts.sort_values(by="Частота", ascending=ascending)

            # Количество отображаемых состояний
            top_n = st.slider("Количество отображаемых состояний:", min_value=1, max_value=50, value=10)
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
                label="⬇️ Скачать CSV",
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

            st.success("\u0414анные успешно загружены и обработаны!")

    except Exception as e:
        st.error(f"Ошибка при обработке файла: {e}")
