import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

app.registerExtension({
  name: "PreviewSaveOnDemand",
  async beforeRegisterNodeDef(nodeType, nodeData) {
    if (nodeData.name !== "PreviewSaveOnDemand") return;

    const onNodeCreated = nodeType.prototype.onNodeCreated;
    nodeType.prototype.onNodeCreated = function () {
      onNodeCreated?.apply(this, arguments);
      const node = this;
      const btn = node.addWidget("button", "Save this image", null, async () => {
        if (!node._lastImages?.length) { btn.name = "Nothing to save yet"; node.setDirtyCanvas(true); return; }
        const prefix = node.widgets.find(w => w.name === "filename_prefix").value;
        const r = await api.fetchApi("/preview_save/save", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ images: node._lastImages, prefix }),
        });
        const j = await r.json();
        btn.name = r.ok ? `Saved: ${j.saved.join(", ")}` : "Save failed (see console)";
        node.setDirtyCanvas(true);
        setTimeout(() => { btn.name = "Save this image"; node.setDirtyCanvas(true); }, 4000);
      });
    };

    const onExecuted = nodeType.prototype.onExecuted;
    nodeType.prototype.onExecuted = function (message) {
      onExecuted?.apply(this, arguments);
      this._lastImages = message?.images ?? [];
    };
  },
});