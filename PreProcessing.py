import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

class PreProcess :
    
    LEMMITIZER = WordNetLemmatizer()

    @classmethod
    def clean(cls,data_frame : pd.DataFrame) -> pd.DataFrame:
        print(data_frame.duplicated().sum())
        # Remove exact duplicates
        data_frame = data_frame.drop_duplicates()
        data_frame = data_frame.dropna(subset=["currentEnergyEfficiencyBand"])

        return data_frame
    
    # Feature engineering - using nltk
    @classmethod
    def make_full_address(cls,data_frame : pd.DataFrame) -> pd.DataFrame:
        # Sort by date - to make sure the certificates that are most up to date are used.

        data_frame["registrationDate"] = pd.to_datetime(data_frame["registrationDate"])
        data_frame.sort_values(by="registrationDate")

        cols = ["addressLine1", "addressLine2", "addressLine3", "addressLine4"]

        data_frame["FullAddress"] = (
            data_frame[cols]
            .fillna("")
            .agg("\n ".join, axis=1)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )

        return data_frame
    @classmethod
    def drop_address_duplicates(cls,data_frame : pd.DataFrame) -> pd.DataFrame:
        # 74 for postcode, 153 for full address
        data_frame = data_frame.drop_duplicates(subset=['FullAddress'], keep='first')

        return data_frame
    @classmethod
    def format_words(cls, text :str) -> list[str]:
        # Lowercase conversion
        text = text.lower()

        # Remove special characters
        cleaned_text = re.sub(r'[^a-zA-Z\s]', '', text)

        # Tokenize the text
        tokens = word_tokenize(cleaned_text)

        stop_words = set(stopwords.words('english'))
        formatted_words = [cls.LEMMITIZER.lemmatize(word) for word in tokens if word.lower() not in stop_words]

        return formatted_words

    # Remove dupes based on postcode - removes buildings that might not necessarily be dupes but buildings under the same post
    # Another edge case could be PO Boxes are used instead
    @classmethod
    def postcode_duplicates(cls, data_frame : pd.DataFrame) -> pd.DataFrame:
        data_frame = data_frame.drop_duplicates(subset=['postcode'], keep='first')
        return data_frame