import requests
import logging
import os
import pandas as pd
import time
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine

logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)

logger = logging.getLogger(__name__)

load_dotenv()

REQUEST_SLEEP = (1 / 10) * 4  # Max: 10requests per seconds


class SECPipeline:
    BASE_API = "https://data.sec.gov/api/xbrl/companyconcept"

    def __init__(self, cik):
        self.company_cik = cik
        self.engine = create_engine(
            "postgresql://%s:%s@%s:%s/%s"
            % (
                os.environ["DB_USER"],
                os.environ["DB_PASS"],
                os.environ["DB_HOST"],
                os.environ["DB_PORT"],
                os.environ["DB_NAME"],
            )
        )
        self.request_url = (
            f"{self.BASE_API}/{str(cik)}/us-gaap/AccountsPayableCurrent.json"
        )
        self.response = None
        self.df = None

    def fetch(
        self,
    ):
        header = {
            "User-Agent": os.environ["USER_AGENT"],
            "Accept-Encoding": "gzip, deflate",
        }
        logger.info(
            "Fetching SEC - AccountsPayableCurrent data for %s", self.company_cik
        )
        try:
            response = requests.get(self.request_url, headers=header)
            response.raise_for_status()
            self.response = response.json()
        except requests.RequestException as err:
            logging.error("message %s", err)
        return self

    def transform(self):
        return self

    def load(self):
        return self


if __name__ == "__main__":
    company_list = [
        "0000320193",
        "0001045810",
        "0000789019",
        "0001018724",
        "0001652044",
        "0001318605",
        "0000104169",
    ]

    for company in company_list:
        cik_val = f"CIK{company}"
        try:
            (SECPipeline(cik_val).fetch().transform().load())
      
        except Exception as err:
            logger.error("Failed to load for company with CIK: %s", cik_val, err)

        time.sleep(REQUEST_SLEEP)
