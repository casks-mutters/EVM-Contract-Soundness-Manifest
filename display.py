def print_banner(title: str):
    print("=" * len(title))
    print(title)
    print("=" * len(title))

def print_comparison(actual: str, expected: str):
    print("Computed root:", actual)
    if expected:
        print("Expected root:", expected)
        if actual.lower() == expected.lower():
            print("✅ Match")
        else:
            print("❌ Mismatch")
