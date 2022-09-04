import logging
import os
import re
import traceback
from argparse import ArgumentParser
from datetime import datetime

import networkx as nx
from networkx.algorithms.traversal.depth_first_search import dfs_tree
import pandas as pd


todays_date = datetime.strftime(datetime.now(), "%Y-%m-%d")
output_path = os.environ.get("OUTPUTPATH", "s3://my_adobe_assignment/output")
retailer_domain = os.environ.get("RETAILER_DOMAIN", "www.esshopzilla.com")
checkout_page = os.environ.get(
    "CHECKOUT_PAGE", "https://www.esshopzilla.com/checkout/?a=complete"
)

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))


class SearchKeywordPerformance:
    def __init__(self, input_path, output_path, retailer_domain, checkout_page):
        self.input_path = input_path
        self.output_file_qualified_path = (
            f"{output_path}{todays_date}_searchKeywordPerformance.tab"
        )
        self.retailer_domain = retailer_domain
        self.checkout_page = checkout_page

    def _parse_product_list(self, data):
        revenue = 0.00
        try:
            products = data.split(",")
            for each_product in products:
                product_attrs = each_product.split(";")
                revenue += float(product_attrs[3]) if product_attrs[3] else 0.00
        except AttributeError:
            pass
        return revenue

    def _parse_referrer(self, data):
        pattern = r"^http\S*//\w+.(\w+.\w+)/"
        matches = re.match(pattern, data.strip())
        return matches.group(1)

    def _parse_search_str(self, data):
        # google search string pattern
        pattern = r"q=(\w+)"
        matches = re.search(pattern, data.strip())
        if matches:
            pass
        else:
            # yahoo search string pattern
            pattern = r"p=(\w+)"
            matches = re.search(pattern, data.strip())
        return matches.group(1)

    def execute(self):
        logger.info(
            f" Reading file to pandas dataframe from location {self.input_path}"
        )
        df = pd.read_csv(
            self.input_path,
            sep="\t",
        )
        logger.info(f"Records in dataframe {len(df)}")
        if len(df) > 1:
            ip_unique = df.ip.unique()
            referrer_list = []

            for each_ip in ip_unique:
                df_per_ip = df[df["ip"] == each_ip].reset_index()
                df_per_ip["revenue"] = df_per_ip.product_list.apply(
                    self._parse_product_list
                )

                g = nx.DiGraph()
                for _i, row in df_per_ip.iterrows():
                    g.add_edge(row["referrer"], row["page_url"], revenue=row["revenue"])

                revenue = nx.get_edge_attributes(g, "revenue")

                for _i, row in df_per_ip.iterrows():
                    if self.retailer_domain in row["referrer"]:
                        pass
                    else:
                        revenue_amt = 0.00
                        x = dfs_tree(g, row["referrer"])
                        for u, v in list(x.edges()):
                            if self.checkout_page in v:
                                revenue_amt += revenue[(u, v)]
                        referrer_list.append(
                            {"Referrer": row["referrer"], "Revenue": revenue_amt}
                        )
            revenue_df = pd.DataFrame(referrer_list)
            revenue_df.insert(
                0,
                "Search Engine Domain",
                revenue_df.Referrer.apply(self._parse_referrer),
            )
            revenue_df.insert(
                1, "Search Keyword", revenue_df.Referrer.apply(self._parse_search_str)
            )
            revenue_df = revenue_df.drop("Referrer", axis=1).sort_values(
                by=["Revenue"], ascending=False
            )
            logger.info(
                f"Writing file from pandas dataframe to Location {self. output_file_qualified_path}"
            )
            revenue_df.to_csv(
                self.output_file_qualified_path,
                sep="\t",
                index=False,
                header=True,
            )
        else:
            logger.info(f"No records in input data. .will bypass processing")


def lambda_handler(event, context):
    try:
        input_path = os.environ.get(" INPUTPATH")
        obj = SearchKeywordPerformance(
            input_path, output_path, retailer_domain, checkout_page
        )
        obj.execute()
    except Exception as err:
        logger.error(f"Exception in processing {err}")
        traceback.format_exc(err)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(" --inputpath", help=" Path of input file")
    args = parser.parse_args()
    os.environ["INPUTPATH"] = args.inputpath.strip()
    lambda_handler({}, None)
