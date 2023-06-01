import pandas as pd
import re
from flair.data import Sentence
from flair.models import SequenceTagger

model = SequenceTagger.load("flair/ner-french")

def anonymize_text(text, model):
    sentence = Sentence(text)
    model.predict(sentence)

    anonymized_sentence = sentence.to_plain_string()
    for entity in sentence.get_spans('ner'):
        anonymized_sentence = anonymized_sentence.replace(str(entity.text), "****")

    anonymized_sentence = re.sub(r'\S+@\S+', '*****', anonymized_sentence)
    anonymized_sentence = re.sub(r'\+\d{2}\(\d{0}\) \d{3} \d{3} \d{3}', '*****', anonymized_sentence)
    anonymized_sentence = re.sub(r'MLK\d+', '*****', anonymized_sentence)
    anonymized_sentence = re.sub(r'FR\d+ \d{4} \d{4} \d{4} \d{4} \d{4} \d{2}', '*****', anonymized_sentence)
    anonymized_sentence = re.sub(r'\S*\d\S*', '*****', anonymized_sentence)

    return anonymized_sentence


def anonymize_reviews(csv_path, model):
    df = pd.read_csv(csv_path , encoding='utf-8-sig', delimiter=';', header=0 )
    df['Anonymized_Review'] = df['Review'].apply(lambda x: anonymize_text(x, model))
    output_file = 'anonymized_reviews.csv'
    df.to_csv(output_file, index=False)
    return output_file

model = SequenceTagger.load("flair/ner-french")

# Anonymize reviews
output_file = anonymize_reviews("test_rgpd.csv", model)
print(f"Anonymized reviews saved in {output_file}")