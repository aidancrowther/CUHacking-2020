from google_images_download import google_images_download
import multiprocessing 

response = google_images_download.googleimagesdownload()
keywords = [
    '-eggs',
    '+butterfly',
    '-table',
    '-screen-shot'
]

f = open('species.txt', 'r')
species = f.read().split("\n")

for i in range(len(species)):
    species[i] = species[i].split(' ')
    for keyword in keywords:
        species[i].append(keyword)

    species[i] = ' '.join(species[i])

keys = []
processes = []


for each in species:
    response.download({
        "keywords": each,
        "limit": 500,
        "print_urls": True,
        "chromedriver": "chromedriver",
        "output_directory": "Dataset"
    })