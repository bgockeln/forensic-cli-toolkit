import os
from file_metadata_scanning.scripts.analyze_images import analyze_images
from file_metadata_scanning.scripts.analyze_videos import analyze_videos
from file_metadata_scanning.scripts.analyze_audio import analyze_audio
from file_metadata_scanning.scripts.analyze_documents import analyze_documents
from file_metadata_scanning.scripts.analyze_pdf import analyze_pdf
from file_metadata_scanning.scripts.analyze_archives import analyze_archives

print("starting main.py")
filetype_mapping = {
    "jpg": "images",
    "jpeg": "images",
    "png": "images",
    "gif": "images",
    "bmp": "images",
    "mp4": "videos",
    "avi": "videos",
    "mov": "videos",
    "mkv": "videos",
    "mp3": "audio",
    "wav": "audio",
    "aac": "audio",
    "flac": "audio",
    "docx": "documents",
    "doc": "documents",
    "xlsx": "documents",
    "xls": "documents",
    "odt": "documents",
    "ods": "documents",
    "odp": "documents",
    "pdf": "pdf",
    "zip": "archives",
    "rar": "archives",
    "7z": "archives"
}

def categorize_files(folder_path):
    files_by_category = {
        "archives": [],
        "audio": [],
        "documents": [],
        "images": [],
        "pdf": [],
        "videos": []
    }

    for filename in os.listdir(folder_path):
        if not os.path.isfile(os.path.join(folder_path, filename)):
            continue
        ext = filename.lower().split(".")[-1]
        if ext in filetype_mapping:
            category = filetype_mapping[ext]
            files_by_category[category].append(filename)

    return files_by_category

def print_summary(file_dict):
    print(" Detected file in categories:\n")
    for category, files in file_dict.items():
        if files:
            print(f" - {len(files)} {category} file(s)")

def main():
    folder_path = os.path.join(os.path.dirname(__file__), "..", "metadata_files")
    files_by_category = categorize_files(folder_path)

    print_summary(files_by_category)
    print("\nBen's File Metadata Analyzer")

    if "archives" in files_by_category:
        analyze_archives(files_by_category["archives"])
    if "audio" in files_by_category:
        analyze_audio(files_by_category["audio"])
    if "documents" in files_by_category:
        analyze_documents(files_by_category["documents"])
    if "pdf" in files_by_category:
        analyze_pdf(files_by_category["pdf"])
    if "images" in files_by_category:
        analyze_images(files_by_category["images"])
    if "videos" in files_by_category:
        analyze_videos(files_by_category["videos"])


if __name__ == "__main__":
    main()