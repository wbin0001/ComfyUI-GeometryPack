# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025 ComfyUI-GeometryPack Contributors

"""
Main nodes - All non-Blender geometry processing nodes.
Runs in an isolation env (pixi/conda) to avoid DLL conflicts with ComfyUI's torch.
"""

import logging
import importlib
log = logging.getLogger("geometrypack")
log.setLevel(logging.INFO)

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
        log.warning("Skipping %s (missing dependency): %s", module_name, e)
        return False
    except Exception as e:
        log.warning("Skipping %s (import error): %s", module_name, e)
        return False


# Core nodes (pip-installable dependencies)
_safe_import('io')
_safe_import('primitives')
_safe_import('analysis')
_safe_import('distance')
_safe_import('conversion')
_safe_import('transforms')
_safe_import('visualization')
_safe_import('skeleton')
_safe_import('combine')
_safe_import('uv')
_safe_import('repair')
_safe_import('remeshing')
_safe_import('reconstruction')
_safe_import('texture_remeshing')
_safe_import('smoothing')
_safe_import('decimation')

# ParaView/VTK filter nodes
_safe_import('paraview')

# CGAL/igl nodes (require conda packages, skip if unavailable)
_safe_import('reconstruction_cgal')
_safe_import('boolean')
_safe_import('remeshing_cgal')
_safe_import('repair_cgal')
_safe_import('decimation_cgal')

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
