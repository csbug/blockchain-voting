import os

from flask import Flask, request, jsonify, render_template

from blockchain import Blockchain

app = Flask(__name__)

blockchain = Blockchain()

CANDIDATES = ["月下", "观星", "爱莉希雅"]

voters = set()

PENDING_VOTES = []


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/candidates")
def get_candidates():
    return jsonify({"candidates": CANDIDATES})


@app.route("/vote", methods=["POST"])
def vote():
    data = request.get_json()
    voter = (data or {}).get("voter", "").strip()
    candidate = (data or {}).get("candidate", "").strip()

    if not voter or not candidate:
        return jsonify({"error": "选民和候选人不能为空"}), 400

    if candidate not in CANDIDATES:
        return jsonify({"error": "候选人不存在"}), 400

    if voter in voters:
        return jsonify({"error": "该选民已经投过票"}), 400

    voters.add(voter)
    vote_record = {"voter": voter, "candidate": candidate}
    PENDING_VOTES.append(vote_record)
    block = blockchain.add_block(PENDING_VOTES.copy())
    PENDING_VOTES.clear()

    return jsonify(
        {
            "message": "投票成功",
            "block_index": block.index,
            "block_hash": block.hash,
        }
    ), 201


@app.route("/results")
def results():
    tally = {c: 0 for c in CANDIDATES}
    for block in blockchain.chain:
        for vote in block.votes:
            if vote["candidate"] in tally:
                tally[vote["candidate"]] += 1
    return jsonify({"tally": tally, "total_votes": sum(tally.values())})


@app.route("/chain")
def chain():
    return jsonify(
        {
            "length": len(blockchain.chain),
            "valid": blockchain.is_valid(),
            "chain": [block.to_dict() for block in blockchain.chain],
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
