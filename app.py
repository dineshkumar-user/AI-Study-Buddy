# ==========================================================
# 🎓 AI STUDY BUDDY
# Main Streamlit Application
#
# AI:
#   Gemini Cloud AI
#   Ollama Local AI
#
# Features:
#   Dashboard
#   Study Material
#   AI Chat
#   Concept Explainer
#   Smart Summary
#   AI Quiz
#   Flashcards
#   Weak Concepts
#   Study Plan
#   Progress
#   Study Timer
#   Bookmarks
#   Study Report
# ==========================================================

import streamlit as st
from datetime import datetime
import pandas as pd


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# IMPORT PROJECT MODULES
# ==========================================================

from modules.ai_engine import (
    explain_concept,
    chat_with_notes,
    generate_ai_summary,
    generate_quiz,
    generate_flashcards,
    generate_study_plan,
    generate_learning_recommendation,
    get_ai_mode,
    get_ai_status,
    gemini_available
)

from modules.document_processor import (
    extract_text
)

from modules.summarizer import (
    tfidf_summary
)

from modules.progress_tracker import (
    load_data,
    save_quiz_result,
    add_bookmark,
    remove_bookmark,
    add_study_session,
    get_progress_statistics
)

from modules.study_planner import (
    create_plan
)

from modules.report_generator import (
    create_report
)


# ==========================================================
# SESSION STATE
# ==========================================================

if "notes" not in st.session_state:
    st.session_state.notes = ""

if "quiz" not in st.session_state:
    st.session_state.quiz = []

if "quiz_results" not in st.session_state:
    st.session_state.quiz_results = []

if "flashcards" not in st.session_state:
    st.session_state.flashcards = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("🎓 AI Study Buddy")

    st.caption(
        "Your Personal AI Learning Assistant"
    )

    st.divider()

    # ------------------------------------------------------
    # DATE AND TIME
    # ------------------------------------------------------

    current_time = datetime.now()

    st.info(
        f"📅 **Date:** "
        f"{current_time.strftime('%d %B %Y')}\n\n"
        f"🕐 **Time:** "
        f"{current_time.strftime('%I:%M:%S %p')}"
    )

    st.divider()

    # ------------------------------------------------------
    # AI CONNECTION
    # ------------------------------------------------------

    st.subheader("🧠 AI Connection")

    try:

        ai_status = get_ai_status()

        if gemini_available():

            st.success(
                "☁️ Gemini Cloud AI Connected"
            )

            st.caption(
                f"Model: {ai_status.get('model', 'Gemini')}"
            )

        else:

            st.success(
                "💻 Ollama Local AI"
            )

            st.caption(
                f"Model: {ai_status.get('model', 'Llama 3.2 3B')}"
            )

    except Exception:

        st.info(
            "💻 Local AI: Ollama"
        )

        st.caption(
            "Model: Llama 3.2 3B"
        )

    st.divider()

    # ------------------------------------------------------
    # NAVIGATION
    # ------------------------------------------------------

    page = st.radio(
        "📍 Navigation",
        [
            "🏠 Dashboard",
            "📚 Study Material",
            "🤖 AI Chat",
            "💡 Concept Explainer",
            "📝 Smart Summary",
            "❓ AI Quiz",
            "🗂️ Flashcards",
            "🎯 Weak Concepts",
            "🧠 Study Plan",
            "📈 Progress",
            "⏱️ Study Timer",
            "📌 Bookmarks",
            "📄 Study Report"
        ]
    )

    st.divider()

    # ------------------------------------------------------
    # AI TECHNIQUES
    # ------------------------------------------------------

    st.subheader("🧠 AI Techniques")

    st.write("• Natural Language Processing")
    st.write("• TF-IDF")
    st.write("• Cosine Similarity")
    st.write("• Large Language Model")
    st.write("• Performance Analysis")
    st.write("• Personalized Recommendations")

    st.divider()

    try:

        st.caption(
            f"Powered by {get_ai_mode()}"
        )

    except Exception:

        st.caption(
            "Powered by Ollama + Llama 3.2 3B"
        )


# ==========================================================
# MAIN HEADER
# ==========================================================

