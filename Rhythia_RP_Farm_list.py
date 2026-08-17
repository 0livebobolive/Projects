import requests
import time
import csv

url = "https://production.rhythia.com/api/getBeatmapPage"

data = {
    "session": "",
    "id": 12744,
    "limit": 200
}

response = requests.post(url, json=data)

print(response.status_code)

map_data = response.json()

print(map_data.keys())

beatmap = map_data["beatmap"]

title = beatmap["title"]
stars = beatmap["starRating"]
length_ms = beatmap["length"]

length_seconds = length_ms / 1000

minutes = int(length_seconds // 60)
seconds = int(length_seconds % 60)

plays = beatmap["playcount"]
status = beatmap["status"]

print("Title:", title)
print("Stars:", stars)
print("Length:", f"{minutes}:{seconds:02d}")
print("Plays:", plays)
print("Status:", status)

scores = map_data["scores"]

print("Scores received:", len(scores))
print("First score:", scores[0])

one_x_scores = []

for score in scores:
    correct_speed = abs(score["speed"] - 1.0) < 0.001
    no_mods = score["mods"] == []
    passed = score["passed"] is True
    no_spin = score["spin"] is False

    if correct_speed and no_mods and passed and no_spin:
        one_x_scores.append(score)

print("Clean 1x scores found:", len(one_x_scores))

for score in one_x_scores:
    print(
        "RP:", score["awarded_sp"],
        "Accuracy:", score["accuracy"],
        "Speed:", score["speed"]
    )

if one_x_scores:
    best_score = max(
        one_x_scores,
        key=lambda score: score["awarded_sp"]
    )

    best_rp = best_score["awarded_sp"]
    best_accuracy = best_score["accuracy"]

    rp_per_minute = best_rp / (length_seconds / 60)

    print("Best observed 1x RP:", best_rp)
    print("Accuracy:", best_accuracy)
    print("Observed RP per minute:", round(rp_per_minute, 2))
else:
    print("No clean 1x scores found")

filters = {
    "session": "",
    "page": 1,
    "minStars": 6,
    "status": "RANKED"
}

maps_url = "https://production.rhythia.com/api/getBeatmaps"

filters = {
    "session": "",
    "page": 1,
    "minStars": 6,
    "status": "RANKED"
}

maps_response = requests.post(maps_url, json=filters)
maps_data = maps_response.json()

print("Total maps found:", maps_data["total"])
print("Maps on this page:", len(maps_data["beatmaps"]))

first_map = maps_data["beatmaps"][0]

print("First map ID:", first_map["id"])
print("First map title:", first_map["title"])
print("First map stars:", first_map["starRating"])

maps_per_page = maps_data["viewPerPage"]
total_maps = maps_data["total"]

total_pages = (total_maps + maps_per_page - 1) // maps_per_page

print("Total pages:", total_pages)

all_maps = []

for page_number in range(1, total_pages + 1):
    filters["page"] = page_number

    page_response = requests.post(maps_url, json=filters)
    page_data = page_response.json()

    all_maps.extend(page_data["beatmaps"])

    print(
        "Collected page:",
        page_number,
        "Total collected:",
        len(all_maps)
    )

    time.sleep(0.5)

print("Finished collecting:", len(all_maps), "maps")
for map_summary in all_maps:

    details_url = "https://production.rhythia.com/api/getBeatmapPage"

results = []
for map_summary in all_maps:
    map_id = map_summary["id"]

    details_request = {
        "session": "",
        "id": map_id,
        "limit": 200
    }

    details_response = requests.post(details_url, json=details_request)
    details_data = details_response.json()

    beatmap = details_data["beatmap"]
    scores = details_data["scores"]

    clean_scores = []

    for score in scores:
        correct_speed = abs(score["speed"] - 1.0) < 0.001
        no_mods = score["mods"] == []
        passed = score["passed"] is True
        no_spin = score["spin"] is False

        if correct_speed and no_mods and passed and no_spin:
            clean_scores.append(score)

    length_seconds = beatmap["length"] / 1000

    if clean_scores:
        best_score = max(
            clean_scores,
            key=lambda score: score["awarded_sp"]
        )

        best_rp = best_score["awarded_sp"]
        best_accuracy = best_score["accuracy"]

        length_seconds = beatmap["length"] / 1000
        rp_per_minute = best_rp / (length_seconds / 60)
    else:
        best_rp = None
        best_accuracy = None
        rp_per_minute = None

    result = {
        "id": map_id,
        "title": beatmap["title"],
        "stars": beatmap["starRating"],
        "length_seconds": length_seconds,
        "best_rp_1x": best_rp,
        "best_accuracy_1x": best_accuracy,
        "rp_per_minute": rp_per_minute
    }

    results.append(result)

    print(result)

    time.sleep(0.5)