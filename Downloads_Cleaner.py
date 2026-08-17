from pathlib import Path

downloads = Path.home() / "Downloads"
rhythia_maps = downloads / "Rhythia Maps"
images = downloads / "Images"
audio_files = downloads / "Audio"
videos = downloads / "Video"
documents = downloads / "Documents"
zip_files = downloads / "Zip Files"
installers = downloads / "Installers"
coding_files = downloads / "Coding"
shortcuts = downloads / "Shortcuts"

images.mkdir(exist_ok=True)
rhythia_maps.mkdir(exist_ok=True)
audio_files.mkdir(exist_ok=True)
videos.mkdir(exist_ok=True)
documents.mkdir(exist_ok=True)
zip_files.mkdir(exist_ok=True)
installers.mkdir(exist_ok=True)
coding_files.mkdir(exist_ok=True)
shortcuts.mkdir(exist_ok=True)

image_extensions = [".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"]
audio_extensions = [".mp3", ".wav", ".flac", ".m4a", ".ogg"]
video_extensions = [".mp4", ".mov", ".mkv", ".avi", ".webm"]
document_extensions = [
    ".pdf", ".txt", ".doc", ".docx",
    ".ppt", ".pptx", ".xls", ".xlsx", ".csv"
]
archive_extensions = [".zip", ".rar", ".7z", ".tar", ".gz"]
installer_extensions = [".exe", ".msi", ".msix"]
code_extensions = [
    ".py", ".js", ".html", ".css",
    ".java", ".cpp", ".c", ".json"
]
shortcut_extensions = [".lnk", ".url"]
map_extensions = [".sspm", ".rhm", ".rhs", ".sspre"]


for item in downloads.iterdir():
    if item.is_file():
        extension = item.suffix.lower()

        if extension in image_extensions:
            folder = images
        elif extension in audio_extensions:
            folder = audio_files
        elif extension in video_extensions:
            folder = videos
        elif extension in document_extensions:
            folder = documents
        elif extension in archive_extensions:
            folder = zip_files
        elif extension in installer_extensions:
            folder = installers
        elif extension in code_extensions:
            folder = coding_files
        elif extension in shortcut_extensions:
            folder = shortcuts
        elif extension in map_extensions:
            folder = rhythia_maps
        else:
            print("Unrecognized, skipped:", item.name)
            continue
        
        destination = folder / item.name

        if destination.exists():
            print("Already exists, skipped:", item.name)
        else:
            item.rename(destination)
            print("Moved:", item.name, "to", folder.name)