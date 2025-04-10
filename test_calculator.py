def calculate_grade(components, drop_midterm1_if_lower=False):
    """
    Calculate the grade based on received components.
    components is a dictionary with keys: homework, discussion, mid1, mid2, mid3, final
    Each value is a tuple of (score, has_grade)
    If drop_midterm1_if_lower is True, it drops Midterm 1 if all midterms are present
    and Midterm 1 score < Midterm 2 score.
    """
    current_grade = 0
    total_weight = 0
    midterm_scores = {}
    midterm_to_drop = None
    
    weights = {
        'homework': 0.05,
        'discussion': 0.10,
        'mid1': 0.20,
        'mid2': 0.20,
        'mid3': 0.20,
        'final': 0.25
    }
    
    # Initial pass to calculate grade and weight, and collect midterm scores
    for component, (score, has_grade) in components.items():
        if has_grade:
            current_grade += score * weights[component]
            total_weight += weights[component]
            if component in ['mid1', 'mid2', 'mid3']:
                midterm_scores[component] = score
    
    # Check conditions for dropping Midterm 1
    all_midterms_entered = all(components[m][1] for m in ['mid1', 'mid2', 'mid3'])
    
    if drop_midterm1_if_lower and all_midterms_entered:
        if midterm_scores['mid1'] < midterm_scores['mid2']:
            midterm1_score = midterm_scores['mid1']
            # Adjust grade and weight
            current_grade -= midterm1_score * weights['mid1']
            total_weight -= weights['mid1']
            midterm_to_drop = 'mid1'
            print("  (Info: Midterm 1 dropped)") # Add info for test output
        else:
            print("  (Info: Midterm 1 not dropped - condition not met)") # Add info for test output
            
    # Calculate final percentage based on potentially adjusted grade/weight
    if total_weight > 0:
        current_percentage = current_grade / total_weight
    else:
        current_percentage = 0
    
    # Return total points, effective weight, and the calculated percentage average
    return current_grade, total_weight, current_percentage 

