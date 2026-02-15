import os
import random
import subprocess
import uuid
from flask import Flask, request, send_file, jsonify

app = Flask(__name__)

HOOKS = [
    "This line changed everything",
    "You weren't supposed to see this",
    "She sent this at 2AM",
    "This is your sign",
    "He wasn't ready for this",
    "Nobody talks about this",
    "Watch till the end",
    "This hits different",
    "You know who this is about",
    "I shouldn't be posting this",
    "This one hurt",
    "Don't send this to her",
    "This got me in trouble",
    "POV: You miss her",
    "She wasn't expecting this",
    "He read it twice",
    "This was personal",
    "You felt this too",
    "This changed my mindset",
    "She never replied"
]

@app.route("/", methods=["POST"])
def edit_video():
    if "video" not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video = request.files["video"]

    hook = request.form.get("hook")
    if not hook:
        hook = random.choice(HOOKS)

    input_path = f"/tmp/{uuid.uuid4()}.mp4"
    output_path = f"/tmp/{uuid.uuid4()}_edited.mp4"

    video.save(input_path)

    command = [
        "ffmpeg",
        "-i", input_path,
        "-vf",
        f"drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='{hook}':fontcolor=white:fontsize=60:box=1:boxcolor=black@0.5:boxborderw=20:x=(w-text_w)/2:y=150",
        "-codec:a", "copy",
        output_path
    ]

    subprocess.run(command, check=True)

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
