import sys
from browser_artifact_scanning import main as artifact_main

def exit_script():
    print("Exiting...")
    sys.exit(0)

def main():
    menu_actions = {
        "1": artifact_main.main, 
        "2": print("2"), #lambda: analyze_cookies(browser_files),
        "3": print("3"), #lambda: analyze_form_history(browser_files),
        "4": print("4"), #lambda: analyze_history(browser_files),
        "5": exit_script
    }

    while True:
        print("\nBen's Forensic CLI Toolkit")
        print("1. Browser Artifact Analysis")
        print("2. File Metadata Analysis")
        print("3. System Artifact Analysis")
        print("4. Memory Analysis")
        print("5. Exit")
        choice = input("Enter choice: ").strip()

        action = menu_actions.get(choice)
        if action:
            action()
        else:
            print("Invalid Choice, try again.")

if __name__ == "__main__":
    main()