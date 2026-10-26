"""
Pandas Analyzer & Data Visualization
Red & White Skill Education - Project

Install dependencies:
    python -m pip install pandas numpy matplotlib seaborn

Run:
    python pandas_analyzer.py

Place your CSV file in the same folder, or enter its full path when prompted.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class SalesDataAnalyzer:
    """Load, explore, clean, analyze, and visualize CSV data."""

    def __init__(self):
        self.df = None
        self.file_path = None

    # ---------- Data loading and exploration ----------

    def load_data(self, file_path=None):
        if not file_path:
            file_path = input("Enter the path of the CSV file: ").strip().strip('"')

        try:
            self.df = pd.read_csv(file_path)
            self.file_path = file_path
            print(f"\nDataset loaded successfully! ({len(self.df)} rows, {len(self.df.columns)} columns)")
            print("\nFirst 5 rows:")
            print(self.df.head().to_string())
            return True
        except FileNotFoundError:
            print("File not found. Check the path and try again.")
        except pd.errors.EmptyDataError:
            print("The file is empty.")
        except Exception as error:
            print(f"Could not load the file: {error}")
        return False

    def require_data(self):
        if self.df is None:
            print("Please load a CSV file first (menu option 1).")
            return False
        return True

    def explore_data(self):
        if not self.require_data():
            return

        print("\n--- DATA OVERVIEW ---")
        print(f"Rows: {self.df.shape[0]} | Columns: {self.df.shape[1]}")
        print("\nColumn names:")
        print(list(self.df.columns))
        print("\nFirst 5 rows:")
        print(self.df.head().to_string())
        print("\nLast 5 rows:")
        print(self.df.tail().to_string())
        print("\nData types:")
        print(self.df.dtypes.to_string())
        print("\nDataset information:")
        self.df.info()
        print("\nDuplicate rows:", self.df.duplicated().sum())
        print("\nMissing values per column:")
        print(self.df.isnull().sum().to_string())

    # ---------- DataFrame operations ----------

    def dataframe_operations(self):
        if not self.require_data():
            return

        while True:
            print("""
