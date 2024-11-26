import json
import folium
from shapely.geometry import Point, Polygon
import geopandas as gpd

# JSONファイルの読み込みとエラーハンドリング
try:
    with open('suirotuuhou.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except Exception as e:
    print(f"Error reading JSON file: {e}")
    exit(1)

# 座標リストと名前リストを準備
coordinates = []
names = []

# JSONデータから座標と名前を抽出
for feature in data["features"]:
    attributes = feature.get("attributes", {})
    geometry = feature.get("geometry", {})
    
    name = attributes.get("name")
    x = geometry.get("x")
    y = geometry.get("y")
    
    if name is not None and x is not None and y is not None:
        # スペースで区切り、一番後ろの文言を取得
        last_word = name.split()[-1]
        
        coordinates.append((y, x))  # foliumは(緯度, 経度)の順
        names.append(last_word)

# foliumマップの作成
m = folium.Map(location=[35.5, 139.8], zoom_start=10)

# ポイントを追加
for coord, name in zip(coordinates, names):
    folium.Marker(location=coord, popup=name).add_to(m)

# 多角形データの読み込み
try:
    with open('polygons.json', 'r', encoding='utf-8') as f:
        polygons = json.load(f)
except Exception as e:
    print(f"Error reading polygons JSON file: {e}")
    exit(1)

# 多角形をマップに追加
for polygon in polygons:
    folium.Polygon(
        locations=polygon["coordinates"],
        color=polygon["color"],
        fill=True,
        fill_color=polygon["color"],
        fill_opacity=polygon["fill_opacity"],
        popup=polygon["popup"]
    ).add_to(m)

# マップをHTMLファイルとして保存
m.save('map_with_alerts.html')

# マップの表示
m
