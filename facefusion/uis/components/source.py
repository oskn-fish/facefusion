from typing import Optional, List
import gradio

import facefusion.globals
from facefusion import wording
from facefusion.uis.typing import File
from facefusion.filesystem import are_images
from facefusion.uis.core import register_ui_component

SOURCE_FILE : Optional[gradio.File] = None
SOURCE_IMAGE : Optional[gradio.Image] = None

SOURCE_FILE_PATHS = None
SOURCE_GRADIO_IMAGE = None

def render(source_ui) -> None:
	global SOURCE_FILE
	global SOURCE_IMAGE

	are_source_images = are_images(facefusion.globals.source_paths)
	SOURCE_FILE = gradio.File(
		file_count = 'multiple',
		file_types =
		[
			'.png',
			'.jpg',
			'.webp'
		],
		label = wording.get('source_file_label'),
		value = facefusion.globals.source_paths if are_source_images else SOURCE_FILE_PATHS
	)
	source_file_names = [ source_file_value['name'] for source_file_value in SOURCE_FILE.value ] if SOURCE_FILE.value else None
	SOURCE_IMAGE = gradio.Image(
		value = source_file_names[0] if are_source_images else None,
		visible = are_source_images,
		show_label = False
	)
	register_ui_component('source_image', SOURCE_IMAGE)
	source_ui.load(restore, outputs = [SOURCE_IMAGE, SOURCE_FILE])


def listen() -> None:
	SOURCE_FILE.change(update, inputs = SOURCE_FILE, outputs = SOURCE_IMAGE)
 
def restore() -> None:
    return SOURCE_GRADIO_IMAGE, SOURCE_FILE_PATHS
    

def update(files : List[File]) -> gradio.Image:
	file_names = [ file.name for file in files ] if files else None
	global SOURCE_FILE_PATHS
	SOURCE_FILE_PATHS = file_names
	if are_images(file_names):
		facefusion.globals.source_paths = file_names
		SOURCE_GRADIO_IMAGE = gradio.Image(value = file_names[0], visible = True)
		return SOURCE_GRADIO_IMAGE
	facefusion.globals.source_paths = None
	return gradio.Image(value = None, visible = False)