--- DATAFRAME OPERATIONS ---
1. Display all data
2. Display first 5 rows
3. Display last 5 rows
4. Display column names and data types
5. Select a column
6. Filter rows by a numeric condition
7. Sort data
8. Add a calculated column
9. Split data by a column value
0. Back to main menu
""")
            choice = input("Enter your choice: ").strip()

            if choice == "0":
                break
            elif choice == "1":
                print(self.df.to_string())
            elif choice == "2":
                print(self.df.head().to_string())
            elif choice == "3":
                print(self.df.tail().to_string())
            elif choice == "4":
                print(self.df.dtypes.to_string())
            elif choice == "5":
                col = self.choose_column()
                if col is not None:
                    print(self.df[col].to_string(index=False))
            elif choice == "6":
                numeric_cols = self.df.select_dtypes(include=np.number).columns.tolist()
                if not numeric_cols:
                    print("No numeric columns available.")
                    continue
                print("Numeric columns:", numeric_cols)
                col = input("Column to filter: ").strip()
                if col not in numeric_cols:
                    print("Choose a valid numeric column.")
                    continue
                operator = input("Condition (>, >=, <, <=, ==, !=): ").strip()
                raw_value = input("Value: ").strip()
                try:
                    value = float(raw_value)
                    conditions = {
                        ">": self.df[col] > value,
                        ">=": self.df[col] >= value,
                        "<": self.df[col] < value,
                        "<=": self.df[col] <= value,
                        "==": self.df[col] == value,
                        "!=": self.df[col] != value,
                    }
                    if operator not in conditions:
                        print("Invalid operator.")
                    else:
                        result = self.df.loc[conditions[operator]]
                        print(result.to_string(index=False) if not result.empty else "No matching rows.")
                except ValueError:
                    print("Enter a numeric value.")
            elif choice == "7":
                col = self.choose_column()
                if col is not None:
                    order = input("Ascending order? (y/n): ").strip().lower() != "n"
                    print(self.df.sort_values(by=col, ascending=order, na_position="last").to_string(index=False))
            elif choice == "8":
                new_col = input("Name for the new column: ").strip()
                numeric_cols = self.df.select_dtypes(include=np.number).columns.tolist()
                print("Numeric columns:", numeric_cols)
                if not new_col or not numeric_cols:
                    print("A name and at least one numeric column are required.")
                    continue
                col1 = input("First numeric column: ").strip()
                col2 = input("Second numeric column: ").strip()
                operation = input("Operation (+, -, *, /): ").strip()
                if col1 not in numeric_cols or col2 not in numeric_cols:
                    print("Choose valid numeric columns.")
                    continue
                try:
                    if operation == "+":
                        self.df[new_col] = self.df[col1] + self.df[col2]
                    elif operation == "-":
                        self.df[new_col] = self.df[col1] - self.df[col2]
                    elif operation == "*":
                        self.df[new_col] = self.df[col1] * self.df[col2]
                    elif operation == "/":
                        self.df[new_col] = self.df[col1] / self.df[col2].replace(0, np.nan)
                    else:
                        print("Invalid operation.")
                        continue
                    print(f"Column '{new_col}' added.")
                    print(self.df[[col1, col2, new_col]].head().to_string(index=False))
                except Exception as error:
                    print("Could not create column:", error)
            elif choice == "9":
                col = self.choose_column()
                if col is not None:
                    print("\nAvailable values:")
                    print(self.df[col].dropna().astype(str).unique().tolist())
                    value = input("Enter the value to select: ").strip()
                    result = self.df[self.df[col].astype(str) == value]
                    print(result.to_string(index=False) if not result.empty else "No matching rows.")
                    if not result.empty:
                        save = input("Save these rows to a new CSV? (y/n): ").strip().lower()
                        if save == "y":
                            output = input("Output filename [filtered_data.csv]: ").strip() or "filtered_data.csv"
                            result.to_csv(output, index=False)
                            print("Saved to", output)
            else:
                print("Invalid choice. Try again.")

    def choose_column(self):
        print("Columns:", self.df.columns.tolist())
        col = input("Enter a column name exactly as shown: ").strip()
        if col not in self.df.columns:
            print("Column not found.")
            return None
        return col

    # ---------- Missing values ----------

    def handle_missing_data(self):
        if not self.require_data():
            return

        print("\nMissing values per column:")
        print(self.df.isnull().sum().to_string())
        print("""
1. Display rows containing missing values
2. Drop rows with missing values
3. Drop columns containing missing values
4. Fill missing values with each column's mean (numeric columns only)
5. Fill missing values with each column's median (numeric columns only)
6. Fill missing values with a specific value
0. Back
""")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            missing_rows = self.df[self.df.isnull().any(axis=1)]
            print(missing_rows.to_string() if not missing_rows.empty else "No missing values found.")
        elif choice == "2":
            before = len(self.df)
            self.df = self.df.dropna().copy()
            print(f"Removed {before - len(self.df)} rows.")
        elif choice == "3":
            before = len(self.df.columns)
            self.df = self.df.dropna(axis=1).copy()
            print(f"Removed {before - len(self.df.columns)} columns.")
        elif choice in ("4", "5"):
            numeric_cols = self.df.select_dtypes(include=np.number).columns
            if len(numeric_cols) == 0:
                print("No numeric columns available.")
            else:
                for col in numeric_cols:
                    fill_value = self.df[col].mean() if choice == "4" else self.df[col].median()
                    if pd.notna(fill_value):
                        self.df[col] = self.df[col].fillna(fill_value)
                print("Missing numeric values filled.")
                print("Note: missing values in text columns were not changed.")
        elif choice == "6":
            value = input("Value to use for missing cells (e.g. Unknown or 0): ")
            self.df = self.df.fillna(value)
            print("Missing values filled.")
        elif choice == "0":
            return
        else:
            print("Invalid choice.")
            return

        print("\nMissing values remaining:")
        print(self.df.isnull().sum().to_string())

    # ---------- Statistics ----------

    def descriptive_statistics(self):
        if not self.require_data():
            return

        print("\n--- DESCRIPTIVE STATISTICS ---")
        print("\nNumeric summary:")
        print(self.df.describe().to_string())
        print("\nSummary including text columns:")
        print(self.df.describe(include="all").to_string())
        numeric = self.df.select_dtypes(include=np.number)
        if not numeric.empty:
            print("\nMean:")
            print(numeric.mean().to_string())
            print("\nMedian:")
            print(numeric.median().to_string())
            print("\nMode:")
            print(numeric.mode().to_string(index=False))
            print("\nStandard deviation:")
            print(numeric.std().to_string())
            print("\nCorrelation matrix:")
            print(numeric.corr().to_string())
        else:
            print("No numeric columns found for numerical statistics.")

    # ---------- Visualization ----------

    def visualize_data(self):
        if not self.require_data():
            return

        print("""
