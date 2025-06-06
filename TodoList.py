import streamlit as st
import time

# 페이지 설정
st.set_page_config(page_title="버킷리스트", layout="centered")

# 다크모드 + 버튼 스타일 + 폰트 조정
custom_css = """
<style>
body {
    background-color: #121212;
    color: #e0e0e0;
}
.stButton > button {
    padding: 8px 14px !important;
    margin: 0 4px !important;
    font-size: 18px !important;
    border: none !important;
    background-color: #2e2e2e !important;
    color: #e0e0e0 !important;
    border-radius: 6px !important;
    transition: background-color 0.3s ease;
    cursor: pointer;
}
.stButton > button:hover {
    background-color: #444444 !important;
}
.stButton > button[disabled] {
    background-color: #555555 !important;
    color: #999999 !important;
    cursor: default !important;
}
.css-1d391kg, .css-1aumxhk, div[data-testid="stMarkdownContainer"] p, .stMarkdown {
    font-size: 20px !important;
}
th, td {
    font-size: 20px !important;
    font-weight: bold !important;
}
.tag-emoji {
    margin-right: 8px;
    font-size: 22px;
    vertical-align: middle;
}
.bucket-item {
    font-size: 20px;
    vertical-align: middle;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 태그 목록과 이모지
DEFAULT_TAGS = ["음식", "여행", "오락", "운동", "학습", "기타"]
TAG_EMOJIS = {
    "음식": "🍔",
    "여행": "✈️",
    "오락": "🎮",
    "운동": "🏃‍♂️",
    "학습": "📚",
    "기타": "📝"
}

# 태그 이모지 HTML 렌더링
def render_tag(tag):
    emoji = TAG_EMOJIS.get(tag, "🏷️")
    return f'<span class="tag-emoji" title="{tag}">{emoji}</span>'

def main():
    st.title("🎯 개인 버킷 리스트")

    # 세션 상태 초기화
    if "bucket_list" not in st.session_state:
        st.session_state.bucket_list = []
    if "completed" not in st.session_state:
        st.session_state.completed = {}
    if "show_congrats" not in st.session_state:
        st.session_state.show_congrats = False

    # 항목 추가 폼
    with st.form("add_bucket_form", clear_on_submit=True):
        new_item = st.text_input("새 버킷 리스트 항목 추가")
        new_tags = st.multiselect("태그 선택 (선택하지 않으면 자동 '기타')", options=DEFAULT_TAGS)
        custom_tags_input = st.text_input("직접 태그 입력 (콤마로 구분)")
        submitted = st.form_submit_button("➕ 추가")

    if submitted:
        custom_tags = [tag.strip() for tag in custom_tags_input.split(",") if tag.strip()]
        all_tags = list(set(new_tags + custom_tags))
        if not all_tags:
            all_tags = ["기타"]
        if new_item.strip():
            st.session_state.bucket_list.append({"item": new_item.strip(), "tags": all_tags})
            st.rerun()
        else:
            st.error("항목을 입력해주세요.")

    st.markdown("---")

    st.markdown("🎯 버킷리스트 현황")
    if st.session_state.bucket_list:
        # 헤더
        cols = st.columns([1.5, 6, 3])
        cols[0].markdown("**우선순위**")
        cols[1].markdown("**버킷리스트**")
        cols[2].markdown("**우선순위변경/삭제**")

        # 리스트 표시
        for idx, entry in enumerate(st.session_state.bucket_list):
            cols = st.columns([1.5, 6, 3])
            cols[0].markdown(f"**{idx + 1}**")

            with cols[1]:
                check_col, text_col = st.columns([0.3, 5.7])
                key = f"check_{idx}"
                if key not in st.session_state.completed:
                    st.session_state.completed[key] = False
                with check_col:
                    checked = st.checkbox("", value=st.session_state.completed[key], key=key)
                with text_col:
                    if checked and not st.session_state.completed[key]:
                        st.session_state.completed[key] = True
                        st.balloons()
                        st.session_state.show_congrats = True
                    elif not checked and st.session_state.completed[key]:
                        st.session_state.completed[key] = False

                    tags_html = "".join([render_tag(tag) for tag in entry["tags"]])
                    text = entry["item"]
                    if st.session_state.completed[key]:
                        text = f"~~{text}~~"
                    st.markdown(f'{tags_html}<span class="bucket-item">{text}</span>', unsafe_allow_html=True)

            with cols[2]:
                up_disabled = idx == 0
                down_disabled = idx == len(st.session_state.bucket_list) - 1
                col_buttons = st.columns([1, 1, 1])
                with col_buttons[0]:
                    if st.button("⬆️", key=f"up_{idx}", disabled=up_disabled):
                        st.session_state.bucket_list[idx], st.session_state.bucket_list[idx - 1] = st.session_state.bucket_list[idx - 1], st.session_state.bucket_list[idx]
                        st.rerun()
                with col_buttons[1]:
                    if st.button("⬇️", key=f"down_{idx}", disabled=down_disabled):
                        st.session_state.bucket_list[idx], st.session_state.bucket_list[idx + 1] = st.session_state.bucket_list[idx + 1], st.session_state.bucket_list[idx]
                        st.rerun()
                with col_buttons[2]:
                    if st.button("❌", key=f"del_{idx}"):
                        st.session_state.bucket_list.pop(idx)
                        st.rerun()
    else:
        st.info("아직 버킷 리스트가 없습니다. 항목을 추가해보세요!")

    # 완료 축하 애니메이션
    if st.session_state.show_congrats:
        st.markdown("""
        <style>
        .congrats-container {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: rgba(0, 128, 0, 0.7);
            color: white;
            padding: 24px 40px;
            border-radius: 16px;
            z-index: 9999;
            font-size: 28px;
            font-weight: bold;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0, 128, 0, 0.6);
            animation: fadeout 2s forwards;
        }
        .balloon {
            position: fixed;
            bottom: 10%;
            left: 50%;
            width: 60px;
            height: 80px;
            background: radial-gradient(circle at 30% 30%, #ff4d4d, #b30000);
            border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
            filter: drop-shadow(0 0 2px #b30000);
            animation: floatUp 2s ease forwards, sway 2s ease-in-out infinite;
            transform-origin: 50% 100%;
            opacity: 1;
            z-index: 10000;
        }
        .balloon:nth-child(2) {
            background: radial-gradient(circle at 30% 30%, #4d94ff, #004080);
            left: 45%;
            animation-delay: 0.3s;
        }
        .balloon:nth-child(3) {
            background: radial-gradient(circle at 30% 30%, #4dff88, #007040);
            left: 55%;
            animation-delay: 0.6s;
        }
        @keyframes floatUp {
            0% { bottom: 10%; opacity: 1; transform: translateY(0) scale(1);}
            100% { bottom: 80%; opacity: 0; transform: translateY(-50px) scale(1.1);}
        }
        @keyframes sway {
            0%, 100% { transform: rotate(0deg);}
            50% { transform: rotate(10deg);}
        }
        @keyframes fadeout {
            0% {opacity: 1;}
            100% {opacity: 0;}
        }
        </style>

        <div class="congrats-container">축하합니다!</div>
        <div class="balloon"></div>
        <div class="balloon"></div>
        <div class="balloon"></div>
        """, unsafe_allow_html=True)

        time.sleep(2)
        st.session_state.show_congrats = False
        st.rerun()

    st.markdown("---")
    # GitHub 아이콘 링크 추가
    st.markdown(f"""
    <div style="text-align: center; margin-top: 30px;">
        <a href="https://github.com/your_username" target="_blank" style="display: inline-block;">
            <div style="
                width: 48px;
                height: 48px;
                background-color: white;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 0 6px rgba(255,255,255,0.4);
                margin: 0 auto;
                transition: 0.3s;
            ">
                <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png"
                    alt="GitHub" width="28" height="28" style="opacity: 0.9; display: block;">
            </div>
        </a>
        <p></p>
        <p style="font-size: 12px;">creator : Seongtaek Lim</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
