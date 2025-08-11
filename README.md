# Ben's Forensic CLI Toolkit
##  This is my toolkit. There are many like it, but this one is mine.

**Disclaimer**: This became a bit too big and complex for me at this point, will continue it later.

For learning purposes: This project is a work-in-progress forensic **CLI-only** toolkit.
I decided to try to build this to dive deeper into python and digital forensics.

---

## Browser Artifact Analysis

Extracts:

* Bookmarks
* Cookies
* History
* Form History

Results are saved as ```.csv```

**Currently supported:**

* 🦊 Firefox - Full support
* 🌐 Edge - Only history extraction
* 🛑 Chrome - Not implemented yet

**Whats missing:**

* Comments not completely added
* Edge and Chrome Support

### How it works
Copy the relevant **browser database files**, into the ```browser_files``` folder.
For **Browser Artifact Analysis** copy:
* places.sqlite
* cookies.sqlite
* History
* Cookies
* etc 

Run the **main.py**, choose **Browser Artifact Analysis** and go from there.

## File Metadata Analysis
Not yet implemented

## System Artifact Analysis
Not yet implemented

## Memory Analysis