st.title("🎓 AI Study Buddy")

st.write(
    "An AI-powered personal learning assistant "
    "for studying, summarization, quizzes and "
    "personalized learning."
)

st.divider()


# ==========================================================
# 🏠 DASHBOARD
# ==========================================================

if page == "🏠 Dashboard":

    st.subheader(
        "👋 Welcome to your AI Study Dashboard"
    )

    data = load_data()

    history = data.get(
        "quiz_history",
        []
    )

    bookmarks = data.get(
        "bookmarks",
        []
    )

    # Latest score

    if history:

        latest_score = history[-1].get(
            "percentage",
            0
        )

    else:

        latest_score = 0

    # ------------------------------------------------------
    # DASHBOARD METRICS
    # ------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📚 Study Words",
            len(
                st.session_state.notes.split()
            )
        )

    with col2:

        st.metric(
            "📝 Quiz Attempts",
            len(history)
        )

    with col3:

        st.metric(
            "🎯 Latest Score",
            f"{latest_score:.1f}%"
        )

    with col4:

        st.metric(
            "📌 Bookmarks",
            len(bookmarks)
        )

    st.divider()

    # ------------------------------------------------------
    # QUICK START
    # ------------------------------------------------------

    st.subheader("🚀 Quick Start")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            "📚 **Study Material**\n\n"
            "Upload PDF, TXT or DOCX notes."
        )

    with col2:

        st.info(
            "🤖 **AI Chat**\n\n"
            "Ask questions about your notes."
        )

    with col3:

        st.info(
            "❓ **AI Quiz**\n\n"
            "Generate quizzes from your notes."
        )

    st.divider()

    # ------------------------------------------------------
    # HOW IT WORKS
    # ------------------------------------------------------

    st.subheader(
        "🧠 How AI Study Buddy Works"
    )

    step1, step2, step3, step4 = st.columns(4)

    with step1:

        st.markdown("### 1️⃣")

        st.write(
            "Upload study material"
        )

    with step2:

        st.markdown("### 2️⃣")

        st.write(
            "AI processes content"
        )

    with step3:

        st.markdown("### 3️⃣")

        st.write(
            "Take AI quiz"
        )

    with step4:

        st.markdown("### 4️⃣")

        st.write(
            "Detect weak concepts"
        )

    st.divider()

    now = datetime.now()

    st.subheader(
        "📅 Current Date & Time"
    )

    st.write(
        now.strftime(
            "%A, %d %B %Y | %I:%M:%S %p"
        )
    )


# ==========================================================
# 📚 STUDY MATERIAL
# ==========================================================

elif page == "📚 Study Material":

    st.subheader(
        "📚 Study Material"
    )

    st.write(
        "Upload your study material or enter it manually."
    )

    # ------------------------------------------------------
    # FILE UPLOAD
    # ------------------------------------------------------

    uploaded_file = st.file_uploader(
        "📂 Upload Study Material",
        type=[
            "txt",
            "pdf",
            "docx"
        ]
    )

    if uploaded_file:

        try:

            content = extract_text(
                uploaded_file
            )

            if content:

                st.session_state.notes = content

                st.success(
                    "✅ Study material loaded successfully!"
                )

            else:

                st.warning(
                    "⚠️ The uploaded file contains no readable text."
                )

        except Exception as error:

            st.error(
                f"❌ Error reading file: {error}"
            )

    st.divider()

    # ------------------------------------------------------
    # MANUAL NOTES
    # ------------------------------------------------------

    notes = st.text_area(
        "✏️ Enter or edit your study material",
        value=st.session_state.notes,
        height=400
    )

    st.session_state.notes = notes

    # ------------------------------------------------------
    # MATERIAL STATISTICS
    # ------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "📖 Words",
            len(notes.split())
        )

    with col2:

        st.metric(
            "🔤 Characters",
            len(notes)
        )

    with col3:

        st.metric(
            "📝 Lines",
            len(notes.splitlines())
        )

    st.divider()

    # ------------------------------------------------------
    # CLEAR NOTES
    # ------------------------------------------------------

    if st.button(
        "🗑️ Clear Study Material"
    ):

        st.session_state.notes = ""

        st.session_state.quiz = []

        st.session_state.quiz_results = []

        st.session_state.flashcards = []

        st.success(
            "✅ Study material cleared!"
        )

        st.rerun()


