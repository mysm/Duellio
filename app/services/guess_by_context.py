import logging

import requests
from zipfile import ZipFile
from pathlib import Path

from navec import Navec
from tqdm import tqdm
from gensim.models import KeyedVectors

logging.basicConfig(level=logging.INFO)


async def guess_similar_words(word: str, topn: int = 5) -> list:
    positive = word.split(" ")
    model = get_model()
    try:
        result = [
            similar_word
            for i, (similar_word, _) in enumerate(
                model.most_similar(positive=positive, topn=topn), 1
            )
        ]
    except KeyError:
        result = []
    return result


def get_model():

    model_dir = Path(".")
    model_dir.mkdir(parents=True, exist_ok=True)

    noun_only_model_txt = model_dir / "noun_model.txt"

    if noun_only_model_txt.exists() is False:
        logging.info("Downloading model...")
        # Download model
        # http://vectors.nlpl.eu/repository/20/180.zip - 116
        # http://vectors.nlpl.eu/repository/20/182.zip -
        zip_path = model_dir / "182.zip"
        response = requests.get(
            "http://vectors.nlpl.eu/repository/20/182.zip", stream=True
        )
        with zip_path.open("wb") as f:
            for data in tqdm(
                response.iter_content(chunk_size=4 * 1024 * 1024), total=153
            ):
                f.write(data)

        logging.info("Unzipping...")
        with ZipFile(zip_path) as archive:
            archive.extractall(model_dir)

        navec_model_tar = model_dir / "navec_hudlit_v1_12B_500K_300d_100q.tar"
        response = requests.get(
            "https://storage.yandexcloud.net/natasha-navec/packs/navec_hudlit_v1_12B_500K_300d_100q.tar",
            stream=True,
        )
        with navec_model_tar.open("wb") as f:
            for data in tqdm(
                response.iter_content(chunk_size=4 * 1024 * 1024), total=13
            ):
                f.write(data)

        navec = Navec.load(navec_model_tar)

        original_model_txt = model_dir / "model.txt"

        logging.info("Extracting nouns...")
        nouns = []
        # mystem = pymystem3.Mystem()
        with original_model_txt.open("r", encoding="utf-8") as f:
            for line in tqdm(f, total=185925):
                if "_NOUN" not in line or "::" in line:
                    continue

                clear_line = line.replace("_NOUN", "")
                clear_word = line.split("_")[0].strip()

                if "-" in clear_word:
                    continue

                if clear_word not in navec:
                    print(f"Strange word: {clear_word}")
                    continue

                nouns.append(clear_line)

        with noun_only_model_txt.open("w", encoding="utf-8") as f:
            f.write(f"{len(nouns)} 300\n")
            for line in nouns:
                f.write(line)
    else:
        logging.info("Model found!")

    logging.info("Loading model...")
    model = KeyedVectors.load_word2vec_format(
        noun_only_model_txt.name, binary=False
    )
    return model


if __name__ == "__main__":
    print(guess_similar_words("король женщина", 3))
    print(guess_similar_words("печь", 3))
