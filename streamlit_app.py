import streamlit as st

import streamlit as st
import random

st.set_page_config(page_title="곱셈·나눗셈 문제", layout="centered")

def generate_questions(n=10):
    qs = []
    for _ in range(n):
        if random.choice([True, False]):
            a = random.randint(2, 12)
            b = random.randint(2, 12)
            qs.append({"text": f"{a} × {b}", "answer": a * b, "type": "mul"})
        else:
            b = random.randint(2, 12)
            a = random.randint(2, 12)
            dividend = a * b  # 나눗셈은 항상 정수 결과로 생성
            qs.append({"text": f"{dividend} ÷ {b}", "answer": a, "type": "div"})
    return qs

if "questions" not in st.session_state:
    st.session_state.questions = generate_questions(10)
    st.session_state.submitted = False

st.title("곱셈 · 나눗셈 연습 (10문제)")
st.write("각 문제에 답을 입력하고 제출하세요. 정답은 정수로 입력합니다.")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("새 문제 생성"):
        st.session_state.questions = generate_questions(10)
        st.session_state.submitted = False

with col2:
    if st.button("답안 초기화"):
        for i in range(len(st.session_state.questions)):
            key = f"ans_{i}"
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.submitted = False

with st.form(key="quiz_form"):
    for i, q in enumerate(st.session_state.questions):
        st.write(f"{i+1}. {q['text']}")
        st.number_input("정답", key=f"ans_{i}", step=1, format="%d", value=0)
    submitted = st.form_submit_button("제출")

if submitted:
    correct = 0
    results = []
    for i, q in enumerate(st.session_state.questions):
        user_ans = st.session_state.get(f"ans_{i}", None)
        is_correct = (user_ans == q["answer"])
        if is_correct:
            correct += 1
        results.append((i+1, q["text"], user_ans, q["answer"], is_correct))

    st.session_state.submitted = True
    st.write(f"결과: {correct} / {len(st.session_state.questions)}")
    for idx, text, user, ans, ok in results:
        mark = "✅ 정답" if ok else "❌ 오답"
        st.write(f"{idx}. {text} — 입력: {user} / 정답: {ans} — {mark}")

if st.session_state.submitted and not submitted:
    # 이전 제출 결과 유지해서 보여주기
    st.write("이전 제출 결과가 표시됩니다. 새 문제를 만들거나 답안 초기화를 이용하세요.")
    correct = sum(1 for i, q in enumerate(st.session_state.questions)
                  if st.session_state.get(f"ans_{i}", None) == q["answer"])
    st.write(f"결과: {correct} / {len(st.session_state.questions)}")