# ==========================================================
# 🤖 AI CHAT
# ==========================================================

elif page == "🤖 AI Chat":

    st.subheader(
        "🤖 AI Chat with Your Notes"
    )

    st.info(
        f"🧠 Using {get_ai_mode()}"
    )

    if not st.session_state.notes.strip():

        st.warning(
            "⚠️ Please add study material first."
        )

    else:

        question = st.text_input(
            "💬 Ask your question",
            placeholder=(
                "Example: Explain inheritance in Python simply"
            )
        )

        if st.button(
            "🤖 Ask AI",
            type="primary"
        ):

            if not question.strip():

                st.warning(
                    "Please enter a question."
                )

            else:

                with st.spinner(
                    "🧠 AI is thinking..."
                ):

                    answer = chat_with_notes(
                        question,
                        st.session_state.notes
                    )

                st.session_state.chat_history.append(
                    {
                        "question": question,
                        "answer": answer
                    }
                )

                if str(answer).startswith("❌"):

                    st.error(
                        answer
                    )

                else:

                    st.success(
                        "🤖 AI Answer"
                    )

                    st.markdown(
                        answer
                    )

    # ------------------------------------------------------
    # CHAT HISTORY
    # ------------------------------------------------------

    if st.session_state.chat_history:

        st.divider()

        st.subheader(
            "💬 Previous Questions"
        )

        for chat in reversed(
            st.session_state.chat_history
        ):

            with st.expander(
                chat["question"]
            ):

                st.markdown(
                    chat["answer"]
                )


# ==========================================================
# 💡 CONCEPT EXPLAINER
# ==========================================================

elif page == "💡 Concept Explainer":

    st.subheader(
        "💡 AI Concept Explainer"
    )

    st.info(
        f"🧠 Using {get_ai_mode()}"
    )

    st.write(
        "Get a simple explanation of difficult concepts."
    )

    topic = st.text_input(
        "📌 Enter a concept",
        placeholder=(
            "Example: Inheritance in Python"
        )
    )

    difficulty = st.selectbox(
        "🎓 Explanation Level",
        [
            "Simple - Beginner",
            "Intermediate",
            "Detailed - Advanced"
        ]
    )

    if st.button(
        "✨ Explain Concept",
        type="primary"
    ):

        if not topic.strip():

            st.warning(
                "Please enter a concept."
            )

        else:

            with st.spinner(
                "🧠 AI is preparing the explanation..."
            ):

                result = explain_concept(
                    topic,
                    st.session_state.notes,
                    difficulty
                )

            if str(result).startswith("❌"):

                st.error(
                    result
                )

            else:

                st.markdown(
                    result
                )


# ==========================================================
# 📝 SMART SUMMARY
# ==========================================================

elif page == "📝 Smart Summary":

    st.subheader(
        "📝 Smart Summary"
    )

    st.info(
        f"🧠 AI Summary: {get_ai_mode()}"
    )

    if not st.session_state.notes.strip():

        st.warning(
            "⚠️ Please add study material first."
        )

    else:

        # --------------------------------------------------
        # AI SUMMARY
        # --------------------------------------------------

        summary_type = st.selectbox(
            "📋 Summary Type",
            [
                "Bullet Points",
                "Paragraph"
            ]
        )

        if st.button(
            "✨ Generate AI Summary",
            type="primary"
        ):

            with st.spinner(
                "🧠 AI is summarizing your notes..."
            ):

                summary = generate_ai_summary(
                    st.session_state.notes,
                    summary_type
                )

            if str(summary).startswith("❌"):

                st.error(
                    summary
                )

            else:

                st.markdown(
                    summary
                )

        st.divider()

        # --------------------------------------------------
        # TF-IDF SUMMARY
        # --------------------------------------------------

        st.subheader(
            "🔬 NLP Extractive Summary"
        )

        number = st.slider(
            "Number of important sentences",
            min_value=3,
            max_value=10,
            value=5
        )

        if st.button(
            "🔍 Generate TF-IDF Summary"
        ):

            summary = tfidf_summary(
                st.session_state.notes,
                number
            )

            if summary:

                for index, sentence in enumerate(
                    summary,
                    1
                ):

                    st.write(
                        f"**{index}.** {sentence}"
                    )

            else:

                st.warning(
                    "Could not generate summary."
                )


