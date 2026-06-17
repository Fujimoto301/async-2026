from os import name
import sys
def evaluate_grade(score):
    if score >= 80:
        return "Excellent"
    elif score >= 50:
        return "Pass"
    else:
        return "Fail"


def main():
    test_scores = [90, 80, 79, 50, 45, 0]
    for test_score in test_scores:
        result = evaluate_grade(test_score)
        print(f"Score: {test_score} -> Grade: {result}")


if __name__ == "__main__":
    main()