--- DATA VISUALIZATION ---
1. Bar plot
2. Line plot
3. Scatter plot
4. Pie chart
5. Histogram
6. Stacked bar plot
7. Correlation heatmap (Seaborn)
0. Back
""")
        choice = input("Enter your choice: ").strip()
        if choice == "0":
            return

        numeric_cols = self.df.select_dtypes(include=np.number).columns.tolist()
        if choice == "7":
            if len(numeric_cols) < 2:
                print("At least two numeric columns are needed for a heatmap.")
                return
            plt.figure(figsize=(9, 6))
            sns.heatmap(self.df[numeric_cols].corr(), annot=True, cmap="coolwarm", fmt=".2f")
            plt.title("Correlation Heatmap")
        elif choice == "5":
            col = self.choose_column()
            if col is None:
                return
            if not pd.api.types.is_numeric_dtype(self.df[col]):
                print("Choose a numeric column for a histogram.")
                return
            plt.figure(figsize=(8, 5))
            self.df[col].dropna().plot(kind="hist", bins=10, edgecolor="black")
            plt.title(f"Histogram of {col}")
            plt.xlabel(col)
        elif choice in ("1", "2", "3", "6"):
            if not numeric_cols:
                print("No numeric columns available.")
                return
            print("Numeric columns:", numeric_cols)
            x_col = input("X-axis/category column: ").strip()
            y_col = input("Y-axis numeric column: ").strip()
            if x_col not in self.df.columns or y_col not in numeric_cols:
                print("Choose valid columns.")
                return
            data = self.df[[x_col, y_col]].dropna()
            if data.empty:
                print("There is no complete data to plot.")
                return
            if choice == "3":
                plt.figure(figsize=(8, 5))
                plt.scatter(data[x_col], data[y_col])
                plt.xlabel(x_col)
                plt.ylabel(y_col)
                plt.title(f"{y_col} vs {x_col}")
            else:
                grouped = data.groupby(x_col, dropna=False)[y_col].sum()
                plt.figure(figsize=(9, 5))
                if choice == "1":
                    grouped.plot(kind="bar")
                    plt.title(f"{y_col} by {x_col} (Bar Plot)")
                elif choice == "2":
                    grouped.plot(kind="line", marker="o")
                    plt.title(f"{y_col} by {x_col} (Line Plot)")
                elif choice == "6":
                    second_col = input("Optional second numeric column for stacking (press Enter to skip): ").strip()
                    if second_col:
                        if second_col not in numeric_cols or second_col == y_col:
                            print("Invalid second numeric column.")
                            plt.close()
                            return
                        stack_data = self.df[[x_col, y_col, second_col]].dropna()
                        stack_data.groupby(x_col)[[y_col, second_col]].sum().plot(kind="bar", stacked=True)
                        plt.title(f"Stacked Bar Plot by {x_col}")
                    else:
                        print("A stacked bar needs two numeric columns; using the selected column only is not possible.")
                        plt.close()
                        return
                plt.xlabel(x_col)
                plt.ylabel(y_col)
                plt.xticks(rotation=45, ha="right")
        elif choice == "4":
            if not numeric_cols:
                print("No numeric columns available.")
                return
            print("Numeric columns:", numeric_cols)
            value_col = input("Numeric column for pie values: ").strip()
            if value_col not in numeric_cols:
                print("Choose a valid numeric column.")
                return
            category_col = self.choose_column()
            if category_col is None:
                return
            grouped = self.df.groupby(category_col)[value_col].sum().dropna()
            grouped = grouped[grouped >= 0]
            if grouped.empty or grouped.sum() == 0:
                print("No positive values available for a pie chart.")
                return
            plt.figure(figsize=(7, 7))
            plt.pie(grouped, labels=grouped.index.astype(str), autopct="%1.1f%%", startangle=90)
            plt.title(f"{value_col} by {category_col}")
        else:
            print("Invalid choice.")
            return

        plt.tight_layout()
        plt.show()

        save = input("Save this visualization? (y/n): ").strip().lower()
        if save == "y":
            filename = input("Filename [visualization.png]: ").strip() or "visualization.png"
            if not filename.lower().endswith((".png", ".jpg", ".jpeg", ".pdf")):
                filename += ".png"
            # Recreate the figure if a plotting function already displayed it.
            try:
                plt.savefig(filename, dpi=300, bbox_inches="tight")
                print("Visualization saved to", filename)
            except Exception as error:
                print("Could not save visualization:", error)
        plt.close("all")

    # ---------- Save / advanced operations ----------

    def save_data(self):
        if not self.require_data():
            return
        filename = input("Output CSV filename [cleaned_data.csv]: ").strip() or "cleaned_data.csv"
        if not filename.lower().endswith(".csv"):
            filename += ".csv"
        try:
            self.df.to_csv(filename, index=False)
            print("Data saved to", filename)
        except Exception as error:
            print("Could not save data:", error)

    def advanced_operations(self):
        if not self.require_data():
            return
        print("""
