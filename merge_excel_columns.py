import pandas as pd
import argparse

def find_id_column(df, candidates=["Gene_ID", "Gene ID", "Gene_ID"]):
    """
    Find the first matching column from candidates in the dataframe.
    """
    for col in df.columns:
        if col.strip() in candidates:
            return col.strip()
    raise ValueError(f"No matching ID column found. Looked for {candidates}, found {list(df.columns)}")

def merge_excel_tables(tab1_file, tab2_file, output_file,
                       tab1_sheet=None, tab2_sheet=None):
    """
    Merge two Excel tables by identifying ID columns automatically.
    Keeps all metadata from both tables.
    If one table has 'Gene_ID', it becomes the reference table.
    """

    # Read Excel files
    df1 = pd.read_excel(tab1_file, sheet_name=tab1_sheet or 0)
    df2 = pd.read_excel(tab2_file, sheet_name=tab2_sheet or 0)

    print(f"Table 1 shape: {df1.shape}, columns: {list(df1.columns)}")
    print(f"Table 2 shape: {df2.shape}, columns: {list(df2.columns)}")

    # Identify ID columns
    id1 = find_id_column(df1)
    id2 = find_id_column(df2)

    print(f"Detected ID column in Table1: {id1}")
    print(f"Detected ID column in Table2: {id2}")

    # Decide which is reference (the one with Gene_ID takes priority)
    if id1 == "Gene_ID":
        ref_df, ref_id = df1, id1
        other_df, other_id = df2, id2
    elif id2 == "Gene_ID":
        ref_df, ref_id = df2, id2
        other_df, other_id = df1, id1
    else:
        # If neither has Gene_ID, just use df1 as reference
        ref_df, ref_id = df1, id1
        other_df, other_id = df2, id2
        print("⚠️ No 'Gene_ID' found, defaulting to Table1 as reference")

    # Clean IDs (string, strip spaces)
    ref_df[ref_id] = ref_df[ref_id].astype(str).str.strip()
    other_df[other_id] = other_df[other_id].astype(str).str.strip()

    # Merge (left join on reference, keep all metadata)
    merged = pd.merge(
        ref_df,
        other_df,
        left_on=ref_id,
        right_on=other_id,
        how="left",
        suffixes=("_tab1", "_tab2")
    )

    # Normalize ID column name
    merged.rename(columns={ref_id: "Gene_ID"}, inplace=True)
    cols = ["Gene_ID"] + [c for c in merged.columns if c != "Gene_ID"]
    merged = merged[cols]

    print(f"Merged table shape: {merged.shape}")
    print(f"Kept all {ref_df.shape[0]} rows from reference table, matched {merged[other_id].notna().sum()} rows with other table")

    # Save
    merged.to_excel(output_file, index=False)
    print(f"✅ Saved merged table to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flexible Excel merge by gene ID columns, keeping all metadata")
    parser.add_argument("tab1_file", help="First Excel file path")
    parser.add_argument("tab2_file", help="Second Excel file path")
    parser.add_argument("output_file", help="Output Excel file path")
    parser.add_argument("--tab1_sheet", help="Sheet name in first Excel file (default: first sheet)")
    parser.add_argument("--tab2_sheet", help="Sheet name in second Excel file (default: first sheet)")
    args = parser.parse_args()

    merge_excel_tables(
        tab1_file=args.tab1_file,
        tab2_file=args.tab2_file,
        output_file=args.output_file,
        tab1_sheet=args.tab1_sheet,
        tab2_sheet=args.tab2_sheet
    )

