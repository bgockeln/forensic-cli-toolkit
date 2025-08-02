import sys
import os
from .history import firefox
from .form_history import firefox
from .bookmarks import firefox
from .cookies import firefox

# Detect the Browsertype by checking what browser profil files are in the bro
def detect_browser_files(folder_path):

    files = os.listdir(folder_path)
    browser_files = {}

    if "places.sqlite" in files or "formhistory.sqlite" in files or "cookies.sqlite" in files:
        browser_files["firefox"] = {
            "history": os.path.join(folder_path, "places.sqlite") if "places.sqlite" in files else None,
            "formhistory": os.path.join(folder_path, "formhistory.sqlite") if "formhistory.sqlite" in files else None,
            "cookies": os.path.join(folder_path, "cookies.sqlite") if "cookies.sqlite" in files else None,
            "bookmarks": os.path.join(folder_path, "places.sqlite") if "places.sqlite" in files else None
        }

    if "History" in files:
        browser_files["chrome"] = {
            "historyy": os.path.join(folder_path, "Historyy")
        }

    if "History" in files or "Bookmarks" in files or "Cookies" in files or "Web Data" in files:
        browser_files["edge"] = {
            "history": os.path.join(folder_path, "History") if "History" in files else None,
            "formhistory": os.path.join(folder_path, "Web Data") if "Web Data" in files else None,
            "cookies": os.path.join(folder_path, "Cookies") if "Cookies" in files else None,
            "bookmarks": os.path.join(folder_path, "Bookmarks") if "Bookmarks" in files else None
        }

    return browser_files

def analyze_bookmarks(browser_files):
    print("\nRunning bookmark analysis") 
    if "firefox" in browser_files and browser_files["firefox"].get("bookmarks"):
        from browser_artifact_scanning.bookmarks import firefox
        firefox.analyze_bookmarks(browser_files["firefox"]["bookmarks"])
    else:
        print("places.sqlite file not found") 

def analyze_cookies(browser_files):
    print("\nRunning cookies analysis") 
    if "firefox" in browser_files and browser_files["firefox"].get("cookies"):
        from browser_artifact_scanning.cookies import firefox
        firefox.analyze_cookies(browser_files["firefox"]["cookies"])
    else:
        print("cookies.sqlite file not found") 

def analyze_form_history(browser_files):
    print("\nRunning form history analysis") 
    if "firefox" in browser_files and browser_files["firefox"].get("formhistory"):
        from browser_artifact_scanning.form_history import firefox
        firefox.analyze_form_history(browser_files["firefox"]["formhistory"])
    else:
        print("formhistory.sqlite file not found")

def analyze_history(browser_files):
    print("\nRunning history analysis") 
    if "firefox" in browser_files and browser_files["firefox"].get("history"):
        from browser_artifact_scanning.history import firefox
        firefox.analyze_history(browser_files["firefox"]["history"])
    elif "edge" in browser_files and browser_files["edge"].get("history"):
        from browser_artifact_scanning.history import edge
        edge.analyze_history(browser_files["edge"]["history"])
    elif "chrome" in browser_files and browser_files["chrome"].get("history"):
        print("not there yet")
    else: 
        print("No supported files found")

def exit_script():
    print("Exiting...")
    sys.exit(0)

def main():
    folder_path = os.path.join(os.path.dirname(__file__), "..", "browser_files")
    browser_files = detect_browser_files(folder_path)

    if not browser_files:
        print("no known browser data found.")
        return

    menu_actions = {
            "1": lambda: analyze_bookmarks(browser_files),
            "2": lambda: analyze_cookies(browser_files),
            "3": lambda: analyze_form_history(browser_files),
            "4": lambda: analyze_history(browser_files),
            "5": exit_script
    }

    while True:
        print("\nBen's Browser Artifact Analyzer")
        print("1. Analyze Bookmarks")
        print("2. Analyze Cookies")
        print("3. Analyze Form History")
        print("4. Analyze History")
        print("5. Exit")
        choice = input("Enter choice: ").strip()

        action = menu_actions.get(choice)
        if action:
            action()
        else:
            print("Invalid Choice, try again.")

if __name__ == "__main__":
    main()