--- ADVANCED OPERATIONS ---
1. Remove duplicate rows
2. Group data and calculate a sum
3. Display unique values in a column
4. Export current data to CSV
0. Back
""")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            before = len(self.df)
            self.df = self.df.drop_duplicates().copy()
            print(f"Removed {before - len(self.df)} duplicate rows.")
        elif choice == "2":
            numeric_cols = self.df.select_dtypes(include=np.number).columns.tolist()
            if not numeric_cols:
                print("No numeric columns available.")
                return
            group_col = self.choose_column()
            if group_col is None:
                return
            print("Numeric columns:", numeric_cols)
            value_col = input("Numeric column to sum: ").strip()
            if value_col not in numeric_cols:
                print("Choose a valid numeric column.")
                return
            print(self.df.groupby(group_col, dropna=False)[value_col].sum().to_string())
        elif choice == "3":
            col = self.choose_column()
            if col is not None:
                print(self.df[col].dropna().unique().tolist())
        elif choice == "4":
            self.save_data()
        elif choice == "0":
            return
        else:
            print("Invalid choice.")


def create_sample_csv(filename="sample_sales.csv"):
    """Create a small sample dataset for first-time testing."""
    sample = pd.DataFrame({
        "Sales": [100, 150, 200, 120, 180, 90],
        "Product": ["Product A", "Product B", "Product C", "Product A", "Product B", "Product C"],
        "Region": ["North", "East", "West", "South", "East", "North"],
        "Profit": [20, 35, 50, 15, 40, 10],
        "Year": [2023, 2023, 2024, 2024, 2025, 2025],
    })
    sample.to_csv(filename, index=False)
    print(f"Sample dataset created: {filename}")


def main():
    analyzer = SalesDataAnalyzer()

    while True:
        print("""
========================================
  DATA ANALYSIS & VISUALIZATION PROGRAM
========================================
1. Load Dataset
2. Explore Data
3. Perform DataFrame Operations
4. Handle Missing Data
5. Generate Descriptive Statistics
6. Data Visualization
7. Save Data
8. Advanced Operations
9. Create Sample CSV
0. Exit
========================================
""")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            analyzer.load_data()
        elif choice == "2":
            analyzer.explore_data()
        elif choice == "3":
            analyzer.dataframe_operations()
        elif choice == "4":
            analyzer.handle_missing_data()
        elif choice == "5":
            analyzer.descriptive_stati--stics()
        elif choice == "6":
            analyzer.visualize_data()
        elif choice == "7":
            analyzer.save_data()
        elif choice == "8":
            analyzer.advanced_operations()
        elif choice == "9":
            create_sample_csv()
        elif choice == "0":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from the menu.")


if __name__ == "__main__":
    main()