# ==========================================================
# ❓ AI QUIZ
# ==========================================================

elif page == "❓ AI Quiz":

    st.subheader(
        "❓ AI Quiz Generator"
    )

    st.info(
        f"🧠 Using {get_ai_mode()}"
    )

    st.write(
        "Generate an interactive multiple-choice quiz "
        "from your study material."
    )

    if not st.session_state.notes.strip():

        st.warning(
            "⚠️ Please add study material first."
        )

    else:

        number = st.slider(
            "Number of questions",
            min_value=3,
            max_value=10,
            value=5
        )

        # --------------------------------------------------
        # GENERATE QUIZ
        # --------------------------------------------------

        if st.button(
            "🎲 Generate AI Quiz",
            type="primary"
        ):

            with st.spinner(
                "🧠 AI is creating your quiz..."
            ):

                try:

                    quiz = generate_quiz(
                        st.session_state.notes,
                        number
                    )

                except Exception as error:

                    quiz = []

                    st.error(
                        f"❌ Quiz error: {error}"
                    )

            if quiz:

                st.session_state.quiz = quiz

                st.session_state.quiz_results = []

                st.success(
                    f"✅ {len(quiz)} questions generated!"
                )

            else:

                st.error(
                    "❌ Quiz generation failed."
                )

                st.info(
                    "Please check that your AI service "
                    "is available and try again."
                )

        # --------------------------------------------------
        # DISPLAY QUIZ
        # --------------------------------------------------

        if st.session_state.quiz:

            st.divider()

            st.subheader(
                "📝 Answer the Questions"
            )

            answers = {}

            for index, question in enumerate(
                st.session_state.quiz
            ):

                st.markdown(
                    f"### Question {index + 1}"
                )

                st.write(
                    question.get(
                        "question",
                        "Question unavailable"
                    )
                )

                options = question.get(
                    "options",
                    []
                )

                if options:

                    answers[index] = st.radio(
                        "Choose your answer:",
                        options,
                        key=f"quiz_answer_{index}"
                    )

                else:

                    st.warning(
                        "Options unavailable for this question."
                    )

                st.divider()

            # --------------------------------------------------
            # SUBMIT QUIZ
            # --------------------------------------------------

            if st.button(
                "✅ Submit Quiz",
                type="primary"
            ):

                results = []

                correct_count = 0

                weak_topics = []

                for index, question in enumerate(
                    st.session_state.quiz
                ):

                    selected = answers.get(
                        index
                    )

                    correct_answer = question.get(
                        "answer",
                        ""
                    )

                    correct = (
                        selected == correct_answer
                    )

                    if correct:

                        correct_count += 1

                    else:

                        weak_topics.append(
                            question.get(
                                "concept",
                                "General"
                            )
                        )

                    results.append(
                        {
                            "question":
                                question.get(
                                    "question",
                                    ""
                                ),

                            "selected":
                                selected,

                            "correct_answer":
                                correct_answer,

                            "correct":
                                correct,

                            "concept":
                                question.get(
                                    "concept",
                                    "General"
                                ),

                            "explanation":
                                question.get(
                                    "explanation",
                                    "No explanation available."
                                )
                        }
                    )

                st.session_state.quiz_results = results

                total = len(
                    st.session_state.quiz
                )

                if total > 0:

                    percentage = (
                        correct_count /
                        total
                    ) * 100

                else:

                    percentage = 0

                # Save result

                save_quiz_result(
                    correct_count,
                    total,
                    sorted(
                        set(weak_topics)
                    )
                )

                # --------------------------------------------------
                # RESULT
                # --------------------------------------------------

                st.divider()

                st.subheader(
                    "🏆 Quiz Result"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "✅ Correct",
                        correct_count
                    )

                with col2:

                    st.metric(
                        "📝 Total",
                        total
                    )

                with col3:

                    st.metric(
                        "🎯 Score",
                        f"{percentage:.1f}%"
                    )

                st.progress(
                    percentage / 100
                )

                if percentage >= 80:

                    st.success(
                        "🎉 Excellent performance!"
                    )

                elif percentage >= 50:

                    st.warning(
                        "👍 Good performance! "
                        "Keep practicing."
                    )

                else:

                    st.error(
                        "📚 More revision is recommended."
                    )

                # --------------------------------------------------
                # ANSWER REVIEW
                # --------------------------------------------------

                st.divider()

                st.subheader(
                    "📋 Answer Review"
                )

                for result in results:

                    if result["correct"]:

                        st.success(
                            "✅ Correct"
                        )

                        st.write(
                            f"**Question:** "
                            f"{result['question']}"
                        )

                        st.write(
                            f"**Your answer:** "
                            f"{result['selected']}"
                        )

                    else:

                        st.error(
                            "❌ Incorrect"
                        )

                        st.write(
                            f"**Question:** "
                            f"{result['question']}"
                        )

                        st.write(
                            f"**Your answer:** "
                            f"{result['selected']}"
                        )

                        st.write(
                            f"**Correct answer:** "
                            f"{result['correct_answer']}"
                        )

                    st.info(
                        f"💡 {result['explanation']}"
                    )

                    st.divider()

                # --------------------------------------------------
                # WEAK TOPICS
                # --------------------------------------------------

                if weak_topics:

                    st.subheader(
                        "🎯 Topics to Practice"
                    )

                    for topic in sorted(
                        set(weak_topics)
                    ):

                        st.warning(
                            f"📚 {topic}"
                        )


