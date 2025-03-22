import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import io

# Заголовок Фонда
st.markdown("<h4 style='text-align: center;'>Некоммерческий Фонд исследования природы времени</h4>", unsafe_allow_html=True)

# Название проекта
st.title("Сфиральная квантовая система")

# Описание проекта
st.markdown("""
### 🌀 О проекте
Это приложение анализирует частотное распределение квантовых состояний, полученных из экспериментов. Оно предназначено для визуализации, фильтрации и интерпретации вероятностной структуры данных, отражающих поведение систем во времени и их связь с моделями мышления, сознания и фрактальной динамики.

Сфиральная квантовая система — это не просто анализ квантовых состояний. Это модель, основанная на **принципе Сфиральной интерференции**, где ключевыми являются **узлы устойчивости**, смена полярности и фрактальные переходы. Такие узлы могут соответствовать стабильным состояниям сознания или биологическим ритмам. Мы исследуем, как эти состояния чередуются и каким образом они влияют на протекание процессов во времени и пространстве.

Формат файла — `.json`, содержащий список состояний под ключом `statevector`. **Максимальный размер файла: 5 МБ.**
""")

# Загрузка файла
st.markdown("""
📁 **Загрузите JSON с данными измерений**
""")

uploaded_file = st.file_uploader("Перетащите файл сюда", type="json")

if uploaded_file:
    try:
        df = pd.read_json(uploaded_file)

        if len(df) > 50000:
            st.warning("⚠️ Файл слишком большой. Разделите его на части для корректной обработки.")
        else:
            df_counts = df["statevector"].value_counts().reset_index()
            df_counts.columns = ["Состояние", "Частота"]

            # Ввод шаблона фильтрации
            pattern_input = st.text_input("🔎 Фильтр по битовому шаблону (используйте * для любых значений):", value="")
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

            # Слайдер для отображения N состояний
            top_n = st.slider("Количество отображаемых состояний:", min_value=1, max_value=50, value=10)
            df_top = df_counts.head(top_n)

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

            # Комментарий результатов
            st.markdown("""
            ---
            ### 🧠 Интерпретация результатов
            Полученное распределение показывает, какие квантовые состояния наиболее устойчивы при моделировании. Пики на графике — это **узлы устойчивости**, отражающие закономерности, устойчивые ко времени. Такие узлы могут соответствовать точкам **перехода фрактального порядка**, **устойчивым ритмам мышления** или **биологическим маркерам**.

            Эти результаты — шаг к пониманию того, как квантовая система может имитировать процессы **времени, памяти и сознания** в сложных фрактальных структурах.
            """)

            st.success("✅ Данные успешно загружены и обработаны!")

    except Exception as e:
        st.error(f"Ошибка при обработке файла: {e}")
