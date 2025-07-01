from flask import Flask, render_template, request, redirect, url_for, send_file, flash, jsonify
import json, os
from verifier import run_verification, validate_single, DEFAULT_FIELD_TYPES

app = Flask(__name__)
app.secret_key = "replace‑me"

UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("inputjson")
        if not file:
            flash("Please choose a JSON file")
            return redirect(url_for("upload"))
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
        return redirect(url_for("verify", filename=file.filename))
    return render_template("upload.html")

@app.route("/verify/<filename>", methods=["GET", "POST"])
def verify(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    data = json.load(open(path, encoding="utf-8"))

    if request.method == "POST":
        output, ok = run_verification(data, request.form)
        if ok:
            out_path = os.path.join(UPLOAD_FOLDER, f"output_{filename}")
            json.dump(output, open(out_path, "w", encoding="utf-8"), indent=2)
            return redirect(url_for("summary", outname=os.path.basename(out_path)))
        flash("Please fix the highlighted errors.")
        return render_template(
            "verify.html",
            data=data,
            form=request.form,
            errors=output["errors"],
            DEFAULT_FIELD_TYPES=DEFAULT_FIELD_TYPES
        )

    return render_template(
        "verify.html",
        data=data,
        form={},
        errors={},
        DEFAULT_FIELD_TYPES=DEFAULT_FIELD_TYPES
    )

@app.post("/api/validate")
def api_validate():
    payload = request.json or {}
    ok, _, msg = validate_single(
        payload.get("value", ""),
        payload.get("vtype", "text"),
        payload.get("required", False)
    )
    return jsonify(ok=ok, msg=msg)

@app.route("/summary/<outname>")
def summary(outname):
    return render_template("summary.html", outname=outname)

@app.route("/download/<outname>")
def download(outname):
    path = os.path.join(UPLOAD_FOLDER, outname)
    return send_file(path, as_attachment=True, download_name="output.json")

if __name__ == "__main__":
    app.run(debug=True)