# ==========================================================
# 🗂️ FLASHCARDS
# ==========================================================

elif page == "🗂️ Flashcards":

    st.subheader(
        "🗂️ AI Flashcards"
    )

    st.info(
        f"🧠 Using {get_ai_mode()}"
    )

    st.write(
        "Generate AI-powered flashcards "
        "for quick revision."
    )

    if not st.session_state.notes.strip():

        st.warning(
            "⚠️ Please add study material first."
        )

    else:

        number = st.slider(
            "Number of flashcards",
            min_value=3,
            max_value=15,
            value=5
        )

        if st.button(
            "🪄 Generate Flashcards",
            type="primary"
        ):

            with st.spinner(
                "🧠 Creating flashcards..."
            ):

                try:

                    cards = generate_flashcards(
                        st.session_state.notes,
                        number
                    )

                except Exception as error:

                    cards = []

                    st.error(
                        f"❌ Flashcard error: {error}"
                    )

            if cards:

                st.session_state.flashcards = cards

                st.success(
                    f"✅ {len(cards)} flashcards created!"
                )

            else:

                st.error(
                    "❌ Could not generate flashcards."
                )

        # --------------------------------------------------
        # DISPLAY FLASHCARDS
        # --------------------------------------------------

        if st.session_state.flashcards:

            st.divider()

            st.subheader(
                "📚 Revision Cards"
            )

            for index, card in enumerate(
                st.session_state.flashcards,
                1
            ):

                question = card.get(
                    "question",
                    "Question unavailable"
                )

                answer = card.get(
                    "answer",
                    "Answer unavailable"
                )

                concept = card.get(
                    "concept",
                    "General"
                )

                with st.expander(
                    f"📌 Card {index}: {question}"
                ):

                    st.markdown(
                        "### ❓ Question"
                    )

                    st.write(
                        question
                    )

                    st.divider()

                    st.markdown(
                        "### 💡 Answer"
                    )

                    st.success(
                        answer
                    )

                    st.caption(
                        f"🧠 Concept: {concept}"
                    )

            # --------------------------------------------------
            # DOWNLOAD
            # --------------------------------------------------

            flashcard_text = ""

            for index, card in enumerate(
                st.session_state.flashcards,
                1
            ):

                flashcard_text += (
                    f"FLASHCARD {index}\n\n"
                    f"Question: "
                    f"{card.get('question', '')}\n\n"
                    f"Answer: "
                    f"{card.get('answer', '')}\n\n"
                    f"Concept: "
                    f"{card.get('concept', 'General')}\n"
                    f"{'-' * 60}\n\n"
                )

            st.download_button(
                "⬇️ Download Flashcards",
                flashcard_text,
                file_name="AI_Flashcards.txt",
                mime="text/plain"
            )


