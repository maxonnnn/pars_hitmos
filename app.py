from flask import Flask, request, jsonify
from parse_hitmos.entered_tracks import EnteredTrack
import json

app = Flask(__name__)

@app.route('/search')
def search():
    query = request.args.get('q')
    limit = int(request.args.get('limit', 20))
    if not query:
        return jsonify({"error": "Missing query"}), 400
    
    result = EnteredTrack(query, limit)
    tracks = []
    for track in result:
        tracks.append({
            "id": track.get_url_track(),
            "title": track.get_title(),
            "artist": track.get_author(),
            "duration": track.get_duration(),
            "artwork": track.get_picture_url(),
            "download_url": track.direct_download_link
        })
    return jsonify(tracks)

@app.route('/download')
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Missing URL"}), 400
    
    result = EnteredTrack(url, 1)
    if result:
        return jsonify({"download_url": result[0].direct_download_link})
    return jsonify({"error": "Track not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
