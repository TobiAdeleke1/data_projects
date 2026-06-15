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
        if not self.response:
            logger.error("No API response: was fetch() called ?")
            return self
        
        logger.info("Parsing SEC response for %s", self.company_cik)
        unit =  str(list(self.response["units"].keys())[0])
        cik = self.response["cik"]
        tag = self.response["tag"]
        entityname = self.response["entityName"]
        all_unit_vals = self.response["units"][unit]
        row_list = [
            {
                **unit_vals,
                "cik": cik,
                "entityname": entityname,
                "unit": unit,
                "tag": tag,
                "end_date": unit_vals["end"],
                "value": unit_vals["val"],
                "accession_number": unit_vals["accn"],
                "fiscal_year": unit_vals["fy"],
                "fiscal_period": unit_vals["fp"],
                "form": unit_vals["form"],
                "filed": unit_vals["filed"],
                "frame": unit_vals.get("frame"),
                "fetched_at": datetime.now(),
            }
            for unit_vals in all_unit_vals
        ]
        self.df = pd.DataFrame(row_list)
        self.df["end_date"] = pd.to_datetime(self.df["end_date"])
        self.df["filed"] = pd.to_datetime(self.df["filed"])
        logger.info("Transformed %s records", len(self.df))
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
