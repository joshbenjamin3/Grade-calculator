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
    drop_lowest = st.checkbox("Drop Midterm 1 (if M1 < M2 and all three entered)?", value=False)
    potential_curve = st.number_input("Potential Curve Adjustment (Points)", min_value=0.0, step=0.5, value=0.0, help="Enter potential points added by a curve to see how it affects requirements.")
    
    # Calculate current grade based on entered components
    current_grade = 0
    total_weight = 0
    midterm_scores = {}
    
    # Define weights
    weights = {
        'homework': 0.05,
        'discussion': 0.10,
        'mid1': 0.20,
        'mid2': 0.20,
        'mid3': 0.20,
        'final': 0.25
    }
    
    # --- Calculate provisional grade and weight ---
    component_inputs = {
        'homework': (homework, has_homework),
        'discussion': (discussion, has_discussion),
        'mid1': (mid1, has_mid1),
        'mid2': (mid2, has_mid2),
        'mid3': (mid3, has_mid3),
        'final': (final, has_final)
    }
    
    all_midterms_entered = has_mid1 and has_mid2 and has_mid3
    
    for name, (score, has_grade) in component_inputs.items():
        if has_grade:
            current_grade += score * weights[name]
            total_weight += weights[name]
            if name in ['mid1', 'mid2', 'mid3']:
                midterm_scores[name] = score

    # --- Apply drop logic for Midterm 1 if applicable ---
    dropped_midterm_info = ""
    midterm_to_drop = None 
    if drop_lowest and all_midterms_entered: 
        if midterm_scores['mid1'] < midterm_scores['mid2']:
            midterm1_score = midterm_scores['mid1']
            current_grade -= midterm1_score * weights['mid1']
            total_weight -= weights['mid1']
            midterm_to_drop = 'mid1'
            dropped_midterm_info = f"*Midterm 1 ({midterm1_score:.2f}%) dropped (was lower than Midterm 2: {midterm_scores['mid2']:.2f}%).*"
        else:
             dropped_midterm_info = f"*Midterm 1 ({midterm_scores['mid1']:.2f}%) not dropped (not lower than Midterm 2: {midterm_scores['mid2']:.2f}%).*"

    # --- Display Current Progress ---
    if total_weight > 0:
        st.subheader("Current Progress")
        st.write(f"Points Earned: {current_grade:.2f}% (out of {total_weight*100:.0f}% possible)") 
        st.write(f"Completed: {total_weight*100:.0f}% of total grade")
        if dropped_midterm_info:
            st.info(dropped_midterm_info) 
        st.write(f"Current Average Score on Included Work: {current_grade / total_weight:.2f}%")
    else:
        st.info("Please enter at least one grade to see your progress.")
    
    # --- Calculate and Display Predictions ---
    if st.checkbox("Show what's needed to reach target grade", value=True):
        max_possible_weight = 1.0 - (weights['mid1'] if midterm_to_drop else 0.0)
        
        if total_weight < max_possible_weight: 
            remaining_weight = max_possible_weight - total_weight
            
            # Adjust points needed by the potential curve adjustment
            points_needed = target_grade - current_grade
            adjusted_points_needed = points_needed - potential_curve # Apply curve adjustment here
            
            if remaining_weight > 0: 
                # Calculate required average based on adjusted points needed
                required_average_on_remaining = adjusted_points_needed / remaining_weight
                
                st.subheader("Prediction Results") 
                # Modify text to mention the curve adjustment if it's non-zero
                curve_text = f" (considering a {potential_curve:.2f} point potential curve adjustment)" if potential_curve > 0 else ""
                st.write(f"To reach your target grade of **{target_grade:.2f}%**{curve_text}, you need an average score of:")
                st.metric(label="Average on Remaining Assignments", value=f"{required_average_on_remaining:.2f}%")

                remaining_assignments = []
                for name, (score, has_grade) in component_inputs.items():
                     if not has_grade and name != midterm_to_drop:
                         remaining_assignments.append(f"{name.replace('mid','Midterm ').capitalize()} ({weights[name]*100:.0f}%)")
                
                if remaining_assignments:
                    st.write(f"*Remaining assignments contributing {remaining_weight*100:.0f}% to the total grade:*")
                    st.write(f"  - {', '.join(remaining_assignments)}")

                # Update warning/success logic based on the adjusted required average
                if required_average_on_remaining > 100:
                    st.warning(f"⚠️ Even with the potential curve adjustment, achieving an average of {required_average_on_remaining:.2f}% on the remaining assignments is impossible (max is 100%). You may need to adjust your target or curve assumption.")
                elif required_average_on_remaining < 0:
                     st.success(f"🎉 With the potential curve adjustment considered, you've already met or exceeded your target grade of {target_grade:.2f}%!")
                else:
                     st.info(f"This adjusted average score of {required_average_on_remaining:.2f}% across the remaining assignments is needed to reach your goal{curve_text}.")

            else: # points_needed <= 0 
                 # Check if target met even *without* curve adjustment for a clearer message
                 if (target_grade - current_grade) <= 0:
                    st.success(f"🎉 You've already met or exceeded your target grade of {target_grade:.2f}% based on current entries (before any potential curve)! ")
                 else: # Target met only *because* of the curve adjustment
                    st.success(f"🎉 With the potential curve adjustment of {potential_curve:.2f} points, you meet or exceed your target grade of {target_grade:.2f}%!")
        
        elif total_weight >= max_possible_weight : # All relevant grades entered
            st.info("You have entered all grades required for the final calculation (considering dropped midterm if applicable).")
            # Calculate final grade considering potential curve
            final_grade_with_curve = current_grade + potential_curve
            final_grade_percentage = (final_grade_with_curve / total_weight) if total_weight > 0 else 0 
            st.metric(label="Final Calculated Grade (with potential curve)", value=f"{final_grade_percentage:.2f}%")
            if final_grade_percentage >= target_grade:
                 st.success(f"Your final grade (with potential curve) meets or exceeds your target of {target_grade:.2f}%!")
            else:
                 st.warning(f"Your final grade (with potential curve) is below your target of {target_grade:.2f}%.")

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