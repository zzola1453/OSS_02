import streamlit as st

def main():
    st.title("📝 간단 투두리스트")

    # 세션 상태에 tasks 리스트 초기화
    if "tasks" not in st.session_state:
        st.session_state.tasks = []

    # 할 일 추가 폼
    with st.form("add_task_form"):
        new_task = st.text_input("새 할 일 입력")
        submitted = st.form_submit_button("추가")
        if submitted and new_task.strip():
            st.session_state.tasks.append({"task": new_task.strip(), "done": False})

    st.write("---")

    # 할 일 리스트 출력 및 체크박스 토글
    for idx, task in enumerate(st.session_state.tasks):
        checked = st.checkbox(task["task"], value=task["done"], key=idx)
        st.session_state.tasks[idx]["done"] = checked

    st.write("---")

    # 완료된 할 일 삭제 버튼
    if st.button("완료된 할 일 삭제"):
        st.session_state.tasks = [task for task in st.session_state.tasks if not task["done"]]

if __name__ == "__main__":
    main()