# ==========================================================
# 🎯 WEAK CONCEPTS
# ==========================================================

elif page == "🎯 Weak Concepts":

    st.subheader(
        "🎯 Weak Concept Detector"
    )

    data = load_data()

    history = data.get(
        "quiz_history",
        []
    )

    if not history:

        st.info(
            "📝 Complete at least one quiz "
            "to detect weak concepts."
        )

    else:

        concept_stats = {}

        # --------------------------------------------------
        # COUNT MISTAKES
        # --------------------------------------------------

        for attempt in history:

            for topic in attempt.get(
                "weak_topics",
                []
            ):

                if topic not in concept_stats:

                    concept_stats[topic] = 0

                concept_stats[topic] += 1

        if not concept_stats:

            st.success(
                "🎉 No weak concepts detected!"
            )

        else:

            st.write(
                "These concepts caused mistakes "
                "across your quiz attempts."
            )

            sorted_topics = sorted(
                concept_stats.items(),
                key=lambda x: x[1],
                reverse=True
            )

            # --------------------------------------------------
            # DISPLAY
            # --------------------------------------------------

            for topic, mistakes in sorted_topics:

                if mistakes >= 3:

                    status = "🔴 High Priority"

                elif mistakes == 2:

                    status = "🟠 Needs Practice"

                else:

                    status = "🟡 Review"

                col1, col2, col3 = st.columns(
                    [4, 2, 1]
                )

                with col1:

                    st.write(
                        f"📚 **{topic}**"
                    )

                with col2:

                    st.write(
                        status
                    )

                with col3:

                    st.metric(
                        "Mistakes",
                        mistakes
                    )

            # --------------------------------------------------
            # TOP WEAK CONCEPT
            # --------------------------------------------------

            st.divider()

            top_topic = sorted_topics[0]

            st.warning(
                f"🎯 **Top Priority:** "
                f"{top_topic[0]}"
            )

            st.info(
                "Recommended action:\n\n"
                "1. Review the concept\n\n"
                "2. Read your study material\n\n"
                "3. Create flashcards\n\n"
                "4. Retake the quiz"
            )


# ==========================================================
# 🧠 STUDY PLAN
# ==========================================================

elif page == "🧠 Study Plan":

    st.subheader(
        "🧠 AI Personalized Study Plan"
    )

    data = load_data()

    history = data.get(
        "quiz_history",
        []
    )

    weak_topics = []

    for attempt in history:

        weak_topics.extend(
            attempt.get(
                "weak_topics",
                []
            )
        )

    weak_topics = sorted(
        set(weak_topics)
    )

    if weak_topics:

        st.write(
            "🎯 Your weak concepts:"
        )

        for topic in weak_topics:

            st.warning(
                f"📚 {topic}"
            )

    else:

        st.info(
            "No weak concepts detected yet. "
            "Take a quiz to generate a personalized plan."
        )

    st.divider()

    study_hours = st.slider(
        "⏰ Study hours per day",
        min_value=1,
        max_value=8,
        value=2
    )

    if st.button(
        "🧠 Generate Study Plan",
        type="primary"
    ):

        with st.spinner(
            "🧠 Creating your personalized study plan..."
        ):

            try:

                plan = create_plan(
                    weak_topics,
                    study_hours
                )

                st.markdown(
                    plan
                )

            except Exception as error:

                st.error(
                    f"❌ Could not create study plan: {error}"
                )


# ==========================================================
# 📈 PROGRESS
# ==========================================================