def test_cases():
    # Test Case 1: All perfect scores
    test1 = {
        'homework': (100, True),
        'discussion': (100, True),
        'mid1': (100, True),
        'mid2': (100, True),
        'mid3': (100, True),
        'final': (100, True)
    }
    grade, weight, percentage = calculate_grade(test1)
    print(f"Test 1 - All perfect scores:")
    print(f"Grade Points: {grade:.2f} (should be 100.00)")
    print(f"Weight: {weight:.2f} (should be 1.00)")
    print(f"Percentage: {percentage:.2f}% (should be 100.00%)")
    print()
    
    # Test Case 2: Only first two midterms (and HW/Disc)
    test2 = {
        'homework': (100, True),
        'discussion': (100, True),
        'mid1': (80, True),
        'mid2': (80, True),
        'mid3': (0, False),
        'final': (0, False)
    }
    grade, weight, percentage = calculate_grade(test2)
    print(f"Test 2 - HW, Disc, Mid1, Mid2 only:")
    print(f"Grade Points: {grade:.2f} (should be 47.00)")
    print(f"Weight: {weight:.2f} (should be 0.55)")
    print(f"Percentage: {percentage:.2f}% (should be 85.45%)")
    print()
    
    # Test Case 3: Mixed grades, some missing
    test3 = {
        'homework': (90, True),
        'discussion': (85, True),
        'mid1': (75, True),
        'mid2': (80, True),
        'mid3': (0, False),
        'final': (0, False)
    }
    grade, weight, percentage = calculate_grade(test3)
    print(f"Test 3 - Mixed grades, some missing:")
    print(f"Grade Points: {grade:.2f} (should be 44.00)")
    print(f"Weight: {weight:.2f} (should be 0.55)")
    print(f"Percentage: {percentage:.2f}% (should be 80.00%)")
    print()
    
    # Test Case 4: No grades entered
    test4 = {
        'homework': (0, False),
        'discussion': (0, False),
        'mid1': (0, False),
        'mid2': (0, False),
        'mid3': (0, False),
        'final': (0, False)
    }
    grade, weight, percentage = calculate_grade(test4)
    print(f"Test 4 - No grades entered:")
    print(f"Grade Points: {grade:.2f} (should be 0.00)")
    print(f"Weight: {weight:.2f} (should be 0.00)")
    print(f"Percentage: {percentage:.2f}% (should be 0.00%)")
    print()

    # Test Case 5: Drop Midterm 1 (M1 < M2)
    test5 = {
        'homework': (100, True),
        'discussion': (100, True),
        'mid1': (70, True), # Lower than M2
        'mid2': (80, True),
        'mid3': (90, True),
        'final': (95, True) 
    }
    # Expected calculation: HW(5) + Disc(10) + M2(16) + M3(18) + Final(23.75) = 72.75 points
    # Expected weight: HW(0.05) + Disc(0.10) + M2(0.20) + M3(0.20) + Final(0.25) = 0.80 weight
    # Expected percentage: 72.75 / 0.80 = 90.94%
    grade, weight, percentage = calculate_grade(test5, drop_midterm1_if_lower=True)
    print(f"Test 5 - Drop Midterm 1 (M1=70 < M2=80):")
    print(f"Grade Points: {grade:.2f} (should be 72.75)")
    print(f"Weight: {weight:.2f} (should be 0.80)")
    print(f"Percentage: {percentage:.2f}% (should be 90.94%)") 
    print()

    # Test Case 6: Attempt Drop Midterm 1 (M1 >= M2) - Should NOT drop
    test6 = {
        'homework': (100, True),
        'discussion': (100, True),
        'mid1': (85, True), # Higher than M2
        'mid2': (80, True),
        'mid3': (90, True),
        'final': (95, True) 
    }
    # Expected calculation (no drop): HW(5)+Disc(10)+M1(17)+M2(16)+M3(18)+Final(23.75) = 89.75
    # Expected weight: 1.00
    # Expected percentage: 89.75 / 1.00 = 89.75%
    grade, weight, percentage = calculate_grade(test6, drop_midterm1_if_lower=True)
    print(f"Test 6 - Attempt Drop Midterm 1 (M1=85 >= M2=80) - No Drop:")
    print(f"Grade Points: {grade:.2f} (should be 89.75)")
    print(f"Weight: {weight:.2f} (should be 1.00)")
    print(f"Percentage: {percentage:.2f}% (should be 89.75%)")
    print()

# --- New function to test prediction logic --- 
def calculate_required_average(components, target_grade, drop_midterm1_if_lower=False, curve_points=0):
    """Calculates the average score needed on remaining assignments."""
    # First, calculate current grade and weight using existing logic
    current_grade = 0
    total_weight = 0
    midterm_scores = {}
    midterm_to_drop = None
    
    weights = {
        'homework': 0.05, 'discussion': 0.10,
        'mid1': 0.20, 'mid2': 0.20, 'mid3': 0.20, 'final': 0.25
    }
    
    # Initial pass
    for component, (score, has_grade) in components.items():
        if has_grade:
            current_grade += score * weights[component]
            total_weight += weights[component]
            if component in ['mid1', 'mid2', 'mid3']:
                midterm_scores[component] = score
    
    # Apply drop logic
    all_midterms_entered = all(components[m][1] for m in ['mid1', 'mid2', 'mid3'])
    if drop_midterm1_if_lower and all_midterms_entered:
        if midterm_scores['mid1'] < midterm_scores['mid2']:
            current_grade -= midterm_scores['mid1'] * weights['mid1']
            total_weight -= weights['mid1']
            midterm_to_drop = 'mid1'

    # Calculate remaining weight and points needed
    max_possible_weight = 1.0 - (weights['mid1'] if midterm_to_drop else 0.0)
    remaining_weight = max_possible_weight - total_weight

    if remaining_weight <= 1e-6: # Use small tolerance for floating point comparison near zero
        return None # Or float('inf') if you prefer for "impossible" or already done

    points_needed = target_grade - current_grade
    adjusted_points_needed = points_needed - curve_points
    
    required_average = adjusted_points_needed / remaining_weight
    return required_average

