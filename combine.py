#!/usr/bin/env python

from pathlib import Path
from typer import Typer
import pandas as pd
import mrich
from mrich import print

app = Typer()


@app.command()
def combine(
    subdir: str,
    output: str,
    pattern: str = "*.csv",
):

    subdir = Path(subdir)

    # list to store the tables
    dfs = []

    # loop over all files in the directory and read them in
    for file in subdir.glob(pattern):
        mrich.reading(file)
        df = pd.read_csv(file, skiprows=1)
        dfs.append(df)

    # Combine all the tables
    df = pd.concat(dfs)

    # split the Name column into three
    df[["Organ", "Animal", "Time"]] = df["Name"].str.split("_", n=2, expand=True)

    # Create the index from the new columns
    df = df.set_index(["Organ", "Image name", "Time", "Animal"])

    # Sort the table
    df = df.sort_values(["Organ", "Image name", "Time"])

    # Write the output
    outfile = Path(output)
    mrich.writing(outfile)
    df.to_csv(outfile)


def main():
    app()


if __name__ == "__main__":
    main()
