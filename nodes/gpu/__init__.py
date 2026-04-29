import logging
import importlib

log = logging.getLogger("geometrypack")

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}


def _safe_import(module_name):
    """Import a submodule and merge its node mappings. Skip on ImportError."""
    try:
        mod = importlib.import_module(f'.{module_name}', package=__name__)
        NODE_CLASS_MAPPINGS.update(getattr(mod, 'NODE_CLASS_MAPPINGS', {}))
        NODE_DISPLAY_NAME_MAPPINGS.update(getattr(mod, 'NODE_DISPLAY_NAME_MAPPINGS', {}))
        return True
    except ImportError as e:
        log.warning("Skipping gpu.%s (missing dependency): %s", module_name, e)
        return False
    except Exception as e:
        log.warning("Skipping gpu.%s (import error): %s", module_name, e)
        return False


_safe_import('remeshing_gpu')
_safe_import('fill_holes_gpu')
_safe_import('uv_gpu')

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
