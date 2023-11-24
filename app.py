import time
from flask import Flask, request, render_template
from flask import request, render_template_string

# Flask constructor
app = Flask(__name__)
@app.route('/', methods=["GET", "POST"])
def gfg():
    wr="test"
    # connecting to AWS using the CLI  
    aws_access_key_id = "AKIAJSIE27KKMHXI3BJQ"
    aws_secret_access_key = "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"

    if request.method == "POST":
        first_ornament=request.form.get("ornament1")
        second_ornament = request.form.get("ornament1")
        uppercount2 = request.form.get("uppercount1")
        lowercount2 = request.form.get("lowercount1")
        grossweightlowerrange2 = request.form.get("grossweightlowerrange1")
        grossweightupperrange2 = request.form.get("grossweightupperrange1")
        # Get the output into a dataframe by using **wr** which is the aws datawrangler package to interact with AWS
        df = wr.athena.read_sql_query("query", database="databasename")
        # Specify the path of the bucket where the result will be stored as **file1.csv**
        bucket = 'input_bucketname'
        path1 = f"s3://{bucket}/file1.csv"
        # Write the csv file to the S3 bucket
        wr.s3.to_csv(df, path1, index=False)
    return render_template("index.html")


@app.route('/serversidetemplate')
def example():
    username = request.args.get('username')
    template = f"<p>Hello {username}</p>"
    return render_template_string(template)


