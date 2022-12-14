import pandas as pd
import requests
import os
import numpy as np

# scroll down to the bottom to implement your solution

if __name__ == "__main__":

    if not os.path.exists("../Data"):
        os.mkdir("../Data")

    # Download data if it is unavailable.
    if (
        "A_office_data.xml" not in os.listdir("../Data")
        and "B_office_data.xml" not in os.listdir("../Data")
        and "hr_data.xml" not in os.listdir("../Data")
    ):
        print("A_office_data loading.")
        url = "https://www.dropbox.com/s/jpeknyzx57c4jb2/A_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open("../Data/A_office_data.xml", "wb").write(r.content)
        print("Loaded.")

        print("B_office_data loading.")
        url = "https://www.dropbox.com/s/hea0tbhir64u9t5/B_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open("../Data/B_office_data.xml", "wb").write(r.content)
        print("Loaded.")

        print("hr_data loading.")
        url = "https://www.dropbox.com/s/u6jzqqg1byajy0s/hr_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open("../Data/hr_data.xml", "wb").write(r.content)
        print("Loaded.")

        # All data in now loaded to the Data folder.

    # write your code here
    a = pd.read_xml("../Data/A_office_data.xml")
    b = pd.read_xml("../Data/B_office_data.xml")
    hr = pd.read_xml("../Data/hr_data.xml")

    a.index = a.employee_office_id.apply(lambda x: "A" + str(x))
    b.index = b.employee_office_id.apply(lambda x: "B" + str(x))
    hr.set_index("employee_id", inplace=True, drop=False)

    df = (
        pd.concat([a, b], axis=0)
        .merge(hr, left_index=True, right_index=True)
        .drop(["employee_office_id", "employee_id"], axis=1)
        .sort_index()
    )

    df2 = pd.pivot_table(
        df,
        index="Department",
        columns=["left", "salary"],
        values="average_monthly_hours",
        aggfunc="median",
    )

    print(
        df2[(df2[0, "high"] < df2[0, "medium"]) | (df2[1, "low"] < df2[1, "high"])]
        .round(2)
        .to_dict()
    )

    df3 = pd.pivot_table(
        df,
        index="time_spend_company",
        columns="promotion_last_5years",
        values=["satisfaction_level", "last_evaluation"],
        aggfunc=["min", "max", "mean"],
    )

    print(
        df3[df3["mean", "last_evaluation", 0] > df3["mean", "last_evaluation", 1]]
        .round(2)
        .to_dict()
    )
