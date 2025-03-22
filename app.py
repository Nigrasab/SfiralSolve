import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import io

# Заголовок Фонда
st.markdown("<h5 style='text-align: center;'>Некоммерческий Фонд исследования природы времени</h5>", unsafe_allow_html=True)

# Заголовок проекта
st.set_page_config(page_title="Сфиральная квантовая система", layout="centered")
st.title("Сфиральная квантовая система")

# Описание проекта
st.subheader("🌀 О проекте")
st.markdown(
    """
    Это приложение анализирует частотное распределение квантовых состояний, полученных из экспериментов. 
    Оно предназначено для визуализации, фильтрации и интерпретации вероятностной структуры данных, отражающих поведение систем во времени и их связь с моделями мышления, сознания и фрактальной динамики.

    Формат файла — `.json`, содержащий список состояний под ключом `statevector`. 
    **Максимальный размер файла: 5 МБ.**
    """
)

# Загрузка файла
st.markdown("### 📁 Загрузите JSON с данными измерений")
uploaded_file = st.file_uploader("Перетащите файл сюда", type="json")

if uploaded_file:
    try:
        df = pd.read_json(uploaded_file)

        if len(df) > 50000:
            st.warning("⚠️ Файл слишком большой. Разделите его на части для корректной обработки.")
        else:
            df_counts = df["statevector"].value_counts().reset_index()
            df_counts.columns = ["Состояние", "Частота"]

            # Фильтрация по шаблону
            pattern_input = st.text_input("🔍 Фильтр по битовому шаблону (используйте * для любых значений):", value="")
            if pattern_input:
                try:
                    regex = re.compile("^" + pattern_input.replace("*", ".") + "$")
                    df_counts = df_counts[df_counts["Состояние"].apply(lambda x: bool(regex.match(x)))]
                except re.error:
                    st.error("Неверный шаблон регулярного выражения.")

            # Сортировка и ограничение отображаемых состояний
            sort_order = st.radio("Сортировать по частоте:", ["По убыванию", "По возрастанию"], horizontal=True)
            ascending = sort_order == "По возрастанию"
            top_n = st.slider("Количество отображаемых состояний:", 1, 50, 10)
            df_top = df_counts.sort_values(by="Частота", ascending=ascending).head(top_n)

            # График
            fig, ax = plt.subplots(figsize=(10, 4))
            sns.barplot(x="Состояние", y="Частота", data=df_top, palette="Blues_r", ax=ax)
            ax.set_title(f"Частота появления топ-{top_n} состояний")
            ax.set_xlabel("Состояние")
            ax.set_ylabel("Частота")
            plt.xticks(rotation=45)
            st.pyplot(fig)

            # Таблица
            st.dataframe(df_top, use_container_width=True)

            # Кнопки скачивания
            csv_buffer = io.BytesIO()
            df_top.to_csv(csv_buffer, index=False)
            st.download_button(
                label="📥 Скачать CSV",
                data=csv_buffer.getvalue(),
                file_name="топ_состояний.csv",
                mime="text/csv"
            )

            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png')
            img_buffer.seek(0)
            st.download_button(
                label="🖼 Скачать график PNG",
                data=img_buffer,
                file_name="гистограмма_состояний.png",
                mime="image/png"
            )

            st.success("✅ Данные успешно загружены и обработаны!")

            # Комментарий к результатам
            st.markdown("""
            ---
            ### 🧠 Комментарий
            Отображённое распределение вероятностей демонстрирует, какие состояния квантовой системы устойчивы, а какие — редки. 
            Это помогает выявить **узлы устойчивости** — ключевые состояния, где система проводит больше всего времени. 
            Такие узлы могут быть аналогами **когнитивных фиксаций в мышлении** или **биологических паттернов устойчивости**, связанных с функционированием памяти и сознания. 

            Сфиральная модель позволяет **рассматривать квантовую систему как фрактальную динамическую структуру**, отражающую не просто данные, а **структуру времени** и **мыслящих процессов**, в которых прошлое и будущее переплетены в едином потоке.
            """)

    except Exception as e:
        st.error(f"Ошибка при обработке файла: {e}")
