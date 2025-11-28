# ui/dashboard.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

# ДОБАВЛЯЕМ ПУТИ ПЕРЕД ИМПОРТОМ models!
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Теперь импортируем
try:
    from models.video_tracker import analyze_video
except ImportError as e:
    st.error(f"Ошибка импорта: {e}")
    st.error(f"Project root: {project_root}")
    st.error(f"Python path: {sys.path}")
    st.stop()

st.set_page_config(page_title="Заводской видео-анализ", layout="wide")
st.title("Детекция и трекинг людей на заводе")
st.caption("Поддерживаются все популярные форматы: .mp4, .mov, .avi, .mkv, .webm и др.")

# Принимаем ВСЕ видеоформаты
uploaded_file = st.file_uploader(
    "Загрузи видео с завода (поддерживается .MOV, .mov, .mp4 и любые другие)",
    type=["mp4", "mov", "MOV", "avi", "mkv", "webm", "m4v", "mpg", "mpeg", "wmv", "flv"]
)

if uploaded_file is not None:
    # Сохраняем файл с оригинальным расширением (важно для OpenCV!)
    suffix = os.path.splitext(uploaded_file.name)[1].lower()   # например ".mov"
    temp_path = f"temp_video{suffix}"
    
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.video(temp_path)
    st.info(f"Формат файла: **{suffix.upper()}** — поддерживается")

    if st.button("Запустить анализ", type="primary"):
        with st.spinner("Обработка видео… (зависит от длины, обычно 30–90 сек)"):
            try:
                df = analyze_video(temp_path)
                
                if df.empty or "person_id" not in df.columns:
                    st.warning("На видео не обнаружено людей")
                else:
                    unique = df["person_id"].nunique()
                    st.success(f"Готово! Найдено **{unique}** уникальных человек(а)")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader("Timeline активности людей")
                        fig, ax = plt.subplots(figsize=(10, 4))
                        for pid in df["person_id"].unique():
                            person = df[df["person_id"] == pid]
                            ax.plot(person["frame"], [pid] * len(person), "o-", label=f"ID {pid}")
                        ax.set_xlabel("Кадр")
                        ax.set_ylabel("ID человека")
                        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
                        st.pyplot(fig)

                    with col2:
                        st.subheader("Heatmap — горячие зоны")
                        fig2, ax2 = plt.subplots(figsize=(8, 6))
                        sns.kdeplot(
                            data=df,
                            x="center_x",
                            y="center_y",
                            fill=True,
                            cmap="Reds",
                            ax=ax2
                        )
                        ax2.invert_yaxis()
                        ax2.set_title("Где чаще всего бывают люди")
                        st.pyplot(fig2)

                    st.download_button(
                        "Скачать CSV с логами",
                        df.to_csv(index=False).encode(),
                        "factory_people_logs.csv",
                        "text/csv"
                    )
            except Exception as e:
                st.error(f"Ошибка при обработке: {e}")
                st.info("Попробуй другое видео или перезагрузи страницу")

else:
    st.info("Загрузи видео любого формата — система автоматически распознает")