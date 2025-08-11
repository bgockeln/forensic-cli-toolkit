import os
import zipfile
#import rarfile
#import py7zr
import csv
from datetime import datetime


#def analyze_archives(files):
#    print("Found Archives:", files)
#print("Loaded analyze_images.py")
def analyze_archives(files):
    print("Found Archives:", files)
    results = []

    # Get current script directory 
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level and into metadata_files
    metadata_dir = os.path.abspath(os.path.join(script_dir, "..", "..", "metadata_files"))

    for file in files:
        full_path = os.path.join(metadata_dir, file)
        metadata = analyze_archive(full_path)
        if metadata: # only add if not None
            results.append(metadata)
    return results
    
print("Loaded analyze_archives.py")

# Archive Type Check
def analyze_archive(filepath):
    """Analyze a single archive and return metadata."""
    archive_type = None
    if filepath.endswith(".zip"):
        archive_type = "zip"
    elif filepath.endswith(".rar"):
        archive_type = "rar"
    elif filepath.endswith(".7z"):
        archive_type = "7z"

    if archive_type is None:
        print(f"Unsupported archive type for file: {filepath}")
        return None
    
    # Metadata Container
    result = {
        "archive_name": os.path.basename(filepath),
        "archive_type": archive_type,
        "num_files": 0,
        "total_uncompressed_size": 0,
        "compression_ratio": None,
        "earliest_file_date": None,
        "latest_file_date": None,
        "password_protected": False,
        "comment": None
    }

    if archive_type == "zip":
        try:
            with zipfile.ZipFile(filepath, "r") as z:
                result["num_files"] = len(z.infolist())
                total_compressed = 0
                total_uncompressed = 0
                earliest = None
                latest = None
                comment = z.comment.decode("utf-8") if z.comment else None
                for info in z.infolist():
                    total_compressed += info.compress_size
                    total_uncompressed += info.file_size

                    # Convert date_time tuple to datetime object
                    file_date = datetime(*info.date_time)
                    if earliest is None or file_date < earliest:
                        earliest = file_date
                    if latest is None or file_date > latest:
                        latest = file_date

                    # Check if file is encrypted
                    if info.flag_bits & 0x1:
                        result["password_protected"] = True

                result["total_uncompressed_size"] = total_uncompressed
                if total_uncompressed > 0:
                    result["compression_ratio"] = round(total_compressed / total_uncompressed, 3)
                result["earliest_file_date"] = earliest.isoformat() if earliest else None
                result["latest_file_date"] = latest.isoformat() if latest else None
                result["comment"] = comment
        except zipfile.BadZipFile:
            print(f"Error: {filepath} is not a valid zip file")

# Save results to a CSV.
def save_result_to_csv(metadata_list, output_file):
    """Save Metadata To CSV."""
    fieldnames = [
        "archive_name",
        "archive_type",
        "num_files",
        "total_uncompressed_size",
        "compression_ratio",
        "earliest_file_date",
        "latest_file_date",
        "password_protected",
        "comment",
        "analyzed_at"
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for metadata in metadata_list:
            if "analyzed_at" not in metadata:
                metadata["analyzed_at"] = datetime.now().isoformat()
            writer.writerow(metadata)
