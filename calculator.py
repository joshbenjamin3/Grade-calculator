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
This app calculates your overall grade based on the following weighted components:
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
    mid3 = st.number_input("Midterm 3 score (percentage)", min_value=0.0, max_value=100.0, value=0.0, disabled=not has_mid3)
    final = st.number_input("Final exam score (percentage)", min_value=0.0, max_value=100.0, value=0.0, disabled=not has_final)

with col2:
    st.subheader("Grade Prediction")
    target_grade = st.number_input("Target Overall Grade (%)", min_value=0.0, max_value=100.0, value=80.0)
    
    # Calculate current grade based on entered components
    current_grade = 0
    total_weight = 0
    
    # Define weights
    weights = {
        'homework': 0.05,
        'discussion': 0.10,
        'mid1': 0.20,
        'mid2': 0.20,
        'mid3': 0.20,
        'final': 0.25
    }
    
    # Calculate current grade and total weight
    if has_homework:
        current_grade += homework * weights['homework']
        total_weight += weights['homework']
    if has_discussion:
        current_grade += discussion * weights['discussion']
        total_weight += weights['discussion']
    if has_mid1:
        current_grade += mid1 * weights['mid1']
        total_weight += weights['mid1']
    if has_mid2:
        current_grade += mid2 * weights['mid2']
        total_weight += weights['mid2']
    if has_mid3:
        current_grade += mid3 * weights['mid3']
        total_weight += weights['mid3']
    if has_final:
        current_grade += final * weights['final']
        total_weight += weights['final']
    
    # Calculate current percentage of completed work
    if total_weight > 0:
        # Split calculation for debugging
        ratio = current_grade / total_weight
        current_percentage = ratio
        
        # --- DEBUGGING START ---
        # st.write(f"(Debug: current_grade = {current_grade})") 
        # st.write(f"(Debug: total_weight = {total_weight})")
        # st.write(f"(Debug: calculated ratio [grade/weight] = {ratio})") # Added ratio debug
        # st.write(f"(Debug: final percentage [=ratio] = {current_percentage})") # Updated debug label
        # --- DEBUGGING END ---
        
        st.subheader("Current Progress") # Moved subheader down
        st.write(f"Points Earned: {current_grade:.2f}%")
        st.write(f"Completed: {total_weight*100:.0f}% of total grade")
        st.write(f"Current Average: {current_percentage:.2f}%") # Display the correct percentage
    else:
        st.info("Please enter at least one grade to see your progress.")
    
    # Calculate what's needed on remaining components
    if st.checkbox("Show what's needed to reach target grade", value=True): # Default checkbox to True
        if total_weight < 1.0:  # Only show if there are remaining grades
            remaining_weight = 1.0 - total_weight
            points_needed = target_grade - current_grade
            
            if remaining_weight > 0: # Avoid division by zero if total_weight is exactly 1.0
                required_average_on_remaining = points_needed / remaining_weight
                
                st.subheader("Prediction Results") # Renamed subheader
                st.write(f"To reach your target grade of **{target_grade:.2f}%**, you need an average score of:")
                st.metric(label="Average on Remaining Assignments", value=f"{required_average_on_remaining:.2f}%") # Use metric for better display

                # Determine which assignments are remaining
                remaining_assignments = []
                if not has_mid3: remaining_assignments.append(f"Midterm 3 ({weights['mid3']*100:.0f}%)")
                if not has_final: remaining_assignments.append(f"Final Exam ({weights['final']*100:.0f}%)")
                # Add checks for other components if they could be unchecked
                if not has_homework: remaining_assignments.append(f"Homework ({weights['homework']*100:.0f}%)")
                if not has_discussion: remaining_assignments.append(f"Discussion ({weights['discussion']*100:.0f}%)")
                if not has_mid1: remaining_assignments.append(f"Midterm 1 ({weights['mid1']*100:.0f}%)")
                if not has_mid2: remaining_assignments.append(f"Midterm 2 ({weights['mid2']*100:.0f}%)")
                
                if remaining_assignments:
                    st.write(f"*Remaining assignments contributing {remaining_weight*100:.0f}% to the total grade:*")
                    st.write(f"  - {', '.join(remaining_assignments)}")

                # Update warning logic based on the average needed
                if required_average_on_remaining > 100:
                    st.warning(f"⚠️ Achieving an average of {required_average_on_remaining:.2f}% on the remaining assignments is impossible (max is 100%). You may need to adjust your target grade.")
                elif required_average_on_remaining < 0:
                     # If points_needed is negative, the target is already met or exceeded.
                     st.success(f"🎉 You've already met or exceeded your target grade of {target_grade:.2f}% based on current entries!")
                else:
                     # Provide context if the score is achievable
                     st.info(f"This average score of {required_average_on_remaining:.2f}% across the remaining assignments is needed to reach your goal.")

            else: # points_needed <= 0 but remaining_weight > 0
                 st.success(f"🎉 You've already met or exceeded your target grade of {target_grade:.2f}% based on current entries!")
        
        elif total_weight >= 1.0 : # total_weight is 1.0 or more (all grades entered)
            st.info("You have entered all grades. Your final grade is calculated.")
            # Optionally show comparison to target grade
            if current_grade >= target_grade:
                 st.success(f"Your final grade of {current_grade:.2f}% meets or exceeds your target of {target_grade:.2f}%!")
            else:
                 st.warning(f"Your final grade of {current_grade:.2f}% is below your target of {target_grade:.2f}%.")
        # Removed the outer else for points_needed <= 0 as it's handled within the required_average_on_remaining logic now.

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