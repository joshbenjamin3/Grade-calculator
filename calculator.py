import streamlit as st

# Theme configuration
st.set_page_config(
    page_title="Grade Calculator",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Apply dark theme
st.markdown("""
<style>
    .stApp {
        background-color: #1E1E1E;
    }
    .stNumberInput, .stTextInput, .stSelectbox {
        background-color: #2E2E2E;
    }
    /* Text colors */
    .stMarkdown, .stText, .stTitle, .stSubheader, .stNumberInput label, 
    .stTextInput label, .stSelectbox label, .stRadio label, .stCheckbox label {
        color: #FFFFFF !important;
    }
    /* Input text colors */
    .stNumberInput input, .stTextInput input {
        color: #FFFFFF !important;
    }
    /* Checkbox and radio colors */
    .stCheckbox .stCheckbox, .stRadio .stRadio {
        color: #FFFFFF !important;
    }
    /* Sidebar colors */
    .css-1d391kg, .css-1v0mbdj {
        background-color: #1E1E1E !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("Grade Calculator")

st.markdown("""
This app helps you calculate your overall grade and predict what you need on future exams to reach your target grade.

### Grade Components:
- Homework: **5%**
- Discussion Engagement: **10%**
- Three Midterm Exams: **20%** each (total **60%**)
- Final Exam: **25%**
""")

# Create two columns for the layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Enter Your Grades")
    
    # Checkboxes to indicate which grades are available
    st.write("Check the boxes for grades you have received:")
    has_homework = st.checkbox("I have my homework grade", value=True)
    has_discussion = st.checkbox("I have my discussion grade", value=True)
    has_mid1 = st.checkbox("I have my Midterm 1 grade", value=True)
    has_mid2 = st.checkbox("I have my Midterm 2 grade", value=True)
    has_mid3 = st.checkbox("I have my Midterm 3 grade", value=False)
    has_final = st.checkbox("I have my Final Exam grade", value=False)
    
    # Input fields for each component (as percentages)
    homework = st.number_input("Homework grade (percentage)", min_value=0.0, max_value=100.0, value=100.0, disabled=not has_homework)
    discussion = st.number_input("Discussion engagement (percentage)", min_value=0.0, max_value=100.0, value=100.0, disabled=not has_discussion)
    mid1 = st.number_input("Midterm 1 score (percentage)", min_value=0.0, max_value=100.0, value=80.0, disabled=not has_mid1)
    mid2 = st.number_input("Midterm 2 score (percentage)", min_value=0.0, max_value=100.0, value=80.0, disabled=not has_mid2)
    mid3 = st.number_input("Midterm 3 score (percentage)", min_value=0.0, max_value=100.0, value=80.0, disabled=not has_mid3)
    final = st.number_input("Final exam score (percentage)", min_value=0.0, max_value=100.0, value=90.0, disabled=not has_final)

with col2:
    st.subheader("Grade Prediction")
    target_grade = st.number_input("Target Overall Grade (%)", min_value=0.0, max_value=100.0, value=80.0)
    
    # Calculate current grade based on entered components
    current_grade = (homework * 0.05 +
                    discussion * 0.10 +
                    mid1 * 0.20 +
                    mid2 * 0.20 +
                    mid3 * 0.20 +
                    final * 0.25)
    
    st.subheader("Current Grade")
    st.write(f"{current_grade:.2f}%")
    
    # Calculate what's needed on remaining components
    if st.checkbox("Show what's needed on remaining exams"):
        # Calculate points already earned from completed components
        earned_points = 0
        if has_homework:
            earned_points += homework * 0.05
        if has_discussion:
            earned_points += discussion * 0.10
        if has_mid1:
            earned_points += mid1 * 0.20
        if has_mid2:
            earned_points += mid2 * 0.20
        if has_mid3:
            earned_points += mid3 * 0.20
        if has_final:
            earned_points += final * 0.25
        
        # Calculate points needed from remaining components
        needed_points = target_grade - earned_points
        
        # Calculate required scores
        if needed_points > 0:
            remaining_weight = 0
            if not has_mid3:
                remaining_weight += 0.20
            if not has_final:
                remaining_weight += 0.25
            
            if remaining_weight > 0:
                st.write("To reach your target grade, you need:")
                if not has_mid3:
                    mid3_needed = (needed_points - (final * 0.25 if has_final else 0)) / 0.20
                    st.write(f"- Midterm 3: {max(0, mid3_needed):.2f}%")
                if not has_final:
                    final_needed = (needed_points - (mid3 * 0.20 if has_mid3 else 0)) / 0.25
                    st.write(f"- Final Exam: {max(0, final_needed):.2f}%")
                
                if (not has_mid3 and mid3_needed > 100) or (not has_final and final_needed > 100):
                    st.warning("⚠️ Note: Some required scores exceed 100%. You may need to adjust your target grade.")
            else:
                st.info("You have entered all grades. No remaining exams to predict.")
        else:
            st.success("🎉 You've already met your target grade!")

# Grade cutoff information
st.subheader("Approximate Grade Cutoffs")
st.markdown("""
- A-: 80% (roughly fours and fives on exams and full discussion engagement)
- B-: 70% (roughly threes and fours on exams and full discussion engagement)
- C-: 50% (roughly twos and threes on exams and full discussion engagement)
- D-: 40%
- F: Below 40%

*Note: These are approximate cutoffs. Final cutoffs may be adjusted lower but will not be set higher.*
""") 