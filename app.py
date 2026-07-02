from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
PLOT_FOLDER = "static/plots"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PLOT_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def home():

    preview = None
    stats = None

    rows = None
    columns = None
    missing = None

    plot_path = None

    error = None

    if request.method == "POST":

        file = request.files["csv_file"]

        if file.filename == "":

            error = "Please choose a CSV file."

        else:

            filepath = os.path.join(
                app.config["UPLOAD_FOLDER"],
                file.filename
            )

            file.save(filepath)

            try:

                df = pd.read_csv(filepath)

                preview = df.head(10).to_html(
                    classes="table",
                    index=False
                )

                rows = df.shape[0]

                columns = df.shape[1]

                missing = int(df.isnull().sum().sum())

                stats = df.describe().round(2).to_html(
                    classes="table"
                )

                numeric_columns = df.select_dtypes(include="number").columns

                if len(numeric_columns) > 0:

                    plt.figure(figsize=(7,4))

                    df[numeric_columns[0]].hist(
                        bins=20,
                        edgecolor="black"
                    )

                    plt.title(f"Histogram of {numeric_columns[0]}")
                    plt.xlabel(numeric_columns[0])
                    plt.ylabel("Frequency")

                    plt.tight_layout()

                    plot_path = "plots/histogram.png"

                    plt.savefig(
                        os.path.join(
                            "static",
                            plot_path
                        )
                    )

                    plt.close()

            except Exception as e:

                error = str(e)

    return render_template(

        "index.html",

        preview=preview,

        stats=stats,

        rows=rows,

        columns=columns,

        missing=missing,

        plot_path=plot_path,

        error=error

    )


if __name__ == "__main__":
    app.run(debug=True)