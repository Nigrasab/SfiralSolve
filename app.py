import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import re

st.set_page_config(page_title="Сфиральная квантовая система", layout="centered")

# Заголовок и описание
st.markdown("""
# Сфиральная квантовая система
### Некоммерческий Фонд исследования природы времени

#### О проекте
Это приложение анализирует частотное распределение квантовых состояний, полученных из экспериментов. Оно предназначено для визуализации, фильтрации и интерпретации вероятностной структуры данных, отражающих поведение систем во времени и их связь с моделями мышления, сознания и фрактальной динамики. Формат файла — `.json`, содержащий список состояний под ключом `statevector`. **Максимальный размер файла: 5 МБ**.

#### Смысл и особенности модели
Это не просто визуализатор квантовой схемы. Это **модель Сфиральной интерференции**, отражающая:  
- вероятностные закономерности как аналог мышления,  
- устойчивые узлы как точки самосогласования (аналог памяти),  
- распределения как след фрактальной динамики во времени.  

**Узлы** — это состояния, которые чаще повторяются. Они соответствуют устойчивым паттернам в структуре данных и могут быть аналогией устойчивых состояний в сознании, биоритмах или динамике времени.
""")

uploaded_file = st.file_uploader("Перетащите файл сюда", type="json")

if uploaded_file:
    if uploaded_file.size > 5 * 1024 * 1024:
        st.error("❌ Файл превышает ограничение в 5 МБ.")
    else:
        try:
            df = pd.read_json(uploaded_file)
            if len(df) > 50000:
                st.warning("⚠️ Файл довольно большой, возможно потребуется разделить его.")
            else:
                df_counts = df["statevector"].value_counts().reset_index()
                df_counts.columns = ["Состояние", "Частота"]

                pattern_input = st.text_input("🔍 Фильтр по битовому шаблону (* для любых значений):", value="")
                if pattern_input:
                    try:
                        regex = re.compile("^" + pattern_input.replace("*", ".") + "$")
                        df_counts = df_counts[df_counts["Состояние"].apply(lambda x: bool(regex.match(x)))]
                    except re.error:
                        st.error("Неверный шаблон регулярного выражения.")

                sort_order = st.radio("Сортировать по частоте:", ["По убыванию", "По возрастанию"], horizontal=True)
                ascending = (sort_order == "По возрастанию")
                df_counts = df_counts.sort_values("Частота", ascending=ascending)

                max_display = min(50, len(df_counts))
                top_n = st.slider("Количество отображаемых состояний:", 1, max_display, 10)
                df_top = df_counts.head(top_n)

                fig, ax = plt.subplots(figsize=(10, 4))
                sns.barplot(x="Состояние", y="Частота", data=df_top, palette="Blues_r", ax=ax)
                ax.set_title(f"Частота появления топ-{top_n} состояний")
                ax.set_xlabel("Состояние")
                ax.set_ylabel("Частота")
                plt.xticks(rotation=45)
                st.pyplot(fig)

                st.dataframe(df_top, use_container_width=True)

                csv_buffer = io.BytesIO()
                df_top.to_csv(csv_buffer, index=False)
                st.download_button(
                    label="⬇️ Скачать CSV",
                    data=csv_buffer.getvalue(),
                    file_name="топ_состояний.csv",
                    mime="text/csv"
                )

                img_buffer = io.BytesIO()
                plt.savefig(img_buffer, format="png")
                img_buffer.seek(0)
                st.download_button(
                    label="🖼️ Скачать график PNG",
                    data=img_buffer,
                    file_name="гистограмма_состояний.png",
                    mime="image/png"
                )

                st.success("✅ Данные успешно загружены и обработаны!")

                st.markdown("""
### 💡 Комментарий к результатам
Выявленные узлы — это устойчивые состояния системы, часто проявляющиеся в квантовых измерениях. Они могут интерпретироваться как аналоги нейронных пиков активности, устойчивых ритмов или состояний равновесия.

Сама модель отражает **фрактально-интерференционную природу времени**, где Сфираль описывает не траекторию, а **структуру вероятностных переходов**. Это приближает нас к пониманию не только вычислений, но и самого **процесса мышления** как квантово-фазовой динамики.
""")

        except Exception as e:
            st.error(f"Ошибка при обработке файла: {e}")
