from typing import Dict, Any, List
from PIL import Image
import numpy as np

def _image_to_array(img: Image.Image, max_size: int = 512) -> np.ndarray:
    # Resize for speed, keep aspect ratio
    w, h = img.size
    scale = min(max_size / max(w, h), 1.0)
    if scale < 1.0:
        img = img.resize((int(w*scale), int(h*scale)))
    arr = np.asarray(img).astype(np.float32) / 255.0
    return arr

def _dominant_colors(img: Image.Image, k: int = 5) -> List[dict]:
    # Use Pillow's quantize to find dominant colors quickly
    pal_img = img.convert('P', palette=Image.Palette.ADAPTIVE, colors=k)
    palette = pal_img.getpalette()[:k*3]
    color_counts = pal_img.getcolors()
    # color_counts: list of tuples (count, palette_index)
    if not color_counts:
        return []

    total = sum([c for c,_ in color_counts])
    colors = []
    for count, idx in sorted(color_counts, reverse=True):
        r = palette[idx*3 + 0]
        g = palette[idx*3 + 1]
        b = palette[idx*3 + 2]
        colors.append({
            "rgb": [int(r), int(g), int(b)],
            "hex": "#{:02x}{:02x}{:02x}".format(int(r), int(g), int(b)),
            "proportion": round(count / total, 4)
        })
    return colors[:k]

def _brightness_saturation(arr: np.ndarray) -> (float, float):
    # Convert to HSV
    eps = 1e-8
    r, g, b = arr[...,0], arr[...,1], arr[...,2]
    maxc = np.max(arr, axis=-1)
    minc = np.min(arr, axis=-1)
    v = maxc
    s = (maxc - minc) / (maxc + 1e-6)
    return float(np.mean(v)), float(np.mean(s))

def _name_palette(dominants: List[dict]) -> str:
    if not dominants:
        return "Unknown"
    # Compute mean saturation and classify
    rgbs = np.array([c["rgb"] for c in dominants]) / 255.0
    maxc = rgbs.max(axis=1)
    minc = rgbs.min(axis=1)
    s = (maxc - minc) / (maxc + 1e-6)
    mean_s = s.mean()
    # Simple heuristic
    if mean_s < 0.15:
        return "Neutral / Minimalist"
    elif mean_s < 0.35:
        return "Soft / Earthy"
    else:
        return "Bold / Vibrant"

def analyze_image(img: Image.Image) -> Dict[str, Any]:
    arr = _image_to_array(img)
    dom = _dominant_colors(img, k=5)
    brightness, saturation = _brightness_saturation(arr)
    palette_name = _name_palette(dom)
    return {
        "dominant_colors": dom,
        "brightness": round(brightness, 4),
        "saturation": round(saturation, 4),
        "palette_name": palette_name,
    }
