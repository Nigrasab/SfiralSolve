import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import io

st.set_page_config(page_title="Сфиральная квантовая система", layout="centered")
st.title("Сфиральная квантовая система")

st.markdown("""
### 🌀 О проекте
Это приложение анализирует частотное распределение квантовых состояний, полученных из экспериментов.
Оно предназначено для визуализации, фильтрации и интерпретации вероятностной структуры данных, 
отражающих поведение систем во времени и их связь с моделями мышления, сознания и фрактальной динамики.
Формат файла — `.json`, содержащий список состояний под ключом `statevector`.
Максимальный размер файла: **5 МБ**.
""")

uploaded_file = st.file_uploader("📁 Загрузите JSON с данными измерений", type="json")

if uploaded_file:
    file_size = uploaded_file.size
    if file_size > 5 * 1024 * 1024:
        st.error("❌ Файл превышает ограничение в 5 МБ. Пожалуйста, разделите его на части для корректной обработки.")
    else:
        try:
            df = pd.read_json(uploaded_file)

            if len(df) > 50000:
                st.warning("⚠️ Файл слишком большой. Разделите его на части для корректной обработки.")
            else:
                df_counts = df["statevector"].value_counts().reset_index()
                df_counts.columns = ["Состояние", "Частота"]

                # Ввод шаблона фильтрации
                pattern_input = st.text_input("🔍 Фильтр по битовому шаблону (используйте * для любых значений):", value="")
                if pattern_input:
                    try:
                        regex = re.compile("^" + pattern_input.replace("*", ".") + "$")
                        df_counts = df_counts[df_counts["Состояние"].apply(lambda x: bool(regex.match(x)))]
                    except re.error:
                        st.error("Неверный шаблон регулярного выражения.")

                # Сортировка и выбор количества
                sort_order = st.radio("Сортировать по частоте:", ["По убыванию", "По возрастанию"], horizontal=True)
                ascending = sort_order == "По возрастанию"

                max_display = min(50, len(df_counts))
                top_n = st.slider("Количество отображаемых состояний:", 1, max_display, value=min(10, max_display))

                df_top = df_counts.sort_values("Частота", ascending=ascending).head(top_n)

                fig, ax = plt.subplots(figsize=(10, 4))
                sns.barplot(x="Состояние", y="Частота", data=df_top, palette="Blues_r", ax=ax)
                ax.set_title(f"Частота появления топ-{top_n} состояний")
                ax.set_xlabel("Состояние")
                ax.set_ylabel("Частота")
                plt.xticks(rotation=45)
                st.pyplot(fig)

                st.dataframe(df_top, use_container_width=True)

                # Скачивание CSV
                csv_buffer = io.BytesIO()
                df_top.to_csv(csv_buffer, index=False)
                st.download_button(
                    label="📥 Скачать CSV",
                    data=csv_buffer.getvalue(),
                    file_name="топ_состояний.csv",
                    mime="text/csv"
                )

                # Скачивание PNG
                img_buffer = io.BytesIO()
                plt.savefig(img_buffer, format='png')
                img_buffer.seek(0)
                st.download_button(
                    label="🖼️ Скачать график PNG",
                    data=img_buffer,
                    file_name="гистограмма_состояний.png",
                    mime="image/png"
                )

                # Комментарий к результатам
                st.markdown("""
---
### 💡 Комментарий к результатам
Анализ частотных распределений позволяет выявить устойчивые состояния в квантовой системе. 
Эти состояния, как пики на графике, могут интерпретироваться как устойчивые точки во временном 
континууме модели, потенциально соответствующие фрагментам квантовой памяти или циклам сознания.
Таким образом, частотные структуры — это не просто статистика, а форма временной логики, 
в которой мысли, волны и состояния связываются в узлы смысла.
""")

                st.success("✅ Данные успешно загружены и обработаны!")

        except Exception as e:
            st.error(f"Ошибка при обработке файла: {e}")