# --- Test cases for the prediction logic --- 
def test_predictions():
    print("--- Testing Prediction Logic ---")
    # Scenario: Midterms 1 & 2 done (both 80), HW/Disc (both 100). Target 90.
    # Current grade = 47.0, weight = 0.55. Remaining weight = 0.45
    # Points needed = 90 - 47 = 43
    # Raw required avg = 43 / 0.45 = 95.56%
    components_partial = {
        'homework': (100, True), 'discussion': (100, True),
        'mid1': (80, True), 'mid2': (80, True),
        'mid3': (0, False), 'final': (0, False)
    }
    
    # Test Case 7: Curve makes target possible
    # Target 98. Raw required avg = (98 - 47) / 0.45 = 51 / 0.45 = 113.33%
    # With 5 curve points: Adj points needed = 51 - 5 = 46. Required avg = 46 / 0.45 = 102.22%
    # With 10 curve points: Adj points needed = 51 - 10 = 41. Required avg = 41 / 0.45 = 91.11%
    req_avg_raw = calculate_required_average(components_partial, 98, False, 0)
    req_avg_curve10 = calculate_required_average(components_partial, 98, False, 10)
    print(f"Test 7 - Curve makes target possible:")
    print(f"  Raw Req Avg (Target 98): {req_avg_raw:.2f}% (should be > 100%)")
    print(f"  Req Avg (Target 98, Curve 10): {req_avg_curve10:.2f}% (should be ~91.11%)")
    print()

    # Test Case 8: Curve reduces requirement
    # Target 90. Raw required avg = (90 - 47) / 0.45 = 43 / 0.45 = 95.56%
    # With 5 curve points: Adj points needed = 43 - 5 = 38. Required avg = 38 / 0.45 = 84.44%
    req_avg_raw = calculate_required_average(components_partial, 90, False, 0)
    req_avg_curve5 = calculate_required_average(components_partial, 90, False, 5)
    print(f"Test 8 - Curve reduces requirement:")
    print(f"  Raw Req Avg (Target 90): {req_avg_raw:.2f}% (should be ~95.56%)")
    print(f"  Req Avg (Target 90, Curve 5): {req_avg_curve5:.2f}% (should be ~84.44%)")
    print()

    # Test Case 9: Curve insufficient
    # Target 100. Raw required avg = (100 - 47) / 0.45 = 53 / 0.45 = 117.78%
    # With 5 curve points: Adj points needed = 53 - 5 = 48. Required avg = 48 / 0.45 = 106.67%
    req_avg_raw = calculate_required_average(components_partial, 100, False, 0)
    req_avg_curve5 = calculate_required_average(components_partial, 100, False, 5)
    print(f"Test 9 - Curve insufficient:")
    print(f"  Raw Req Avg (Target 100): {req_avg_raw:.2f}% (should be > 100%)")
    print(f"  Req Avg (Target 100, Curve 5): {req_avg_curve5:.2f}% (should be > 100%)")
    print()

    # Test Case 10: All grades entered (including dropped M1)
    # Use Test 5 components: HW(100), Disc(100), M1(70), M2(80), M3(90), Final(95)
    # Drop M1 (since 70<80). total_weight=0.80. max_weight=0.80. remaining=0
    components_all_drop = {
        'homework': (100, True), 'discussion': (100, True),
        'mid1': (70, True), 'mid2': (80, True), 'mid3': (90, True), 'final': (95, True) 
    }
    req_avg_all_in = calculate_required_average(components_all_drop, 90, True, 5)
    print(f"Test 10 - All grades entered (drop M1 active):")
    print(f"  Req Avg: {req_avg_all_in} (should be None, as remaining weight is 0)")
    print()

if __name__ == "__main__":
    test_cases() # Run original grade calculation tests
    test_predictions() # Run new prediction logic tests 