elif page == "📈 Progress":

    st.subheader(
        "📈 Learning Progress"
    )

    stats = get_progress_statistics()

    data = load_data()

    history = data.get(
        "quiz_history",
        []
    )

    # --------------------------------------------------
    # MAIN METRICS
    # --------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "🎯 Latest Score",
            f"{stats.get('latest_score', 0)}%"
        )

    with col2:

        st.metric(
            "📊 Average Score",
            f"{stats.get('average_score', 0)}%"
        )

    with col3:

        st.metric(
            "🏆 Best Score",
            f"{stats.get('best_score', 0)}%"
        )

    with col4:

        st.metric(
            "🔥 Learning Streak",
            f"{stats.get('streak', 0)} days"
        )

    st.divider()

    # --------------------------------------------------
    # SECONDARY METRICS
    # --------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "📝 Quiz Attempts",
            stats.get(
                "quiz_attempts",
                len(history)
            )
        )

    with col2:

        total_minutes = stats.get(
            "total_minutes",
            0
        )

        hours = total_minutes // 60

        minutes = total_minutes % 60

        st.metric(
            "⏱️ Study Time",
            f"{hours}h {minutes}m"
        )

    st.divider()

    # --------------------------------------------------
    # IMPROVEMENT
    # --------------------------------------------------

    improvement = stats.get(
        "improvement",
        0
    )

    if improvement > 0:

        st.success(
            f"📈 Your latest score improved by "
            f"{improvement} percentage points."
        )

    elif improvement < 0:

        st.warning(
            f"📉 Your latest score decreased by "
            f"{abs(improvement)} percentage points."
        )

    else:

        st.info(
            "📊 Take another quiz to measure your improvement."
        )

    # --------------------------------------------------
    # SCORE HISTORY
    # --------------------------------------------------

    if history:

        st.divider()

        st.subheader(
            "📊 Quiz Score History"
        )

        scores = [
            item.get(
                "percentage",
                0
            )
            for item in history
        ]

        chart_df = pd.DataFrame(
            {
                "Quiz Attempt":
                    range(
                        1,
                        len(scores) + 1
                    ),

                "Score":
                    scores
            }
        )

        st.line_chart(
            chart_df.set_index(
                "Quiz Attempt"
            )
        )

        # --------------------------------------------------
        # HISTORY TABLE
        # --------------------------------------------------

        st.subheader(
            "📋 Detailed History"
        )

        history_df = pd.DataFrame(
            [
                {
                    "Date":
                        item.get(
                            "date",
                            ""
                        ),

                    "Score":
                        f"{item.get('percentage', 0)}%",

                    "Correct":
                        item.get(
                            "correct",
                            0
                        ),

                    "Total":
                        item.get(
                            "total",
                            0
                        ),

                    "Weak Topics":
                        ", ".join(
                            item.get(
                                "weak_topics",
                                []
                            )
                        )
                }

                for item in reversed(history)
            ]
        )

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )


# ==========================================================
# ⏱️ STUDY TIMER
# ==========================================================

elif page == "⏱️ Study Timer":

    st.subheader(
        "⏱️ Study Session Timer"
    )

    st.write(
        "Record the amount of time you spend studying."
    )

    minutes = st.number_input(
        "⏰ Study session duration (minutes)",
        min_value=1,
        max_value=180,
        value=25
    )

    st.info(
        f"Recommended session: "
        f"{minutes} minutes"
    )

    if st.button(
        "✅ Record Study Session",
        type="primary"
    ):

        add_study_session(
            int(minutes)
        )

        st.success(
            f"✅ {minutes} minute study session recorded!"
        )


# ==========================================================
# 📌 BOOKMARKS
# ==========================================================

elif page == "📌 Bookmarks":

    st.subheader(
        "📌 Bookmarked Topics"
    )

    topic = st.text_input(
        "Enter a topic to bookmark",
        placeholder="Example: Python Inheritance"
    )

    if st.button(
        "📌 Add Bookmark"
    ):

        if topic.strip():

            add_bookmark(
                topic.strip()
            )

            st.success(
                "✅ Topic bookmarked!"
            )

        else:

            st.warning(
                "Please enter a topic."
            )

    data = load_data()

    bookmarks = data.get(
        "bookmarks",
        []
    )

    st.divider()

    if bookmarks:

        for index, bookmark in enumerate(
            bookmarks
        ):

            col1, col2 = st.columns(
                [5, 1]
            )

            with col1:

                st.write(
                    f"📌 **{bookmark}**"
                )

            with col2:

                if st.button(
                    "Remove",
                    key=f"remove_bookmark_{index}"
                ):

                    remove_bookmark(
                        bookmark
                    )

                    st.rerun()

    else:

        st.info(
            "No bookmarked topics yet."
        )


