import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import io

st.set_page_config(page_title="Сфиральная квантовая система", layout="centered")

st.markdown("""
### Некоммерческий Фонд исследования природы времени

# Сфиральная квантовая система

#### 🌀 О проекте
Это приложение анализирует частотное распределение квантовых состояний, полученных из экспериментов. Оно предназначено для визуализации, фильтрации и интерпретации вероятностной структуры данных, отражающих поведение систем во времени и их связь с моделями мышления, сознания и фрактальной динамики. 

**Формат файла** — `.json`, содержащий список состояний под ключом `statevector`. **Максимальный размер файла: 5 МБ.**
""")

uploaded_file = st.file_uploader("📂 Загрузите JSON с данными измерений", type="json")

if uploaded_file:
    try:
        df = pd.read_json(uploaded_file)

        if len(df) > 50000:
            st.warning("⚠️Файл слишком большой. Разделите его на части для корректной обработки.")
        else:
            df_counts = df["statevector"].value_counts().reset_index()
            df_counts.columns = ["Состояние", "Частота"]

            # 🔎 Ввод шаблона фильтрации
            pattern_input = st.text_input("🔍 Фильтр по битовому шаблону (используйте * для любых значений):", value="")
            if pattern_input:
                try:
                    regex = re.compile("^" + pattern_input.replace("*", ".") + "$")
                    df_counts = df_counts[df_counts["Состояние"].apply(lambda x: bool(regex.match(x)))]
                except re.error:
                    st.error("Неверный шаблон регулярного выражения.")

            # 📊 Сортировка и отображение
            sort_order = st.radio("Сортировать по частоте:", ["По убыванию", "По возрастанию"], horizontal=True)
            ascending = sort_order == "По возрастанию"
            df_counts = df_counts.sort_values("Частота", ascending=ascending)

            top_n = st.slider("Количество отображаемых состояний:", min_value=1, max_value=50, value=10)
            df_top = df_counts.head(top_n)

            # 📈 Гистограмма
            fig, ax = plt.subplots(figsize=(10, 4))
            sns.barplot(x="Состояние", y="Частота", data=df_top, palette="Blues_r", ax=ax)
            plt.xticks(rotation=45)
            st.pyplot(fig)

            # 📋 Таблица
            st.dataframe(df_top, use_container_width=True)

            # 📥 Скачивание CSV
            csv_buffer = io.BytesIO()
            df_top.to_csv(csv_buffer, index=False)
            st.download_button(
                label="📥 Скачать CSV",
                data=csv_buffer.getvalue(),
                file_name="топ_состояний.csv",
                mime="text/csv"
            )

            # 🖼️ Скачивание PNG
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png')
            img_buffer.seek(0)
            st.download_button(
                label="🖼️ Скачать график PNG",
                data=img_buffer,
                file_name="гистограмма_состояний.png",
                mime="image/png"
            )

            st.success("✅Данные успешно загружены и обработаны!")

            # 💠 Сфиральное состояние (интерпретация)
            st.subheader("💠 Сфиральное состояние")
            if not df_top.empty:
                stable_states = df_top[df_top['Частота'] == df_top['Частота'].max()]['Состояние'].tolist()
                st.markdown("""
                **Обнаружены узлы максимальной устойчивости:**
                
                Эти состояния представляют наибольшую повторяемость в квантовой интерференции и могут рассматриваться как фрактальные якоря Сфиральной структуры. Их стабильность свидетельствует о ритмической упорядоченности.
                
                Такие узлы интерпретируются как **точки притяжения** в пространстве состояний — подобно тому, как в биологии устойчивые формы возникают из множества возможных конфигураций.
                
                Это также может быть связано с временными структурами — где повторяющиеся узлы формируют пульс времени и отражают закономерности мышления или сознания.
                """)
                for s in stable_states:
                    st.code(s, language="")

    except Exception as e:
        st.error(f"Ошибка при обработке файла: {e}")
