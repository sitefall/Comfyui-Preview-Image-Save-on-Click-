# Preview Image (Save on Click)

A small ComfyUI custom node that works like the built-in Preview Image node, with one addition: a button that saves the image to your output folder only when you click it.

Preview Image doesn't save anything, so a great seed is easy to lose. Save Image saves everything, so your output folder fills up with images you have to delete later. This node sits between the two. You preview as usual, and when one looks good you click Save. The saved file keeps the embedded workflow, prompt and seed, same as Save Image.

## Install

Clone the repo into your `custom_nodes` folder:

```
cd ComfyUI/custom_nodes
git clone https://github.com/sitefall/Comfyui-Preview-Image-Save-on-Click-
```

Or download the ZIP and extract it into `ComfyUI/custom_nodes/`. The folder should contain `__init__.py` directly.

Restart ComfyUI, then hard-refresh your browser (Ctrl+F5).

## Usage

1. Double-click the canvas and search for "Preview Image (Save on Click)". The node is called **Preview Image (Save on Click)** and lives under `image`.
2. Connect your `IMAGE` output to the `images` input.
3. Set `filename_prefix` if you want. It works the same as on Save Image, so `Keepers/portraits/img_` saves into `output/Keepers/portraits/` with a file called `img_n` (with n being whatever number Comfyui gives it.
4. Run the workflow. The image shows up on the node like a normal preview.
5. If you like it, click **Save this image**. The button label shows the saved file name for a few seconds.

If you generated a batch, the button saves every image in that batch.

## Notes

- No idea if this works with Nodes2.0 I have never touched that in my life and don't intend to.
- Previews live in ComfyUI's temp folder, which is cleared when ComfyUI restarts. Save before you restart.
- The button only saves the image(s) currently in the preview.  If you don't save it when it's generated, and don't pull it from the temp folder before restarting Comfyui, it's lost.
- If you start ComfyUI with `--disable-metadata`, the saved images won't contain the workflow (obviously).

## How it works

The node is a thin subclass of ComfyUI's built-in `PreviewImage`. It writes preview images to the temp folder the same way the stock node does. Those temp PNGs already have the workflow and prompt embedded in them, so nothing extra needs to be captured.

The Save button is added by a small JavaScript extension (`js/save_button.js`). Each time the node finishes executing, the extension remembers which temp files were just shown. When you click the button, it sends those file names and your `filename_prefix` to a custom server route, `/preview_save/save`.

The route (in `nodes.py`) checks that each file is really inside the temp folder, then works out the destination using ComfyUI's own `get_save_image_path`. That's why prefixes, subfolders and the numbered file names (`name_00001_.png`) behave like Save Image. The temp file is then copied to the output folder as is, which keeps the metadata intact.

## License

MIT
