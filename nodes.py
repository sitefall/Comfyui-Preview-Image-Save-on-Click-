import os, shutil
from aiohttp import web
from PIL import Image
import folder_paths
from server import PromptServer
from nodes import PreviewImage


class PreviewSaveOnDemand(PreviewImage):
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    CATEGORY = "image"


@PromptServer.instance.routes.post("/preview_save/save")
async def save_from_temp(request):
    data = await request.json()
    temp_dir = os.path.realpath(folder_paths.get_temp_directory())
    out_root = folder_paths.get_output_directory()
    saved = []
    for img in data.get("images", []):
        src = os.path.realpath(os.path.join(temp_dir, img.get("subfolder", ""), img["filename"]))
        if not src.startswith(temp_dir + os.sep) or not os.path.isfile(src):
            return web.json_response({"error": "invalid source file"}, status=400)
        with Image.open(src) as im:
            w, h = im.size
        folder, name, counter, subfolder, _ = folder_paths.get_save_image_path(
            data.get("prefix", "ComfyUI"), out_root, w, h)
        os.makedirs(folder, exist_ok=True)
        out_name = f"{name}_{counter:05}_.png"
        shutil.copy2(src, os.path.join(folder, out_name))
        saved.append(os.path.join(subfolder, out_name))
    return web.json_response({"saved": saved})