# ==========================================================
# 📄 STUDY REPORT
# ==========================================================

elif page == "📄 Study Report":

    st.subheader(
        "📄 AI Study Report"
    )

    data = load_data()

    history = data.get(
        "quiz_history",
        []
    )

    bookmarks = data.get(
        "bookmarks",
        []
    )

    study_sessions = data.get(
        "study_sessions",
        []
    )

    stats = get_progress_statistics()

    # --------------------------------------------------
    # LATEST QUIZ
    # --------------------------------------------------

    if history:

        latest = history[-1]

        score = latest.get(
            "percentage",
            0
        )

        weak_topics = latest.get(
            "weak_topics",
            []
        )

    else:

        score = 0

        weak_topics = []

    # --------------------------------------------------
    # REPORT PREVIEW
    # --------------------------------------------------

    st.subheader(
        "📊 Report Preview"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "🎯 Latest Score",
            f"{score}%"
        )

    with col2:

        st.metric(
            "📊 Average Score",
            f"{stats.get('average_score', 0)}%"
        )

    with col3:

        st.metric(
            "🏆 Best Score",
            f"{stats.get('best_score', 0)}%"
        )

    with col4:

        st.metric(
            "⏱️ Study Time",
            f"{stats.get('total_minutes', 0)} min"
        )

    st.divider()

    # --------------------------------------------------
    # WEAK CONCEPTS
    # --------------------------------------------------

    st.subheader(
        "🎯 Weak Concepts"
    )

    if weak_topics:

        for topic in weak_topics:

            st.warning(
                f"📚 {topic}"
            )

    else:

        st.success(
            "🎉 No weak concepts recorded "
            "in the latest quiz."
        )

    st.divider()

    # --------------------------------------------------
    # BOOKMARKS
    # --------------------------------------------------

    st.subheader(
        "📌 Bookmarked Topics"
    )

    if bookmarks:

        for bookmark in bookmarks:

            st.write(
                f"📌 {bookmark}"
            )

    else:

        st.info(
            "No bookmarks available."
        )

    st.divider()

    # --------------------------------------------------
    # REPORT SUMMARY
    # --------------------------------------------------

    report_summary = st.text_area(
        "✏️ Report Summary",
        value=(
            "This report summarizes my learning "
            "performance using AI Study Buddy."
        ),
        height=120
    )

    # --------------------------------------------------
    # GENERATE PDF
    # --------------------------------------------------

    if st.button(
        "📄 Generate PDF Report",
        type="primary"
    ):

        try:

            with st.spinner(
                "📄 Creating your study report..."
            ):

                filepath = create_report(
                    "study_report.pdf",
                    score,
                    report_summary,
                    weak_topics,
                    history,
                    bookmarks,
                    study_sessions
                )

            with open(
                filepath,
                "rb"
            ) as file:

                pdf_data = file.read()

            st.success(
                "✅ Your study report is ready!"
            )

            st.download_button(
                "⬇️ Download Study Report",
                pdf_data,
                file_name="AI_Study_Buddy_Report.pdf",
                mime="application/pdf"
            )

        except TypeError:

            # Compatibility with an older
            # create_report() function

            try:

                filepath = create_report(
                    "study_report.pdf",
                    score,
                    report_summary,
                    weak_topics
                )

                with open(
                    filepath,
                    "rb"
                ) as file:

                    pdf_data = file.read()

                st.success(
                    "✅ Your study report is ready!"
                )

                st.download_button(
                    "⬇️ Download Study Report",
                    pdf_data,
                    file_name="AI_Study_Buddy_Report.pdf",
                    mime="application/pdf"
                )

            except Exception as error:

                st.error(
                    f"❌ Report generation failed: {error}"
                )

        except Exception as error:

            st.error(
                f"❌ Report generation failed: {error}"
            )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "🎓 AI Study Buddy | "
    "Python + Streamlit + NLP + "
    "Machine Learning + AI/LLM"
)