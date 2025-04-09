def calculate_grade(components):
    """
    Calculate the grade based on received components.
    components is a dictionary with keys: homework, discussion, mid1, mid2, mid3, final
    Each value is a tuple of (score, has_grade)
    """
    current_grade = 0
    total_weight = 0
    
    weights = {
        'homework': 0.05,
        'discussion': 0.10,
        'mid1': 0.20,
        'mid2': 0.20,
        'mid3': 0.20,
        'final': 0.25
    }
    
    for component, (score, has_grade) in components.items():
        if has_grade:
            current_grade += score * weights[component]
            total_weight += weights[component]
    
    if total_weight > 0:
        current_percentage = current_grade / total_weight
    else:
        current_percentage = 0
    
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
    print(f"Grade: {grade:.2f}% (should be 100%)")
    print(f"Weight: {weight:.2f} (should be 1.0)")
    print(f"Percentage: {percentage:.2f}% (should be 100%)")
    print()
    
    # Test Case 2: Only first two midterms
    test2 = {
        'homework': (100, True),
        'discussion': (100, True),
        'mid1': (80, True),
        'mid2': (80, True),
        'mid3': (0, False),
        'final': (0, False)
    }
    grade, weight, percentage = calculate_grade(test2)
    print(f"Test 2 - First two midterms only:")
    print(f"Grade: {grade:.2f}% (should be 47%)")
    print(f"Weight: {weight:.2f} (should be 0.55)")
    print(f"Percentage: {percentage:.2f}% (should be 85.45%)")
    print()
    
    # Test Case 3: Mixed grades
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
    print(f"Grade: {grade:.2f}% (should be 44%)")
    print(f"Weight: {weight:.2f} (should be 0.55)")
    print(f"Percentage: {percentage:.2f}% (should be 80%)")
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
    print(f"Grade: {grade:.2f}% (should be 0%)")
    print(f"Weight: {weight:.2f} (should be 0)")
    print(f"Percentage: {percentage:.2f}% (should be 0%)")
    print()

if __name__ == "__main__":
    test_cases() 