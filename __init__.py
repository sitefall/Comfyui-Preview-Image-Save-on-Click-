from .nodes import PreviewSaveOnDemand

NODE_CLASS_MAPPINGS = {"PreviewSaveOnDemand": PreviewSaveOnDemand}
NODE_DISPLAY_NAME_MAPPINGS = {"PreviewSaveOnDemand": "Preview Image (Save on Click)"}
WEB_DIRECTORY = "./js"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]